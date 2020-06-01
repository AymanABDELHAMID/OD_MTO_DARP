"""
Ayman Mahmoud - Mai 2020
--------------------------------------------
This script takes the output of part 1 from the problem definition
and runs the second part to optimize the driver allocation problem.
"""

import numpy as np, csv, random, operator
import json
import pandas
import matplotlib.pyplot as plt
import gurobipy as gp
from gurobipy import GRB


# Get booking data
# adding type hint to the dict
with open('data/data_generated/bookings_part2.json') as f:
    data_bookings = json.load(f)

# Get Shifts data
with open('data/data_generated/shifts.json') as f:
    data_shifts = json.load(f)

# get Travel Times Data
df = pandas.read_csv("data/data_generated/travel_times.csv", sep=",")
travel_times = df.set_index('Unnamed: 0').to_numpy()

# Compute key parameters of MIP model formulation
num_bookings = len(data_bookings)
num_shifts = len(data_shifts)

cost = np.zeros((2*num_bookings+2,2*num_bookings+2,num_shifts))

for l in range(num_shifts):
    for i in range(2*num_bookings+2):
        for j in range(2*num_bookings+2):
            if 1 <= i <= num_bookings:
                depart = int(data_bookings[i - 1]["jobs"]["station"][0][1:])
            elif num_bookings + 1 <= i <= 2 * num_bookings:
                depart = int(data_bookings[i - 1 - num_bookings]["jobs"]["station"][1][1:])
            elif i == 0:
                depart = 0
            elif i == 2 * num_bookings + 1:
                depart = 0
            else:
                depart = None

            if 1 <= j <= num_bookings:
                arrive = int(data_bookings[j - 1]["jobs"]["station"][0][1:])
            elif num_bookings + 1 <= j <= 2 * num_bookings:
                arrive = int(data_bookings[j - 1 - num_bookings]["jobs"]["station"][0][1:])
            elif j == 0:
                arrive = 0
            elif j == 2 * num_bookings + 1:
                arrive = 0
            else:
                arrive = None

            cost[i, j, l] = travel_times[depart, arrive]  # [depart + 1, arrive + 1]


# Create initial model
model = gp.Model('DARP')

"1. add model variables"
# Initialize decision variables for ground set:
# x[i,j,k] == 1 if driver k is chosen for the trip i to j.
x = model.addMVar(shape=(2*num_bookings+2,2*num_bookings+2,num_shifts), vtype=GRB.BINARY, name='x')

# u[i] is the variable for
u = model.addMVar(shape=(2*num_bookings), vtype=GRB.INTEGER, name='u')

# v[] time at which station at booking i is served by driver k
v = model.addMVar(shape=(num_shifts,2), vtype=GRB.INTEGER, name='v')

# w[] is a variable for n. of passenger in vehicle when reaching booking i
w = model.addMVar(shape=(2*num_bookings+2), vtype=GRB.INTEGER, name='w')

# r[] is a variable for time of the trip of booking i
r = model.addMVar(shape=(num_bookings), vtype=GRB.INTEGER, name='r')



"2. add model constraints"
"we need to make sure that each pickup is assured only once by the same vehicle"
model.addConstrs((x[i, :, :].sum() == 1 for i in range(1,num_bookings + 1)), name="c1")  # not sure if it should be == or <=

"make sure that each trip starts and end at s0"
model.addConstrs((x[0, :, l].sum() == 1 for l in range(num_shifts)), name="c2")  # départ du dépot, not 1 it should be 0
model.addConstrs((x[:, 2*num_bookings+1, l].sum() == 1 for l in range(num_shifts)), name="c3")  # retour au dépot

"respect the shifts"
model.addConstrs((v[l,1] <= data_shifts[l]["jobs"][0]["TimeWindow"][1] for l in range(num_shifts)), name="c4")  # respect des shifts
model.addConstrs((v[l,0] >= data_shifts[l]["jobs"][0]["TimeWindow"][0] for l in range(num_shifts)), name="c5")  # respect des shifts

model.addConstrs((x[i, :, l].sum() - x[i+num_bookings, :, l].sum() == 0 for i in range(1, num_bookings + 1)
                                                               for l in range(num_shifts)), name="c6")  # you can also add if i != j
