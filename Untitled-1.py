import time
import os
from datetime import datetime
import random

#ORDER INFO: MOVIE TITLE, ROOM NUMBER, SCHEDULE, SEAT, PRICE, TIME
orders = {}

def tryparse(value):
    try:
        return int(value)
    except ValueError:
        return None

def generate_TID():
    while True:
        tid = random.randint(1000, 9999)
        if tid not in orders:
            return tid

def confirm_order():
    tid = generate_TID()
    orders[tid] = {
        "Title:": cinema_info[chosen_room]["Title"],
        "Room Number": chosen_room,
        "Schedule": cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
        "Seat(s)": booked_seats,
        "Price:": total_price,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    for seat in booked_seats:
        cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"][seat-1] = 'X' #replace booked seat by the character X

def display_seats(room_num, time_id):
    movie_and_time = cinema_info[room_num]["Showtimes"][time_id]["Seats"]
    print("┌──────────────────────────────────────────────────┐")
    print("│                      SCREEN                      │")
    print("└──────────────────────────────────────────────────┘\n\n")

    for i, seat in enumerate(movie_and_time, start=1): #nag enumerate ako para maayos ung seats by index, instead of the actual values. kasi nga narereplace sila by letter X if booked
        print(f"{seat:>2}  ", end=" ")
        if i % 5 == 0: #add space per 5 seats
            print ("    ", end=" ")
        if i % 10 == 0: #newline per 10 seats
            print()

def print_all_info(dict, info_to_print): #this just prints whatever info needed in a list by numbers
    n = 0
    for _, info in dict.items():
        n += 1
        print(f"{n}. {info[info_to_print]}")

#main----------------------------------------------------------------------
max_seats = 50
cinema_info = {
    1: { #Room 1
        "Title": "Movie 1",
        "Price": 150,
        "Showtimes": {
            1: {"Time": "1:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "2:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "3:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    2: { #Room 2
        "Title": "Movie 2",
        "Price": 250,
        "Showtimes": {
            1: {"Time": "4:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "5:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "6:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    3: { #Room 3
        "Title": "Movie 3",
        "Price": 350,
        "Showtimes": {
            1: {"Time": "7:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "8:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "9:00", "Seats": list(range(1, (max_seats+1)))}
        }
    }    
}

while True:
    os.system('cls')
    #print all orders for debugging
    for key, val in orders.items():
        print(f"{key}: {val}")
    print()

    print("WELCOME TO MOVIE TICKET RESERVATION SYSTEM")
    print("(Enter 0 anytime to return to the previous menu)")
    print("\n1. Book Movie Ticket \n2. Manage Orders")

    user_input = tryparse(input("> "))

    if user_input is None or user_input > 2:
        print("Invalid boi")
        time.sleep(1)
        continue
    else:
        match(user_input):
            case 1:
                while True: #Select Room
                    os.system('cls')
                    print("Rooms:")
                    print_all_info(cinema_info, "Title")
                    chosen_room = tryparse(input("> "))

                    if chosen_room is None or chosen_room > len(cinema_info) or chosen_room < 0:
                        print("Invalid boi")
                        time.sleep(1)
                        continue
                    if chosen_room == 0:
                        break
                    
                    while True: #Select Schedule
                        os.system('cls')
                        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time:")
                        print_all_info(cinema_info[chosen_room]["Showtimes"], "Time")
                        chosen_time = tryparse(input("> "))
                        
                        if chosen_time is None or chosen_time > len(cinema_info[chosen_room]["Showtimes"]) or chosen_time < 0:
                            print("Invalid boi")
                            time.sleep(1)
                            continue
                        if chosen_time == 0:
                            break

                        while True: #Select Seats
                            os.system('cls')
                            print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
                            display_seats(chosen_room, chosen_time)
                            print()
                            chosen_seat = input("> Choose seat(s) (separated by commas): ")

                            #below is kinda spaghetti but this block checks for valid characters, since the program allows booking multiple seats separated by commas, it makes the input field pretty sensitive
                            invalid_found = False
                            for seat in chosen_seat.split(","): #split by commas first
                                if seat == "": #if its empty, thats invalid
                                    invalid_found = True
                                    break

                                for char in seat: #now check every character if its a digit
                                    if not char.isdigit():
                                        invalid_found = True
                                        break
                                if invalid_found:
                                    brea
                            

                            if not invalid_found and len(chosen_seat.split(",")) == len(set(chosen_seat.split(","))): #set() returns a collection with removed duplicates. if the original has no duplicats, then it should match the length of the set()
                                booked_seats = [int(seat) for seat in chosen_seat.split(",")]
                                if booked_seats == [0]: #if the list ONLY contains a 0, break the loop, which returns to the previous menu
                                    break

                                for seat in booked_seats: #self explanatory, booked seats should only be in the range from 1 to whatever max number of seats is
                                    if seat > max_seats or seat < 1:
                                        invalid_found = True
                            else:
                                invalid_found = True
                            
                            if invalid_found: #restart loop if invalid was found
                                print("Invalid boi")
                                time.sleep(1)
                                continue

                            print("\nConfirm Order: \n---------------")
                            print(f"Title: {cinema_info[chosen_room]['Title']} \nRoom: {chosen_room} \nSchedule: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
                            print("Seat(s): ", end = " ")
                            for i, seat in enumerate(booked_seats):
                                if i < len(booked_seats) - 1:
                                    print(f"{seat}, ", end="")
                                else:
                                    print(f"{seat}")
                            total_price = cinema_info[chosen_room]["Price"] * len(booked_seats)
                            print(f"--------------- \nPrice: {total_price}")
                            input("> Enter Y to Confirm: ")
                            confirm_order()
            case 2:
                pass

    input() #wala lang to, i run using cmd, nilagyan ko lang para di magclose agad ung cmd