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


# map timeslot here, it won't affect the distances
