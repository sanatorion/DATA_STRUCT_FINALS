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
        "Seat": chosen_seat,
        "Price:": cinema_info[chosen_room]["Price"],
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"][chosen_seat-1] = 'X'

def display_seats(room_num, time_id):
    movie_and_time = cinema_info[room_num]["Showtimes"][time_id]["Seats"]
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
cinema_info = {
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
                while True:
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
                    
                    while True:
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

                        while True:
                            os.system('cls')
                            print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
                            display_seats(chosen_room, chosen_time)
                            print()
                            chosen_seat = tryparse(input("> Choose a seat: "))
                            
                            if chosen_seat is None or chosen_seat > max_seats or chosen_seat < 0:
                                print("Invalid boi")
                                time.sleep(1)
                                continue
                            if chosen_seat == 0:
                                break

                            print("\nConfirm Order: \n---------------")
                            print(f"Title: {cinema_info[chosen_room]['Title']} \nRoom: {chosen_room} \nSchedule: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']} \nSeat: {chosen_seat} \n---------------\nPrice:{cinema_info[chosen_room]['Price']}\n")
                            input("> Enter Y to Confirm: ")
                            confirm_order()
            case 2:
                pass

    input()