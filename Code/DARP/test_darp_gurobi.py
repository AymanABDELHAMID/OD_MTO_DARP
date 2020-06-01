"""
Testing Gurobi Functionalities:
the problem I had to fix is:
 1-D MVar objects, viz., A @ x.
 basically we cannot optimize and n-D array id n > 1, this is why the objective function
 has to be linearized.
 The test was successful.
"""


import gurobipy as gp
from gurobipy import GRB

import numpy as np

m = 25
n = 25
z = 8
cost = np.zeros((2*m+2,2*n+2,z))


model = gp.Model()
X = model.addMVar((2*m+2,2*n+2,z))
a = np.random.rand(2*m+2)
b = np.random.rand(2*n+2)
c = np.random.rand(z)

# Set objective to a @ X @ b
model.setObjective(sum(cost[:,j,k] @ X[:, j,k] for k in range(z)
                       for j in range(n)), GRB.MINIMIZE)

"""

"--------------------------------------------------------------------------"
"Linearization Part"
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
                    model.addConstr(v[l,1] >= u[i-1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm3")
            elif i == 0:
                if 1 <= j <= 2*num_bookings:
                    model.addConstr(u[j-1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm4"+str(l+50+j))
                elif j == 0:
                    model.addConstr(v[l,0] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm5")
                elif j == 2*num_bookings+1:
                    model.addConstr(v[l,1] >= v[l,0] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm6")
            elif i == 2*num_bookings+1:
                if 1 <= j <= 2*num_bookings:
                    model.addConstr(u[j-1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm7")
                elif j == 0:
                    model.addConstr(v[l,0] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm8")
                elif j == 2*num_bookings+1:
                    model.addConstr(v[l,1] >= v[l,1] + d + travel_times[depart,arrive] - M[i,j]*(1 - x[i,j,l]),name="cm9")

"---------------------------------------------------------------------------"
"""