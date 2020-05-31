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
import matplotlib.pyplot as plt
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

price = np.zeros(bookings_n)
for i in range(bookings_n):
    price[i] = data["bookings"][i]["price"]

cost = np.zeros((2*bookings_n+2,2*bookings_n+2,shifts_n))

for l in range(shifts_n):
    for i in range(2*bookings_n+2):
        for j in range(2*bookings_n+2):
            if 1 <= i <= bookings_n:
                depart = int(data["bookings"][i - 1]["jobs"][0]["station"][1:])
            elif bookings_n + 1 <= i <= 2 * bookings_n:
                depart = int(data["bookings"][i - 1 - bookings_n]["jobs"][1]["station"][1:])
            elif i == 0:
                depart = 0
            elif i == 2 * bookings_n + 1:
                depart = 0
            else:
                depart = None

            if 1 <= j <= bookings_n:
                arrive = int(data["bookings"][j - 1]["jobs"][0]["station"][1:])
            elif bookings_n + 1 <= j <= 2 * bookings_n:
                arrive = int(data["bookings"][j - 1 - bookings_n]["jobs"][1]["station"][1:])
            elif j == 0:
                arrive = 0
            elif j == 2 * bookings_n + 1:
                arrive = 0
            else:
                arrive = None

            cost[i, j, l] = travel_times[depart, arrive]  # [depart + 1, arrive + 1]

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
model.addConstrs((sum(x[i, :, :]) <= 1 for i in range(1,bookings_n)), name="c1")  # not sure if it should be == or <=

model.addConstrs((sum(x[1, :, l]) == 1 for l in range(shifts_n)), name="c2")  # départ du dépot
model.addConstrs((sum(x[:, 2*bookings_n+1, l]) == 1 for l in range(shifts_n)), name="c3")  # retour au dépot # found an error here 1 instead of :
model.addConstrs((v[l,1] <= data["shifts"][l]["jobs"][1]["timeDate"] for l in range(shifts_n)), name="c4")  # respect des shifts
model.addConstrs((v[l,0] >= data["shifts"][l]["jobs"][0]["timeDate"] for l in range(shifts_n)), name="c5")  # respect des shifts

model.addConstrs((sum(x[i, :, l]) - sum(x[i+bookings_n, :, l]) == 0 for i in range(1, bookings_n)  # found error #2 bookings_n + 1 instead of bookings_n
                                                               for l in range(shifts_n)), name="c6")  # you can also add if i != j
model.addConstrs((sum(x[:, i, l]) - sum(x[i, :, l]) == 0 for i in range(1, bookings_n)  # same error #2
                                                               for l in range(shifts_n)), name="c7")
model.addConstrs((sum(x[:,i+bookings_n,l]) - sum(x[i+bookings_n, :, l]) == 0 for i in range(1, bookings_n)  # same error #2
                                                               for l in range(shifts_n)), name="c8")

"Linearisation"


M = np.zeros((2*bookings_n+2,2*bookings_n+2))

