"""
In this script we are going to use p-median
method to solve the station allocation problem

v0 : static input data treating a single timeslot
"""

import gurobipy as gp
from gurobipy import GRB
import random
from itertools import product
from math import sqrt

# Parameters


graph_size = 50
booking_number = 50
# Generate bookings within the graph limit needs a fix with numpy to plot
original_values = range(0, graph_size)
bookings = [(random.choice(original_values), random.choice(original_values))
            for _ in range(booking_number)]
# you can also define the station distances and generate all possible permutations
pickup_stations = [(0, 0), (0, 15), (0, 30), (0, 45), (15, 0), (15, 15), (15, 30), (30, 0),
(15, 45), (30, 15), (30, 30), (30, 45), (45, 0), (45, 15), (45,30), (45, 45)]


cost_per_step = 1

# This function determines the Euclidean distance between a pickup station and booking location.


def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)

# Compute key parameters of MIP model formulation


num_pickup_stations = len(pickup_stations)
num_bookings = len(bookings)
cartesian_prod = list(product(range(num_bookings), range(num_pickup_stations)))

# Compute shipping costs

matching_cost = {(c, f): cost_per_step*compute_distance(bookings[c], pickup_stations[f]) for c, f in cartesian_prod}
# this is a list containing all bookings with the corresponding cost to each station so the size of it
# is equal to num_bookings*num_pickup_stations


# MIP  model formulation

m = gp.Model('pickup_stations')

select = m.addVars(num_pickup_stations, vtype=GRB.BINARY, name='Select')
assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

m.addConstrs((assign[(c, f)] <= select[f] for c, f in cartesian_prod), name='Numbers')
m.addConstrs((gp.quicksum(assign[(c, f)] for f in range(num_pickup_stations)) == 1 for c in range(num_bookings)), name='serveOnce')

# Save model
m.write('pickup_pmedian_v1.lp')

m.setObjective(assign.prod(matching_cost), GRB.MINIMIZE)

m.optimize()

#♦ Analysis

for facility in select.keys():
    if abs(select[facility].x) > 1e-6:
        print(f"\n Pickup station at location {facility + 1} will receive customers.")
"""
for customer, facility in assign.keys():
    if abs(assign[customer, facility].x) > 1e-6:
        print(f"\n Booking {customer + 1} will be picked up from station {facility + 1}.")
"""
"""
- We can't serve a customer from 2 stations
- We want to minimize the number of stations
- We want to add capacity limit to each station
"""