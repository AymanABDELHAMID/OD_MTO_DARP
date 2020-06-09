"""
In this script we are going to use p-median
method to solve the station allocation problem
"""

import gurobipy as gp
from gurobipy import GRB
import json
from itertools import product
from math import sqrt
import numpy as np

# Parameters
# Get booking data
# adding type hint to the dict
with open('data/data_generated/bookings_short.json') as f:
    data_bookings = json.load(f)

# Get Stations data
with open('data/data_generated/stations.json') as f:
    data_stations = json.load(f)


# Compute key parameters of MIP model formulation
num_bookings = len(data_bookings)
num_pickup_stations = len(data_stations)
cartesian_prod = list(product(range(num_bookings), range(num_pickup_stations)))
cost_per_step = 1
distance_limit = np.zeros(num_bookings)
for booking in range(num_bookings):
    distance_limit[booking] = data_bookings[booking]["jobs"][0]["distancelimit"]
setup_cost = []  # np.zeros(num_pickup_stations)
for station in range(num_pickup_stations):
    # setup_cost[station] = data_stations[station]["setupCost"]
    setup_cost.append(data_stations[station]["setupCost"])


# This function determines the Euclidean distance between a pickup station and booking location.
def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)

# Compute shipping costs
#matching_cost = {(c, f): cost_per_step*compute_distance(data_bookings[c]["jobs"][0]["location"], data_stations[f]["location"]) for c, f in cartesian_prod}
matching_cost = np.zeros((num_bookings, num_pickup_stations))
for c in range(num_bookings):
    for f in range(num_pickup_stations):
        matching_cost[c, f] = cost_per_step*compute_distance(data_bookings[c]["jobs"][0]["location"], data_stations[f]["location"])
# this is a list containing all bookings with the corresponding cost to each station so the size of it
# is equal to num_bookings*num_pickup_stations

# MIP  model formulation

model = gp.Model('pickup_stations')

# select = model.addVars(num_pickup_stations, vtype=GRB.BINARY, name='Select')
assign = model.addMVar(shape=(num_bookings,num_pickup_stations), vtype=GRB.BINARY, name='Assign')  # vtype=GRB.CONTINUOUS

#model.addConstrs((assign[(c, f)] <= select[f] for c, f in cartesian_prod), name='Numbers')
model.addConstrs((sum(assign[c, :]) == 1 for c in range(num_bookings)), name='serveOnce')
#model.addConstrs((gp.quicksum(assign[(c, f)] for f in range(num_pickup_stations)) == 1 for c in range(num_bookings)), name='distance_lim')
model.addConstrs((assign[c,f]*matching_cost[c,f]*250 <= (distance_limit[c] + 2000) for c, f in cartesian_prod), name='distance_lim')  # for f in range(num_pickup_stations) for c in range(num_bookings)

# Save model
model.write('Station_alloc/pickup_pmedian_v1.lp')

#model.setObjective(select.prod(setup_cost)+assign.prod(matching_cost), GRB.MINIMIZE)
model.setObjective(sum(assign[c,f]*setup_cost[f] for c in range(num_bookings) for f in range(num_pickup_stations))+ sum(250*assign[c,f]*matching_cost[c,f] for c in range(num_bookings) for f in range(num_pickup_stations)), GRB.MINIMIZE)


model.optimize()


#♦ Analysis

# Data generation for part II
total_construction_cost = 0
counter = 0
for customer in range(num_bookings):
    for station in range(num_pickup_stations):
        if (assign[customer, station].X):
            counter = counter + 1
            print(f"\n Pickup station at location", station + 1, "will receive customers.")
            total_construction_cost = total_construction_cost + setup_cost[station]
            print(f"\n Booking", customer + 1,  "will go to station", station + 1)
print('Total number of bookings served:', counter)
print('Total distance to walk (in meters):', float(model.objVal)-total_construction_cost)

num_stations_active = 0
for station in range(num_pickup_stations):
    if sum(assign[:, station].X):
        num_stations_active = num_stations_active + 1
print('Total number of stations open:', num_stations_active, " out of", num_pickup_stations)

# timeslot is 7h*60 + Timeslot*60
# the idea is to add the data we took from here to the big data file:
"#1 - Add bookings into a new dict"
bookings = []
booking = {
    "id": [],
    "price": [],  # each booking is worth 1000
    "passengers": [],  # sum of all bookings going to this station
    "maximumDuration": [],  # min of all max durations of bookings
    "old_location": [],
    "jobs":
            {
                "duration": 60,
                "station": [],
                "timewindow": [],  # timeslot is 7h*60 + Timeslot*60 and can be picked up 2 hours before the timelimit (-120)
            },
}

"#2 - Introduce data from this script to the new dict"
"#2.1 get range of timeslots available"
timeslots = np.zeros(num_bookings)
for booking in range(num_bookings):
    timeslots[booking] = distance_limit[booking] = data_bookings[booking]["jobs"][0]["timeslot"]

timeslots = list(dict.fromkeys(timeslots))
for station in range(num_pickup_stations):
    for ts in timeslots:
        append = False
        price = 0
        passengers = 0
        maximumduration = []
        old_location = []
        t1 = ts * 60 + 7 * 60
        t0 = t1 - 120
        for customer in range(num_bookings):
            if assign[customer, station].X:
                if data_bookings[customer]["jobs"][0]["timeslot"] == ts:
                    append = True
                    id = data_bookings[customer]["id"]  # we will just add any id
                    price = price + 1000
                    passengers = passengers + data_bookings[customer]["passengers"]
                    maximumduration.append(data_bookings[customer]["maximumDuration"])
                    old_location.append(data_bookings[customer]["jobs"][0]["location"])
        if append:
            booking = {
                "id": id,
                "price": price,  # each booking is worth 1000
                "passengers": passengers,  # sum of all bookings going to this station
                "maximumDuration": min(maximumduration),  # min of all max durations of bookings
                "old_location": old_location,
                "jobs":
                    {
                        "duration": 2,
                        "station": ["s" + str(station), "s" + str(num_pickup_stations-2)],  # because we remove the depot stations
                        "timewindow": [t0, t1],
                    },
            }
            bookings.append(booking)


"#3 - put data into a .json file"

with open("data/data_generated/bookings_part2.json", "w") as write_file:
    json.dump(bookings, write_file, indent=4)
