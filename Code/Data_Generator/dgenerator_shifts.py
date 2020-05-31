"""
May 2020 - Ayman Mahmoud
----------------------------------------
This module generates all data corresponding to shifts
- id
- capacity
- location
- shiftbegin / shiftend
- maximum turnover
- average speed
"""

import json
import random

# a Python object (dict):
with open('data/Data_Yuso-20200302/week_data.json') as f:
    data = json.load(f)
shifts = data["shifts"]

"Start modifying data here"
for shift in range(len(shifts)):
    "Keys we don't need for all bookings"
    "#1 - remove second part of Job"
    try:
        del shifts[shift]["jobs"][1]
    except KeyError:
        print("Key 'jobs' not found")
    "#2 - remove Job 'id', 'Type' & 'Timedate'"
    try:
        del shifts[shift]["jobs"][0]["id"]
        del shifts[shift]["jobs"][0]["type"]
        del shifts[shift]["jobs"][0]["timeDate"]
    except KeyError:
        print("Key 'id' | 'Type' | 'Timedate' not found")
    "#3 - change maximum capacity to be 8 (a minibus)"
    shifts[shift]["capacity"] = 8
    "#4 - add new key: location"
    shifts[shift]["jobs"][0]["location"] = [0, 65]  # This is the location of the depot station
    "#5 - add new key: TimeWindow"
    shifts[shift]["jobs"][0]["TimeWindow"] = [360, 1320]  # A working day shift is from 6am to 10pm
    "#6 - add new key: Average_speed"
    shifts[shift]["jobs"][0]["Average_speed"] = 60  # A van average speed is 60km/h
    "Average speed can then be averaged by the history of each driver w.r.t a limit"

with open("data/data_generated/shifts.json", "w") as write_file:
    json.dump(shifts, write_file, indent=4)