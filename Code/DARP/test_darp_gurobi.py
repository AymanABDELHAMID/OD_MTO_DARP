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
