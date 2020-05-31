"""
May 2020 - Ayman Mahmoud
----------------------------------------
This module generates data corresponding each station
- location
- maximum capacity
- type (pickup or dropoff)
- name (s1, s2, ..., sX)
"""
import json

stations_size = 15
" you need to automate station location generation "
pickup_stations = [(0, 0), (0, 15), (0, 30), (0, 45), (15, 0), (15, 15), (15, 30),
                   (30, 0), (15, 45), (30, 15), (30, 30), (30, 45), (45, 0), (45, 15),
                   (45,30), (45, 45)]

stations = []
station = {
  "name": [],
  "pickup": [],
  "dropoff": [],
  "max_capacity": [],
  "location": []
}

" add depot station "
station = {
  "name": "s0",
  "pickup": False,
  "dropoff": True,
  "max_capacity": None,
  "location": (0, 65)
}

stations.append(station)


for station_itr in range(len(pickup_stations)):
    """
    station["name"].append("s" + str(station_itr))
    station["pickup"].append(True)
    station["dropoff"].append(False)
    station["max_capacity"].append(8)
    station["location"].append(pickup_stations[station_itr])
    stations.append(station)
    """
    station = {
        "name": "s" + str(station_itr+1),
        "pickup": True,
        "dropoff": False,
        "max_capacity": 8,
        "location": pickup_stations[station_itr]
    }
    stations.append(station)
" add drop off station "
station = {
  "name": "s" + str(len(pickup_stations)+1),
  "pickup": False,
  "dropoff": True,
  "max_capacity": None,
  "location": (25, 75)
}

stations.append(station)

with open("data/data_generated/stations.json", "w") as write_file:
    json.dump(stations, write_file, indent=4)