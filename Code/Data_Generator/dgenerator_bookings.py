
"""
April 2020 - Ayman Mahmoud
--------------------------------------------
this code generates booking data
input: (<--) : Booking data with the following fields :-
"id": 16566388,
        "price": 1370,
        "passengers": 1,
        "maximumDuration": 2100,
        "jobs": [
                "id": 23926039,
                "type": "PickUpJob",
                "timeWindowBeginDate": 42600,
                "timeWindowEndDate": 43500,
                "duration": 60,
                "latitude": 49.01606369018555,
                "longitude": 1.6916327476501465,
                "station": "s16"
                ]

output: (-->) : Booking data with new and modified fields :-
            "id": 17149523,
            "passengers": 1,
            "maximumDuration": 2100,
            "jobs": [
                {
                    "id": 25109598,
                    "duration": 60,
                    "latitude": 48.98927307128906,
                    "longitude": 1.715390682220459,
                    "station": "s5",
                    "timeslot": 4,
                    "distancelimit": 2000,
                    "location": [
                        36,
                        21
                    ]
                }
            ]
"""
import json
import random

# a Python object (dict):
with open('data/Data_Yuso-20200302/week_data.json') as f:
    data = json.load(f)
bookings = data["bookings"]
shifts = data["shifts"]  # not needed for now

"Define variables"  # essayer de parametrer ces données
timeslot_size = 10  # size can be changed later to display a larger array of items
graph_size = range(0, 50)  # range of points the booking can be at
pickup_stations_size = 16

"Start modifying data here"
for booking in range(len(bookings)):
    "#1 - Keys we don't need for all bookings"
    try:
        del bookings[booking]["price"]
    except KeyError:
        print("Key 'price' not found")
    "#2 - remove second part of Job"
    try:
        del bookings[booking]["jobs"][1]
    except KeyError:
        print("Key 'jobs' not found")
    "#3 - remove job type"
    try:
        del bookings[booking]["jobs"][0]["type"]
    except KeyError:
        print("Key 'type' not found")
    "#4 - remove job time window"
    try:
        del bookings[booking]["jobs"][0]["timeWindowBeginDate"]
        del bookings[booking]["jobs"][0]["timeWindowEndDate"]
    except KeyError:
        print("Key 'time window' not found")
    "#5 - change destination station to be the same (S + number of stations available + 1)"
    # bookings[booking]["jobs"][0]["station"] = "s" + str(len(bookings) + 1)
    bookings[booking]["jobs"][0]["station"] = "s" + str(pickup_stations_size + 1)
    "#6 - add new key: timeslot"
    bookings[booking]["jobs"][0]["timeslot"] = random.randint(1, timeslot_size)
    "#7 - add new key: distancelimit"
    bookings[booking]["jobs"][0]["distancelimit"] = 2000  # the generator can then pick between variable distance limits
    "#8 - add new key: location"
    bookings[booking]["jobs"][0]["location"] = [random.choice(graph_size), random.choice(graph_size)]

if len(bookings) <= 10:
    with open("data/data_generated/bookings_short.json", "w") as write_file:
        json.dump(bookings, write_file, indent=4)
elif len(bookings) > 25:
    with open("data/data_generated/bookings_long.json", "w") as write_file:
        json.dump(bookings, write_file, indent=4)
else:
    with open("data/data_generated/bookings_medium.json", "w") as write_file:
        json.dump(bookings, write_file, indent=4)

