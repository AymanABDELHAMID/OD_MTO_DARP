"""
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
            if 2 <= i <= bookings_n + 1:
                # I think here you need to convert to int...
                depart = int(data["bookings"][i - 1]["jobs"][1]["station"][2:-1])
            elif bookings_n + 2 <= i <= 2 * bookings_n + 1:
                depart = data["bookings"][i - 1 - bookings_n]["jobs"][2]["station"][2:-1]
            elif i == 1:
                depart = 0
            elif i == 2 * bookings_n + 2:
                depart = 0









# Create initial model
model = gp.Model('DARP')


