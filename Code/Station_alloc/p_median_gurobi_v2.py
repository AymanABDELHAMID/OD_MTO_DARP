"""
In this script we are going to use p-median
method to solve the station allocation problem

v2 : constraints are modified to introduce the user distance limit "dl"
"""
from itertools import product
from math import sqrt
import random

import gurobipy as gp
from gurobipy import GRB

# tested with Gurobi v9.0.0 and Python 3.7.0

# Parameters
graph_size = 50
booking_number = 25
# Generate bookings within the graph limit needs a fix with numpy to plot
original_values = range(0, graph_size)
bookings = [(random.choice(original_values), random.choice(original_values))
            for _ in range(booking_number)]  # customers
# you can also define the station distances and generate all possible permutations
pickup_stations = [(0, 0), (0, 15), (0, 30), (0, 45), (15, 0), (15, 15), (15, 30), (30, 0),
(15, 45), (30, 15), (30, 30), (30, 45), (45, 0), (45, 15), (45,30), (45, 45)]  # facilities

setup_cost = [3, 2, 3, 1, 3, 3, 4, 3, 2, 3, 2, 3, 1, 3, 3, 4]
cost_per_step = 1

# This function determines the Euclidean distance between a facility and customer sites.

def compute_distance(loc1, loc2):
    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(dx*dx + dy*dy)

# Compute key parameters of MIP model formulation


num_stations = len(pickup_stations)
num_bookings = len(bookings)
cartesian_prod = list(product(range(num_bookings), range(num_stations)))

# Compute shipping costs

shipping_cost = {(c,f): cost_per_step*compute_distance(bookings[c], pickup_stations[f]) for c, f in cartesian_prod}


# MIP  model formulation

m = gp.Model('pickup_stations')

select = m.addVars(num_stations, vtype=GRB.BINARY, name='Select')
assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

m.addConstrs((assign[(c,f)] <= select[f] for c,f in cartesian_prod), name='Setup2ship')
m.addConstrs((gp.quicksum(assign[(c,f)] for f in range(num_stations)) == 1 for c in range(num_bookings)), name='Demand')

m.setObjective(select.prod(setup_cost)+assign.prod(shipping_cost), GRB.MINIMIZE)

m.optimize()

"""
- We can't serve a customer from 2 stations
- We want to minimize the number of stations
- We want to add capacity limit to each station
"""

# display optimal values of decision variables

for facility in select.keys():
    if (abs(select[facility].x) > 1e-6):
        print(f"\n open station at {facility + 1}.")

"""
for customer, facility in assign.keys():
    if (abs(assign[customer, facility].x) > 1e-6):
        print(f"\n Supermarket {customer + 1} recieves from Warehouse {facility + 1} "
              f"{round(100*assign[customer, facility].x, 2)} % of its demand.")
"""

# mapping to the bookings I have
