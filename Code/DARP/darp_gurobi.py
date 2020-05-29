"""
Mai 2020 - Ayman Mahmoud
--------------------------------------------
This is a small darp problem solved using
data used is from YUSO and has been given to us
then the model is going to be modified to
accommodate the new mathematical formulation
in the course of Optimization of Passenger Transport systems

"""

import numpy as np, csv, random, operator
import json
import pandas
from operator import itemgetter
import copy
import matplotlib.pyplot as plt
import time
import gurobipy as gp
from gurobipy import GRB

# adding type hint to the dict
data = dict

with open('data/Data_Yuso-20200302/day_data.json') as f:
    data = json.load(f)
bookings = data["bookings"]
shifts = data["shifts"]
df = pandas.read_csv("data/Data_Yuso-20200302/travel_times.csv", sep=";")
travel_times = df.set_index('Unnamed: 0').to_numpy()
bookings_n = len(bookings)
shifts_n = len(shifts)

price = np.zeros((bookings_n))
for i in range(bookings_n):
    price[i] = data["bookings"][i]["price"]

cost = np.zeros((2*bookings_n+2,2*bookings_n+2,shifts_n))

for l in range(shifts_n):
    for i in range(bookings_n):
        for j in range(bookings_n):
            if 1 <= i <= bookings_n:
                # I think here you need to convert to int...
                depart = int(data["bookings"][i - 1]["jobs"][0]["station"][1:])
            elif bookings_n + 1 <= i <= 2 * bookings_n:
                depart = int(data["bookings"][i - 1 - bookings_n]["jobs"][1]["station"][1:])
            elif i == 0:
                depart = 0
            elif i == 2 * bookings_n + 1:
                depart = 0

            if 1 <= j <= bookings_n:
                arrive = int(data["bookings"][j - 1]["jobs"][0]["station"][1:])
            elif bookings_n + 1 <= j <= 2 * bookings_n:
                arrive = int(data["bookings"][j - 1 - bookings_n]["jobs"][1]["station"][1:])
            elif j == 0:
                arrive = 0
            elif j == 2 * bookings_n + 1:
                arrive = 0

            cost[i, j, l] = travel_times[depart + 1, arrive + 1]  # verify if indices are correct

# Create initial model
model = gp.Model('DARP')

"1. add model variables"
# Initialize decision variables for ground set:
# x[i,j,k] == 1 if driver k is chosen for the trip i to j.
x = model.addMVar(shape=(2*bookings_n+2,2*bookings_n+2,shifts_n), vtype=GRB.BINARY, name='x')

# u[i] is the variable for
u = model.addMVar(shape=(2*bookings_n), vtype=GRB.INTEGER, name='u')

# v[] time at which station at booking i is served by driver k
v = model.addMVar(shape=(shifts_n,2), vtype=GRB.INTEGER, name='v')

# w[] is a variable for n. of passenger in vehicle when reaching booking i
w = model.addMVar(shape=(2*bookings_n+2), vtype=GRB.INTEGER, name='w')

# r[] is a variable for time of the trip of booking i
r = model.addMVar(shape=(bookings_n), vtype=GRB.INTEGER, name='r')

"""
FYI:
 addVar (adds a new variable), 
 addVars (adds multiple new variables), 
 addMVar (adds an a NumPy ndarray of Gurobi variables)
"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

"2. add model constraints"
# m.addConstr(A @ x <= rhs, name="c")
"explore this part further to create an addMConstraint"
model.addConstrs((sum(x[i, :, :]) <= 1 for i in range(1,bookings_n)), name="c1") # not sure if it should be == or <=

model.addConstrs((sum(x[1, :, l]) == 1 for l in range(shifts_n)), name="c2")  # départ du dépot
model.addConstrs((sum(x[1, 2*bookings_n+1, l]) == 1 for l in range(shifts_n)), name="c3")  # retour au dépot
model.addConstrs((v[l,1] <= data["shifts"][l]["jobs"][1]["timeDate"] for l in range(shifts_n)), name="c4")  # respect des shifts
model.addConstrs((v[l,0] >= data["shifts"][l]["jobs"][0]["timeDate"] for l in range(shifts_n)), name="c5")  # respect des shifts

model.addConstrs((sum(x[i, :, l]) - sum(x[i+bookings_n,:,l]) == 0 for i in range(1, bookings_n+1)
                                                               for l in range(shifts_n)), name="c6")  # you can also add if i != j
model.addConstrs((sum(x[:, i, l]) - sum(x[i,:,l]) == 0 for i in range(1, bookings_n+1)
                                                               for l in range(shifts_n)), name="c7")
model.addConstrs((sum(x[:,i+bookings_n,l]) - sum(x[i+bookings_n,:,l]) == 0 for i in range(1, bookings_n+1)
                                                               for l in range(shifts_n)), name="c8")

"""
Here you will add the linearized big M and big W constraints
"""

# duration = data["bookings"][:]["jobs"][0]["duration"] - duration[i-1]
model.addConstrs((r[i-1] == u[bookings_n+i-1] - u[i-1] - 60 for i in range(1,bookings_n+1)), name="c9")  # respect des shifts

# The objective is to minimize the total distance travelled
#model.setObjective(sum(x*cost), GRB.MINIMIZE)
#model.setObjective(x.prod(cost), GRB.MINIMIZE)  # sum(np.multiply(x,cost))
#model.setObjective(sum(cost[:, j, k] @ x[:, j, k] for j in range(n)), GRB.MINIMIZE)
#model.setObjective(cost @ x.sum(), GRB.MINIMIZE)
model.setObjective(sum(cost[:,j,k] @ x[:, j,k] for k in range(shifts_n)
                       for j in range(2*bookings_n+2)), GRB.MINIMIZE)  # I am definite this is the correct one
# save a linear programming model
#model.write('DARP.lp')

# optimize model
model.optimize()
print('Objective value: %g' % model.objVal)


