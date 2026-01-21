import time
import os
from datetime import datetime
import random
from debug import DebugTools

current_menu_id = 1 #this menu id is used to determine which panel to show, each panels modifies its value to show the correct menu order. so every loop, its value changes, which changes the menu shown as well
max_seats = 50 
orders = {} #ORDER INFO: ORDER ID, MOVIE TITLE, ROOM NUMBER, SCHEDULE, SEAT, PRICE, TIME
cinema_info = {}

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

def mark_seats(marker, room_num, time, seats_to_mark_from, convert_time, use_marker):
    if convert_time:
        showtimes = cinema_info[room_num]["Showtimes"]
        for key, val in showtimes.items():
            if val["Time"] == time:
                time = key
                break
    for seat in seats_to_mark_from:
        cinema_info[room_num]["Showtimes"][time]["Seats"][seat-1] = marker if use_marker else seat

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

#-----------------------------------------------------------------------------------
def select_room_panel(tid):
    global current_menu_id, exit #current_menu_id, nasa Main ito, this is used para makapag traverse ung menu smoothly by detecting anong menu dapat ung lalabas currently
    while True:
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room Number']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
        print("Rooms:")
        print_all_info(cinema_info, "Title")
        chosen_room = tryparse(input("> "))

        if chosen_room is None or chosen_room > len(cinema_info) or chosen_room < 0:
            print("Invalid boi")
            time.sleep(1)
            continue
        elif chosen_room == 0: exit = True; return #edits the exit boolean variable that allows the menu traversal to work. used in a while loop sa Main
        else: current_menu_id += 1; return chosen_room #increment menu id to go to the next  menu
        
