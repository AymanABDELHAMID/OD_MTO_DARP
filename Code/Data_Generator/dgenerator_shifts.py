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
    "#1 - Keys we don't need for all bookings"
    try:
        del shifts[booking]["price"]
    except KeyError:
        print("Key 'price' not found")