model.addConstrs((x[:, i, l].sum() - x[i, :, l].sum() == 0 for i in range(1, num_bookings + 1)
                                                               for l in range(num_shifts)), name="c7")
model.addConstrs((x[:,i+num_bookings,l].sum() - x[i+num_bookings, :, l].sum() == 0 for i in range(1, num_bookings + 1)
                                                               for l in range(num_shifts)), name="c8")

"Linearization : "
M = np.zeros((2*num_bookings+2,2*num_bookings+2))

for i in range(2*num_bookings+2):
    for j in range(2*num_bookings+2):
        if 1 <= i <= num_bookings:
            d = data_bookings[i - 1]["jobs"]["duration"]
        elif num_bookings + 1 <= i <= 2 * num_bookings:
            d = data_bookings[i - num_bookings - 1]["jobs"]["duration"]
        elif i == 0:
            d = 0
        elif i == 2 * num_bookings + 1:
            d = 0

        if 1 <= i <= num_bookings:
            depart = int(data_bookings[i - 1]["jobs"]["station"][0][1:])
        elif num_bookings + 1 <= i <= 2 * num_bookings:
            depart = int(data_bookings[i - 1 - num_bookings]["jobs"]["station"][1][1:])
        elif i == 0:
            depart = 0
        elif i == 2 * num_bookings + 1:
            depart = 0

        if 1 <= j <= num_bookings:
            arrive = int(data_bookings[j - 1]["jobs"]["station"][0][1:])
        elif num_bookings+1 <= j <= 2*num_bookings:
            arrive = int(data_bookings[j - 1 - num_bookings]["jobs"]["station"][1][1:])
        elif j == 0:
            arrive = 0
        elif j == 2*num_bookings + 1:
            arrive = 0

        if 1 <= j <= num_bookings:
            begin_date = data_bookings[j-1]["jobs"]["timewindow"][0]
        elif num_bookings + 1 <= j <= 2*num_bookings:
            begin_date = data_bookings[j-1-num_bookings]["jobs"]["timewindow"][1] - 30
        elif j == 0:
            begin_date = data_shifts[0]["jobs"][0]["TimeWindow"][0]
        elif j == 2*num_bookings+1:
            begin_date = data_shifts[0]["jobs"][0]["TimeWindow"][0]

        if 1 <= i <= num_bookings:
            end_date = data_bookings[i-1]["jobs"]["timewindow"][0] + 30
        elif num_bookings+1 <= i <= 2*num_bookings:
            end_date = data_bookings[i-1-num_bookings]["jobs"]["timewindow"][1]
        elif i == 0:
            end_date = data_shifts[0]["jobs"][0]["TimeWindow"][1]  # same here, fait gaffe !
        elif i == 2*num_bookings+1:
            end_date = data_shifts[0]["jobs"][0]["TimeWindow"][1]

        M[i, j] = max(0, (end_date + travel_times[depart, arrive] + d - begin_date))

        for l in range(num_shifts):
            if 1 <= i <= 2*num_bookings:
                if 1 <= j <= 2*num_bookings:
                    model.addConstr(u[j-1] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm1"+str(250+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm2"+str(50+j))
                elif j == 2*num_bookings+1:
                    model.addConstr(v[l,1] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm3"+str(350+j))
            elif i == 0:
                if 1 <= j <= 2*num_bookings:
                    model.addConstr(u[j-1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm4"+str(l+50+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm5"+str(l+50+j))
                elif j == 2*num_bookings+1:
                    model.addConstr(v[l,1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm6"+str(l+50+j))
            elif i == 2*num_bookings+1:
                if 1 <= j <= 2*num_bookings:
                    model.addConstr(u[j-1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm7"+str(l+50+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm8"+str(l+50+j))
                elif j == 2*num_bookings+1:
                    model.addConstr(v[l,1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm9"+str(l+50+j))


W = np.zeros((2*num_bookings+2,2*num_bookings+2))

capacity = data_shifts[0]["capacity"]  # because in this problem the capacity is the same

for i in range(2*num_bookings+2):
    for j in range(2*num_bookings+2):
        if 1 <= i <= num_bookings:
            q_i = data_bookings[i-1]["passengers"]
        elif num_bookings+1 <= i <= 2*num_bookings:
            q_i = -data_bookings[i-1-num_bookings]["passengers"]
        elif i == 0:
            q_i = 0
        elif i == 2*num_bookings+1:
            q_i = 0

        if 1 <= j <= num_bookings:
            q_j = data_bookings[j-1]["passengers"]
        elif num_bookings+1 <= j <= 2*num_bookings:
            q_j = -data_bookings[j-1-num_bookings]["passengers"]
        elif j == 0:
            q_j = 0
        elif j == 2*num_bookings+1:
            q_j = 0


        W[i,j] = min(capacity, capacity + q_i)
        for l in range(num_shifts):
            model.addConstr(w[j] >= w[i] + q_j - W[i, j]*(1 - x[i, j, l]), name="cw1"+str(2*l))

model.addConstrs((r[i-1] == u[num_bookings+i-1] - u[i-1] - 2 for i in range(1, num_bookings+1)), name="c9")


capacity = data_shifts[0]["capacity"]  # because in this problem the capacity is the same
for i in range(2*num_bookings+2):
    if 1 <= i <= num_bookings:
        q = data_bookings[i-1]["passengers"]
    elif num_bookings+1 <= i <= 2*num_bookings:
        q = -data_bookings[i-1-num_bookings]["passengers"]
    elif i == 0:
        q = 0
    elif i == 2*num_bookings+1:
        q = 0

    if q >= 0:
        model.addConstr(q <= w[i], name="c10n" + str(i))
        model.addConstr(w[i] <= capacity, name="c10r" + str(i))
    else:
        model.addConstr(0 <= w[i], name="c11l" + str(i))
        model.addConstr(w[i] <= capacity + q, name="c11r" + str(i))

for i in range(2*num_bookings+2):
    if 1 <= i <= num_bookings:
        begin_date = data_bookings[i-1]["jobs"]["timewindow"][0]
        end_date = begin_date + 30
        model.addConstr(begin_date <= u[i-1], name="c12l" + str(i))
        model.addConstr(u[i - 1] <= end_date, name="c12r" + str(i))
    elif num_bookings+1 <= i <= 2*num_bookings:
        begin_date = data_bookings[i-1-num_bookings]["jobs"]["timewindow"][1] - 30  # the client can arrive up to 30min early
        end_date = begin_date + 30
        model.addConstr(begin_date <= u[i-1], name="c13l" + str(i))
        model.addConstr(u[i - 1] <= end_date, name="c13r" + str(i))


for i in range(1, num_bookings+1):
    depart = int(data_bookings[i - 1]["jobs"]["station"][0][1:])
    arrive = int(data_bookings[i - 1]["jobs"]["station"][1][1:])
    L = data_bookings[i-1]["maximumDuration"]
    model.addConstr(travel_times[depart,arrive] <= r[i-1], name="c14_1"+ str(i))
    model.addConstr(r[i - 1] <= L, name="c14_2"+ str(i))

for i in range(2*num_bookings+2):  # found another error here in for loop
    model.addConstr(sum(x[i, i, :]) == 0, name="c15")  # no need to do do [].sum() because the result here is correct

model.addConstr(x[2*num_bookings+1, :, :].sum() == 0, name="c16")

"Price vector"
price = np.zeros(num_bookings)
for i in range(num_bookings):
    price[i] = data_bookings[i]["price"]


for l in range(num_shifts):
    model.addConstr(sum(price[i] * x[i + 1, j, l] for i in range(num_bookings)
        for j in range(2 * num_bookings + 2)) <= 20000, name = 'c'+str(l+26))   # respect the max revenue

#model.setObjective(sum(cost[:,j,k] @ x[:, j,k] for k in range(num_shifts)
#                          for j in range(2*num_bookings+2)), GRB.MINIMIZE)

from itertools import product

shape = list(product(range(2*num_bookings+2), range(2*num_bookings+2),range(num_shifts)))
model.setObjective(sum(x[i, j, k]*cost[i, j, k] for i, j, k in shape))


# save a linear programming model
model.write('DARP/DARP_part2.lp')

# optimize model
model.optimize()
print('Objective value: %g' % model.objVal)

# Data analysis