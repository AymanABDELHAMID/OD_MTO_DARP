"""
May 2020 - Ayman Mahmoud
-------------------------------------
This file is the main

factorized sample of the whole project
"""
import argparse

from dgenerator import generate_bookings


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-b,", help="the number of bookings you want in your instance (<150)", required=True)
    parser.add_argument("-s,", help="number of pickup stations in your instance (<20)", required=True)
    parser.add_argument("-t,", help="the number of time slots available (<20)", required=True)
    parser.add_argument("-v,", help="the number of vehicles that are available to serve(<200)", required=True)
    args = parser.parse_args()

    bookings_number = args.b
    stations_number = args.s
    timeslots_number = args.t
    drivers_number = args.v


    "do the if __main__ thing here"
    "don't run this part if in the command line the data is already given"
    "User input"
    print("Hello, welcome to the DARP solver.")

    while True:
        try:
            bookings_number = int(input("Please enter the number of bookings you want in your instance (<150)"))
            assert(1 <= bookings_number <= 150)
        except AssertionError:
            print("You entered a number greater than 150 or less than 1")
            continue
        except ValueError:
            print("You didn't enter a correct number")
            continue
        else:
            print("The number you entered is:", bookings_number)
            break
    while True:
        try:
            stations_number = int(input("Please insert the number of pickup stations in your instance (<20)"))
            assert(1 <= stations_number <= 20)
        except AssertionError:
            print("You entered a number greater than 20 or less than 1")
            continue
        except ValueError:
            print("You didn't enter a correct number")
            continue
        else:
            print("The number you entered is:", stations_number)
            break
    while True:
        try:
            timeslots_number = int(input("Please insert the number of time slots available (<20)"))
            assert(timeslots_number <= 20)
        except AssertionError:
            print("You entered a number greater than 20 or less than 1")
            continue
        except ValueError:
            print("You didn't enter a correct number")
        else:
            print("The number you entered is:", timeslots_number)
            break
    while True:
        try:
            drivers_number = int(input("Please insert the number of vehicles that are available to serve(<200)"))
            assert(drivers_number <= 200)
        except AssertionError:
            print("You entered a number greater than 200 or less than 1")
            continue
        except ValueError:
            print("You didn't enter a correct number")
        else:
            print("The number you entered is:", drivers_number)
            break

    print("You made it through all four steps")
    #################################################"""
    "population generator"
    #dg.generate_bookings(bookings_number)
    # generate_bookings(bookings_number)
    # Change color to red