def select_schedule_panel(chosen_room, tid):
     global current_menu_id
     while True: 
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room Number']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
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
def select_seats_panel(chosen_room, chosen_time, tid):
    global current_menu_id, flag_for_multiple_zeros
    if tid:
        mark_seats("[]", orders[tid]["Room Number"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, True)
    while True:
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room Number']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
        display_seats(chosen_room, chosen_time)
        print()
        flag_for_multiple_zeros = False
        chosen_seat = input("> Choose seat(s) (separated by comma): ") #allow booking multiple seats per order, separated by comma

        if chosen_seat == "0": #ito kasi di naman nadedetect mga 00000 input since comparing to string lang, pero by default python converts multiple zeros to single 0 lang rin pero di ko inallow mag ganon cause of a few input issues
            current_menu_id -= 1 #decrement menu id to go back to previous menu
            if tid:
                mark_seats("X", orders[tid]["Room Number"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, True)
            break
        elif are_input_seat_invalid(chosen_seat):
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            booked_seats = [int(seat) for seat in chosen_seat.split(",")]
            if are_seats_unavailable(booked_seats, chosen_room, chosen_time, tid):
                print("Seat already taken.")
                time.sleep(1)
                continue
            
        if flag_for_multiple_zeros: continue
        complete_order(chosen_room, chosen_time, booked_seats, tid if tid else None, "[]" if tid else "X")

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

def are_seats_unavailable(seats, chosen_room, chosen_time, tid):
    global flag_for_multiple_zeros
    if tid:
        for seat in seats:
            if seat < 1:
                flag_for_multiple_zeros = True
                print("Invalid boi")
                time.sleep(1)
                return False
            if seat not in orders[tid]['Seat(s)'] and seat not in cinema_info[chosen_room]['Showtimes'][chosen_time]['Seats']:
                return True
    else:
        for seat in seats:
            if seat < 1:
                flag_for_multiple_zeros = True
                print("Invalid boi")
                time.sleep(1)
                return False
            if seat not in cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"]:
                return True
        
def complete_order(chosen_room, chosen_time, seats, tid, marker_for_booked_seats):
    print("\nConfirm Order: \n---------------")
    print(f"Title: {cinema_info[chosen_room]['Title']} \nRoom: {chosen_room} \nSchedule: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
    print("Seat(s): ", end = " ")
    for i, seat in enumerate(seats):
        if i < len(seats) - 1:
            print(f"{seat}, ", end="")
        else:
            print(f"{seat}")
    total_price = cinema_info[chosen_room]["Price"] * len(seats)
    print(f"--------------- \nPrice: {total_price}")
    confirmation = input("> Enter Y to Confirm: ")

    if confirmation.capitalize() == "Y":
        confirm_order(chosen_room, chosen_time, total_price, seats, tid, marker_for_booked_seats)
    else:
        print("Cancelled.")
    time.sleep(2)

def confirm_order(chosen_room, chosen_time, price, seats, tid, marker_for_booked_seats): #enter TID if updating
    if tid is not None:
        mark_seats("", orders[tid]["Room Number"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, False)
    else:
        tid = generate_TID()

    orders[tid] = {
        "Title": cinema_info[chosen_room]["Title"],
        "Room Number": chosen_room,
        "Schedule": cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
        "Seat(s)": seats,
        "Price": price,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    mark_seats(marker_for_booked_seats, chosen_room, chosen_time, seats, False, True)
    print("Success! We look forward to seeing you!")
#-----------------------------------------------------------------------------------

def manage_orders_panel():
    global exit
    while True:
        os.system('cls')
        print("What would you like to do?\n1. Search Order\n2. Update Order \n3. Cancel Order\n4. View All Orders")
        manage_choice = tryparse(input("> "))
        if manage_choice == 0: exit = True; return
        elif manage_choice is None or manage_choice > 4 or manage_choice < 1:
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            return manage_choice

def search_order_panel():
    global current_menu_id, exit
    while True:
        os.system('cls')
        if not orders:
            print("No orders found.")
            time.sleep(2)
            return
        print("Orders:")
        for tid in orders.keys():
            print(tid)
        search_choice = tryparse(input("\n> Enter TID to search: "))
        if search_choice == 0: exit = True; return
        elif search_choice is None or search_choice not in orders:
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            info = orders[search_choice]
            print(f"{search_choice}: {info}")
            input("Press Enter to continue...")
            return

def update_order_panel():
    global current_menu_id, exit
    while True:
        exit = False
        os.system('cls')
        if not orders:
            print("No orders found.")
            time.sleep(2)
            return
        display_all_orders(orders)
        tid = tryparse(input("\n> Enter TID to update: "))
        if tid == 0: return
        elif tid is None or tid not in orders:
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            new_room = 0; new_time = 0
            current_menu_id = 1
            while not exit:
                os.system('cls')
                match(current_menu_id):
                    case 1: new_room = select_room_panel(tid)
                    case 2: new_time = select_schedule_panel(new_room, tid)
                    case 3: select_seats_panel(new_room, new_time, tid)

def cancel_order_panel():
    while True:
        os.system('cls')
        if not orders:
            print("No orders found.")
            time.sleep(2)
            return
        display_all_orders(orders)
        cancel_choice = tryparse(input("\n> Enter TID to cancel: "))
        if cancel_choice == 0: return
        elif cancel_choice is None or cancel_choice not in orders:
            print("Invalid boi")
            time.sleep(1)
            continue
        
        print("Are you sure you want to cancel this order?")
        confirmation = input("> Enter Y to Confirm: ")
        if confirmation.capitalize() == "Y":
            mark_seats("", orders[cancel_choice]["Room Number"], orders[cancel_choice]["Schedule"], orders[cancel_choice]["Seat(s)"], True, False)
            del orders[cancel_choice]
            print("Order Cancelled.")
        else:
            print("Cancellation aborted.")
        time.sleep(2)

def view_all_orders_panel():
    while True:
        os.system('cls')
        if not orders:
            print("No orders found.")
            time.sleep(2)
            return
        print("Sort Orders by:\n1. Room Number\n2. Schedule\n3. Price\n4. Order Date")
        sort_choice = tryparse(input("> "))
        if sort_choice == 0: return
        elif sort_choice is None or sort_choice > 4 or sort_choice < 1:
            print("Invalid boi")
            time.sleep(1)
            continue
        else:
            match(sort_choice):
                case 1:
                    sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Room Number']))
                case 2:
                    sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Schedule']))
                case 3:
                    sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Price']))
                case 4:
                    sorted_orders = dict(sorted(orders.items(), key=lambda item: datetime.strptime(item[1]['Time'], "%Y-%m-%d %H:%M:%S")))
                
            while True:
                os.system('cls')
                print("Orders:")
                display_all_orders(sorted_orders)
                choice = input("\nEnter R to reverse the list, else any key to exit...")
                if choice.capitalize() == "R":
                    sorted_orders = dict(reversed(sorted_orders.items()))
                else:
                    break

def display_all_orders(order_collection):
    for tid, info in order_collection.items():
        print(f"Order ID: {tid} | Title: {info['Title']} | Room {info['Room Number']} | Schedule: {info['Schedule']} | Seat(s): {info['Seat(s)']} | Price: {info['Price']} | Order Date: {info['Time']}")

#main----------------------------------------------------------------------
modify_cinema_room(1, "Movie 1", 150, "1:00", "2:00", "3:00")
modify_cinema_room(2, "Movie 2", 250, "4:00", "5:00", "6:00")
modify_cinema_room(3, "Movie 3", 350, "7:00", "8:00", "9:00")

generator = DebugTools(cinema_info, orders)
generator.generate_random_orders(4)

while True:
    os.system('cls')
    #print all orders for debugging lang, remove rin to pag tapos na
    display_all_orders(orders)

    print("WELCOME TO MOVIE TICKET RESERVATION SYSTEM")
    print("(Enter 0 anytime to return to the previous menu)")
    print("\n1. Book Movie Ticket \n2. Manage Orders(Wala pa) \n3. Exit")

    user_input = tryparse(input("> "))
    if user_input is None or user_input > 3:
        print("Invalid boi")
        time.sleep(1)
        continue
    else:
        exit = False
        match(user_input):
            case 1:
                room_num = 0
                time_id = 0
                current_menu_id = 1
                while not exit:
                    match(current_menu_id):
                        case 1: room_num = select_room_panel(None)
                        case 2: time_id = select_schedule_panel(room_num, None)
                        case 3: select_seats_panel(room_num, time_id, None)
            case 2:
                while not exit:
                    choice = manage_orders_panel()
                    match(choice):
                        case 1:
                            search_order_panel()
                        case 2:
                            update_order_panel()
                        case 3:
                            cancel_order_panel()
                        case 4:
                            view_all_orders_panel()
            case 3:
                break
input() #wala lang to, i run using cmd, nilagyan ko lang para di magclose agad ung cmd