for i in range(2*bookings_n+2):
    for j in range(2*bookings_n+2):
        if 1 <= i <= bookings_n:
            d = data["bookings"][i - 1]["jobs"][0]["duration"]
        elif bookings_n + 1 <= i <= 2 * bookings_n:
            d = data["bookings"][i - bookings_n - 1]["jobs"][1]["duration"]
        elif i == 0:
            d = 0
        elif i == 2 * bookings_n + 1:
            d = 0

        if 1 <= i <= bookings_n:
            depart = int(data["bookings"][i - 1]["jobs"][0]["station"][1:])
        elif bookings_n + 1 <= i <= 2 * bookings_n:
            depart = int(data["bookings"][i - 1 - bookings_n]["jobs"][1]["station"][1:])
        elif i == 0:
            depart = 0
        elif i == 2 * bookings_n + 1:
            depart = 0

        if 1 <= j <= bookings_n:
            arrive = int(data["bookings"][j - 1]["jobs"][0]["station"][1:])
        elif bookings_n+1 <= j <= 2*bookings_n:
            arrive = int(data["bookings"][j - 1 - bookings_n]["jobs"][1]["station"][1:])
        elif j == 0:
            arrive = 0
        elif j == 2*bookings_n + 1:
            arrive = 0

        if 1 <= j <= bookings_n:  # found error #3   2 instead of 1
            begin_date = data["bookings"][j-1]["jobs"][0]["timeWindowBeginDate"]
        elif bookings_n + 1 <= j <= 2*bookings_n:
            begin_date = data["bookings"][j-1-bookings_n]["jobs"][1]["timeWindowBeginDate"]
        elif j == 0:
            begin_date = 31200  # this is an evaluation code but don't put fixed numbers in general
        elif j == 2*bookings_n+1:
            begin_date = 31200

        if 1 <= i <= bookings_n:
            end_date = data["bookings"][i-1]["jobs"][0]["timeWindowEndDate"]
        elif bookings_n+1 <= i <= 2*bookings_n:
            end_date = data["bookings"][i-1-bookings_n]["jobs"][1]["timeWindowEndDate"]
        elif i == 0:
            end_date = 64548  # same here, fait gaffe !
        elif i == 2*bookings_n+1:
            end_date = 64548

        M[i, j] = max(0, (end_date + travel_times[depart, arrive] + d - begin_date))

        for l in range(shifts_n):
            if 1 <= i <= 2*bookings_n:
                if 1 <= j <= 2*bookings_n:
                    model.addConstr(u[j-1] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm1"+str(250+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm2"+str(50+j))
                elif j == 2*bookings_n+1:
                    model.addConstr(v[l,1] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm3")  # found error # 4 depart + 1 instead of depart
            elif i == 0:
                if 1 <= j <= 2*bookings_n:
                    model.addConstr(u[j-1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm4"+str(l+50+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm5")
                elif j == 2*bookings_n+1:
                    model.addConstr(v[l,1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm6")
            elif i == 2*bookings_n+1:
                if 1 <= j <= 2*bookings_n:
                    model.addConstr(u[j-1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm7")
                elif j == 0: # found error number 5 1 instead of 0
                    model.addConstr(v[l,0] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm8")
                elif j == 2*bookings_n+1:
                    model.addConstr(v[l,1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm9")

W = np.zeros((2*bookings_n+2,2*bookings_n+2))

capacity = data["shifts"][0]["capacity"]  # because in this problem the capacity is the same

for i in range(2*bookings_n+2):
    for j in range(2*bookings_n+2):
        if 1 <= i <= bookings_n:
            q_i = data["bookings"][i-1]["passengers"]
        elif bookings_n+1 <= i <= 2*bookings_n:
            q_i = -data["bookings"][i-1-bookings_n]["passengers"]
        elif i == 0:
            q_i = 0
        elif i == 2*bookings_n+1:
            q_i = 0

        if 1 <= j <= bookings_n:
            q_j = data["bookings"][j-1]["passengers"]
        elif bookings_n+1 <= j <= 2*bookings_n:
            q_j = -data["bookings"][j-1-bookings_n]["passengers"]
        elif j == 0:
            q_j = 0
        elif j == 2*bookings_n+1:
            q_j = 0


        W[i,j] = min(capacity, capacity + q_i)
        for l in range(shifts_n):
            model.addConstr(w[j] >= w[i] + q_j - W[i, j]*(1 - x[i, j, l]), name="cw1"+str(2*l))
# duration = data["bookings"][:]["jobs"][0]["duration"] - duration[i-1]=
model.addConstrs((r[i-1] == u[bookings_n+i-1] - u[i-1] - 60 for i in range(1, bookings_n)), name="c9")  # respect des shifts found error # 6 bookings_n + 1

for i in range(2*bookings_n+2):
    if 1 <= i <= bookings_n:
        q = data["bookings"][i-1]["passengers"]
    elif bookings_n+1 <= i <= 2*bookings_n:
        q = -data["bookings"][i-1-bookings_n]["passengers"]
    elif i == 0:
        q = 0
    elif i == 2*bookings_n+1:
        q = 0

    if q >= 0:
        model.addConstr(q <= w[i], name="c10l")
        model.addConstr(w[i] <= capacity, name="c10r")
    else:
        model.addConstr(0 <= w[i], name="c11l")
        model.addConstr(w[i] <= capacity + q, name="c11r")


for i in range(2*bookings_n+2):
    if 1 <= i <= bookings_n:
        begin_date = data["bookings"][i-1]["jobs"][0]["timeWindowBeginDate"]
        end_date = data["bookings"][i-1]["jobs"][0]["timeWindowEndDate"]
        model.addConstr(begin_date <= u[i-1], name="c12l")
        model.addConstr(u[i - 1] <= end_date, name="c12r")
    elif bookings_n+1 <= i <= 2*bookings_n:
        begin_date = data["bookings"][i-1-bookings_n]["jobs"][1]["timeWindowBeginDate"]
        end_date = data["bookings"][i-1-bookings_n]["jobs"][1]["timeWindowEndDate"]
        model.addConstr(begin_date <= u[i-1], name="c13l")
        model.addConstr(u[i - 1] <= end_date, name="c13r")

for i in range(1, bookings_n):
    depart = int(data["bookings"][i - 1]["jobs"][0]["station"][1:])
    arrive = int(data["bookings"][i - 1]["jobs"][1]["station"][1:])
    L = data["bookings"][i-1]["maximumDuration"]
    model.addConstr(travel_times[depart,arrive] <= r[i-1], name="c14_1")
    model.addConstr(r[i - 1] <= L, name="c14_2")

for i in range(1,2*bookings_n+2):
    model.addConstr(sum(x[i,i,:])==0, name="c15")

model.addConstr(sum(x[2*bookings_n+1, :, :]) == 0, name="c16")

for l in range(shifts_n):
    model.addConstr(sum(price[i] * x[i + 1, j, l] for i in range(bookings_n)
        for j in range(2 * bookings_n + 2)) <= 6000, name = 'c'+str(l+16))   # respect the max revenue


# The objective is to minimize the total distance travelled
#model.setObjective(sum(x*cost), GRB.MINIMIZE)
#model.setObjective(x.prod(cost), GRB.MINIMIZE)  # sum(np.multiply(x,cost))
#model.setObjective(sum(cost[:, j, k] @ x[:, j, k] for j in range(n)), GRB.MINIMIZE)
#model.setObjective(cost @ x.sum(), GRB.MINIMIZE)
#model.setObjective(sum(cost[:,j,k] @ x[:, j,k] for k in range(shifts_n)
#                       for j in range(2*bookings_n+2)), GRB.MINIMIZE)  # I am definite this is the correct one
model.setObjective(sum(cost[i,j,l] * x[i, j,l] for i in range(2 * bookings_n + 2)
                                               for j in range(2 * bookings_n + 2)
                                               for l in range(shifts_n)), GRB.MINIMIZE)

# save a linear programming model
model.write('DARP/DARP.lp')

# optimize model
model.optimize()
print('Objective value: %g' % model.objVal)


