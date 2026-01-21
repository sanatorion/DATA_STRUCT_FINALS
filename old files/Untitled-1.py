import time
import os
from datetime import datetime
import random

#SPAGHETTI CODE AYUSIN PA
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

def confirm_order(chosen_room, chosen_time, price, seats):
    tid = generate_TID()
    orders[tid] = {
        "Title:": cinema_info[chosen_room]["Title"],
        "Room Number": chosen_room,
        "Schedule": cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
        "Seat(s)": seats,
        "Price:": price,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    for seat in seats:
        cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"][seat-1] = 'X' #replace booked seat by the character X
    print("Ticket Booked! We look forward to seeing you!")

def modify_cinema_room(room_num, movie_name, price, time1, time2, time3): #add or edit any movie details using this function
    cinema_info[room_num] = { 
        "Title": movie_name,
        "Price": price,
        "Showtimes": {
            1: {"Time": time1, "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": time2, "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": time3, "Seats": list(range(1, (max_seats+1)))}
        }
    }

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

def select_room_panel(chosen_room):
    global current_menu_id, exit #current_menu_id, nasa Main ito, this is used para makapag traverse ung menu smoothly by detecting anong menu dapat ung lalabas currently
    while True:
        os.system('cls')
        print("Rooms:")
        print_all_info(cinema_info, "Title")
        chosen_room = tryparse(input("> "))

        if chosen_room is None or chosen_room > len(cinema_info) or chosen_room < 0:
            print("Invalid boi")
            time.sleep(1)
            continue
        elif chosen_room == 0: exit = True; return #edits the exit boolean variable that allows the menu traversal to work. used in a while loop sa Main
        else: current_menu_id += 1; return chosen_room #increment menu id to go to the next  menu
        
def select_schedule_panel(chosen_room, chosen_time):
     global current_menu_id
     while True: 
        os.system('cls')
        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time:")
        print_all_info(cinema_info[chosen_room]["Showtimes"], "Time")
        chosen_time = tryparse(input("> "))

        if chosen_time is None or chosen_time > len(cinema_info[chosen_room]["Showtimes"]) or chosen_time < 0:
            print("Invalid boi")
            time.sleep(1)
            continue
        elif chosen_time == 0: current_menu_id -= 1; break #decrement menu id to go back to previous menu
        else: current_menu_id += 1; return chosen_time #increment menu id to go to the next  menu

flag_for_multiple_zeros = False #just a lazy checker for 00000 inputs, its main condition is in "are_seats_unavailable() (line 151)"" tignan mo comment sa line 104
def select_seats_panel(chosen_room, chosen_time):
    global current_menu_id, flag_for_multiple_zeros
    while True:
        os.system('cls')
        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
        display_seats(chosen_room, chosen_time)
        print()
        flag_for_multiple_zeros = False
        chosen_seat = input("> Choose seat(s) (separated by comma): ") #allow booking multiple seats per order, separated by comma

        if chosen_seat == "0": #ito kasi di naman nadedetect mga 00000 input since comparing to string lang, pero by default python converts multiple zeros to single 0 lang rin pero di ko inallow mag ganon cause of a few input issues
            current_menu_id -= 1 #decrement menu id to go back to previous menu
            break
        elif are_input_seat_invalid(chosen_seat):
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            booked_seats = [int(seat) for seat in chosen_seat.split(",")]
            if are_seats_unavailable(booked_seats, chosen_room, chosen_time):
                print("Seat already taken.")
                time.sleep(1)
                continue
            
        if flag_for_multiple_zeros: continue
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
        confirmation = input("> Enter Y to Confirm: ")
        if confirmation.capitalize() == "Y":
            confirm_order(chosen_room, chosen_time, total_price, booked_seats)
        else:
            print("Order cancelled.")
        time.sleep(2)

def are_input_seat_invalid(chosen_seat):
    seats = chosen_seat.split(",") #since we allow booking multiple seats per order, seats is a string muna and yeah split it by comma
    for seat in seats:
        if seat == "": 
            return True
        for char in seat:
            if not char.isdigit():  #check each character in the current seat string if digit sya
                return True
        if int(seat) > max_seats or int(seat) < 0:  #make sure seat is actually in the range of seat numbers
            return True
        
    if len(seats) != len(set(seats)): #set() removes duplicates in a collection, so the original collection must match the length of the set() collection if walang duplicates, if it dont match, edi invalid
        return True
    return False

def are_seats_unavailable(seats, chosen_room, chosen_time):
    global flag_for_multiple_zeros
    for seat in seats:
        if seat < 1: #if seat num input is 0000000, python automatically converts it to a single 0 kaya if less than 1, then flag it
            flag_for_multiple_zeros = True
            print("Invalid boi")
            time.sleep(1)
            return False
        if seat not in cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"]:
            return True

#main----------------------------------------------------------------------
#ORDER INFO: MOVIE TITLE, ROOM NUMBER, SCHEDULE, SEAT, PRICE, TIME
max_seats = 50
orders = {}
cinema_info = {}

modify_cinema_room(1, "Movie 1", 150, "1:00", "2:00", "3:00")
modify_cinema_room(2, "Movie 2", 250, "4:00", "5:00", "6:00")
modify_cinema_room(3, "Movie 3", 350, "7:00", "8:00", "9:00")

while True:
    os.system('cls')
    #print all orders for debugging lang, remove rin to pag tapos na
    for key, val in orders.items():
        print(f"{key}: {val}")
    print()

    print("WELCOME TO MOVIE TICKET RESERVATION SYSTEM")
    print("(Enter 0 anytime to return to the previous menu)")
    print("\n1. Book Movie Ticket \n2. Manage Orders(Wala pa) \n3. Exit")

    user_input = tryparse(input("> "))
    if user_input is None or user_input > 3:
        print("Invalid boi")
        time.sleep(1)
        continue
    else:
        match(user_input):
            case 1:
                room_num = 0
                time_id = 0
                exit = False
                current_menu_id = 1 #this menu id is used to determine which panel to show, each panels modifies its value to show the correct menu order. so every loop, its value changes, which changes the menu shown as well
                while not exit:
                    match(current_menu_id):
                        case 1: room_num = select_room_panel(room_num)
                        case 2: time_id = select_schedule_panel(room_num, time_id)
                        case 3: select_seats_panel(room_num, time_id)
            case 2:
                pass #dito ung admin stuff 
            case 3:
                break
input() #wala lang to, i run using cmd, nilagyan ko lang para di magclose agad ung cmd