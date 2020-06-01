"""
May 2020 - Ayman Mahmoud
----------------------------------------
This module generates a table (matrix) of all travel times between stations and to destinations
Distance between pickup stations will be used in the future when a vehicle can operate on multiple pickups
before reaching the final destination.

Distance between each node on a horizontal or vertical line in 500 meters.
Travel time is calculated by measuring the distance between two stations over speed
Speed in this problem is considered to be 20km/h. This speed represents the average speed of a vehicle
later on the speed is going to be based on each vehicle's average speed.
"""

import json
from math import sqrt
import numpy as np
import pandas as pd

with open('data/data_generated/stations.json') as f:
    stations = json.load(f)

distance_factor = 250  # 250 meters per each step
number_of_stations = len(stations)
distance_matrix = np.zeros(shape=(number_of_stations, number_of_stations))

for station in range(len(stations)):
    "normal euclidean distance is calculated"
    for other_station in range(len(stations)):
        dx = abs(stations[station]["location"][0] - stations[other_station]["location"][0])
        dy = abs(stations[station]["location"][1] - stations[other_station]["location"][1])
        distance_matrix[station][other_station] = sqrt(dx ** 2 + dy ** 2)*0.25  #*(60 / (60 * 3600)) * (60
"""
"show distances in a heat map"
import matplotlib.pyplot as plt

plt.imshow(distance_matrix, cmap='hot', interpolation='nearest')
plt.show()
"""
distance_matrix = distance_matrix.round(2)

pd.DataFrame(distance_matrix).to_csv("data/data_generated/travel_times.csv")
