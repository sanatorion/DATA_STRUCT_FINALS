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

def confirm_order(chosen_room, chosen_time, chosen_seat):
    tid = generate_TID()
    orders[tid] = {
        "Title:": cinema[chosen_room]["Title"],
        "Room Number": chosen_room,
        "Schedule": cinema[chosen_room]["Showtimes"][chosen_time]["Time"],
        "Seat": chosen_seat,
        "Price:": cinema[chosen_room]["Price"],
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    cinema[chosen_room]["Showtimes"][chosen_time]["Seats"][chosen_seat-1] = 'X'

def display_seats(room_num, time_id):
    movie_and_time = cinema[room_num]["Showtimes"][time_id]["Seats"]
    print("┌──────────────────────────────────────────────────┐")
    print("│                      SCREEN                      │")
    print("└──────────────────────────────────────────────────┘\n\n")

    for i, seat in enumerate(movie_and_time, start=1):
        print(f"{seat:>2}  ", end=" ")
        if i % 5 == 0: 
            print ("    ", end=" ")
        if i % 10 == 0:
            print()

def print_all_info(dict, info_to_print):
    n = 0
    for _, info in dict.items():
        n += 1
        print(f"{n}. {info[info_to_print]}")

#main----------------------------------------------------------------------
max_seats = 50
cinema = {
    1: {
        "Title": "Movie 1",
        "Price": 150,
        "Showtimes": {
            1: {"Time": "1:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "2:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "3:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    2: {
        "Title": "Movie 2",
        "Price": 250,
        "Showtimes": {
            1: {"Time": "4:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "5:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "6:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    3: {
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
    #print orders for debugging
    for key, val in orders.items():
        print(f"{key}: {val}")
    print()

    print("WELCOME TO MOVIE TICKET RESERVATION SYSTEM")
    print("1. Book Movie Ticket \n2. Manage Orders")

    user_input = tryparse(input("> "))

    if user_input is None:
        print("Invalid boi")
        time.sleep(1)
        os.system('cls')
    else:
        match(user_input):
            case 1:
                os.system('cls')
                print("Choose Rooms: (or movie idk man)")
                print_all_info(cinema, "Title")
                chosen_room = tryparse(input("> "))

                #add error handling here
                os.system('cls')
                print("Choose a time:")
                n = 0
                print_all_info(cinema[chosen_room]["Showtimes"], "Time")
                chosen_time = tryparse(input("> "))
                os.system('cls')

                display_seats(chosen_room, chosen_time)
                print("\n")
                chosen_seat = tryparse(input("> Choose a seat: "))
                #add error handling here
                os.system('cls')

                print("Confirm Order: \n---------------")
                print(f"Title: {cinema[chosen_room]['Title']} \nRoom: {chosen_room} \nSchedule: {cinema[chosen_room]['Showtimes'][chosen_time]['Time']} \nSeat: {chosen_seat} \n---------------\nPrice:{cinema[chosen_room]['Price']}\n")
                input("> Enter Y to Confirm: ")
                confirm_order(chosen_room, chosen_time, chosen_seat)
            case 2:
                pass

    input()