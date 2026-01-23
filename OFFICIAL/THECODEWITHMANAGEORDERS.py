import time
import os
from datetime import datetime
import random

current_menu_id = 1 #used to simulate menu traversal. each panels modifies its value to show the correct menu order. so every loop, its value changes, which changes the menu shown as well
max_seats = 50 #total number of seats
orders = {} #ORDER INFO: ORDER ID, MOVIE TITLE, ROOM NUMBER, SCHEDULE, SEAT, PRICE, TIME
cinema_info = {} #stores cinema data here
orders_in_strings = {}

def display_invalid_message():
    print("Invalid"); time.sleep(1)

def build_string_reference():
    global orders_in_strings # update string references
    for tid, val in orders.items(): 
            orders_in_strings[tid] = ""
            for category, val2 in val.items():
                val2 = str(val2).replace("[", "").replace("]", "").replace(" ", "")
                orders_in_strings[tid] += (category + val2)

def tryparse(value):
    try:
        return int(value)
    except ValueError:
        return None

def is_input_time(value):
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False

def are_input_seat_invalid(chosen_seat):
    seats = chosen_seat.split(",") # since we allow booking multiple seats per order, seats is a string and is split by comma
    for seat in seats:
        if seat == "": 
            return True
        for char in seat:
            if not char.isdigit():  # check each character in the current seat string if its a digit
                return True
        if int(seat) < 1 or int(seat) > max_seats: # make sure seat is actually in the range of seat numbers
            return True
        
    if len(seats) != len(set(seats)): #set() returns a collection with removed duplicates, so the original collection must match the length of the set() collection if no duplicates
        return True
    return False

def are_seats_unavailable(seats, chosen_room, chosen_time, tid): #check if requested seats are available
    for seat in seats:
        if tid:
            if seat not in orders[tid]['Seat(s)'] and seat not in cinema_info[chosen_room]['Showtimes'][chosen_time]['Seats']: # Check if seat is taken by another order (not the current one being updated and not available)
                return True
        else:
            if seat not in cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"]: # check if seat is still in the list of seats (booked seats are replaced by a character 'X')
                return True
    return False

def generate_TID():
    while True:
        tid = random.randint(1000, 10000)
        if tid not in orders:
            return tid

def mark_seats(marker, room_num, time, seats_to_mark_from, convert_time, use_marker): #seat marker
    if convert_time: # Converts schedule string (stored in orders) to numeric time ID (used in showtimes) when updating an existing order.
        showtimes = cinema_info[room_num]["Showtimes"]
        for key, val in showtimes.items():
            if val["Time"] == time:
                time = key
                break
    for seat in seats_to_mark_from:
        cinema_info[room_num]["Showtimes"][time]["Seats"][seat-1] = marker if use_marker else seat #mark seats as marker, else just use seat number. seat number is used to revert booked seats

def modify_cinema_room(room_num, movie_name, price, time1, time2, time3): #add or edit any cinema details using this function
    cinema_info[room_num] = { 
        "Title": movie_name,
        "Price": price,
        "Showtimes": {
            1: {"Time": time1, "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": time2, "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": time3, "Seats": list(range(1, (max_seats+1)))}
        }
    }

def modify_title_or_showtimes_panel(chosen_room):
    global current_menu_id
    os.system('cls')
    print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']}\n1. Modify Room Title\n2. Manage Showtimes")
    choice = tryparse(input("> "))
    if choice == 0: current_menu_id -= 1
    elif not choice or (choice > 2 or choice < 0):
        display_invalid_message()
    elif choice == 1: current_menu_id += 1
    elif choice == 2: current_menu_id += 2

def modify_value_panel(value_to_change, use_time_only, chosen_room):
    global current_menu_id
    while True:
        os.system('cls')
        print(f"Current: {value_to_change}")
        new_val = input("> Enter new: ")
        if new_val == "0": current_menu_id -= 1; return value_to_change

        if use_time_only and not is_input_time(new_val): display_invalid_message()
        elif new_val.replace(" ", "") == "": display_invalid_message() 
        else: 
            if use_time_only: 
                showtimes = cinema_info[chosen_room]["Showtimes"]
                for _, val in showtimes.items():
                    if val["Time"] == new_val:
                        print("Schedule already occupied.")
                        time.sleep(1)
                        return value_to_change
            return new_val


def display_seats(room_num, time_id): #displays seats
    movie_and_time = cinema_info[room_num]["Showtimes"][time_id]["Seats"]
    print("┌──────────────────────────────────────────────────┐")
    print("│                      SCREEN                      │")
    print("└──────────────────────────────────────────────────┘\n\n")

    for i, seat in enumerate(movie_and_time, start=1): #nag enumerate ako para maayos ung display ng seats by index, instead of the actual values. kasi they can get replaced when booked
        print(f"{seat:>2}  ", end=" ")
        if i % 5 == 0: #add space per 5 seats
            print ("    ", end=" ")
        if i % 10 == 0: #newline per 10 seats
            print()

def print_all_info(dict, info_to_print): # Prints a numbered list of the specified info from each item in a dictionary
    n = 0
    for _, info in dict.items():
        n += 1
        print(f"{n}. {info[info_to_print]}")
    
def display_all_orders(order_collection):
    for tid, info in order_collection.items():
        print(f"Order ID: {tid} | Title: {info['Title']} | Room {info['Room']} | Schedule: {info['Schedule']} | Seat(s): {info['Seat(s)']} | Price: {info['Price']} | Order Date: {info['Time']}")

#-----------------------------------------------------------------------------------
def select_room_panel(tid):
    global current_menu_id, exit
    while True:
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
        print("Rooms:")
        print_all_info(cinema_info, "Title")
        chosen_room = tryparse(input("> "))

        if chosen_room is None or chosen_room > len(cinema_info) or chosen_room < 0:
            display_invalid_message()
            continue
        elif chosen_room == 0: exit = True; return #edits the exit boolean variable that also allows the menu traversal to work. used in a while loop sa Main
        else: current_menu_id += 1; return chosen_room #increment menu id to go to the next menu
        
def select_schedule_panel(chosen_room, tid, return_decrement):
     global current_menu_id
     while True: 
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time:")
        print_all_info(cinema_info[chosen_room]["Showtimes"], "Time")
        chosen_time = tryparse(input("> "))

        if chosen_time is None or chosen_time > len(cinema_info[chosen_room]["Showtimes"]) or chosen_time < 0:
            display_invalid_message()
            continue
        elif chosen_time == 0: current_menu_id -= return_decrement; break #decrement menu id to go back to previous menu
        else: current_menu_id += 1; return chosen_time #increment menu id to go to the next  menu

def select_seats_panel(chosen_room, chosen_time, tid): # tid parameter is used to indicate if updating an existing order (tid is the order ID) or creating a new booking (tid is None)
    global current_menu_id
    if tid:
        mark_seats("[]", orders[tid]["Room"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, True) # mark booked seats of currently accesed order with "[]"
    while True:
        os.system('cls')
        if tid:
            print(f"Order ID: {tid} | Room {orders[tid]['Room']} | Schedule: {orders[tid]['Schedule']} | Seat(s): {orders[tid]['Seat(s)']} | Price: {orders[tid]['Price']}")
        print(f"Room {chosen_room}: {cinema_info[chosen_room]['Title']} > Time: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
        display_seats(chosen_room, chosen_time)
        print()
        chosen_seat = input("> Choose seat(s) (separated by comma): ") # allow booking multiple seats per order, separated by comma

        if chosen_seat == "0":# comparing to string "0" prevents detecting multiple zeros (e.g., "00000") as back input, but Python auto-converts them to single 0 anyway, so it's fine. However, we disallow it due to inputs starting with 0 (e.g., "01") which is weird
            current_menu_id -= 1 #decrement menu id to go back to previous menu
            if tid:
                mark_seats("X", orders[tid]["Room"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, True) #revert "[]" marked seats to "X"
            break
        elif are_input_seat_invalid(chosen_seat):
            display_invalid_message()
            continue
        else:
            booked_seats = [int(seat) for seat in chosen_seat.split(",")]
            if are_seats_unavailable(booked_seats, chosen_room, chosen_time, tid):
                print("Seat already taken.")
                time.sleep(1)
                continue
        complete_order(chosen_room, chosen_time, booked_seats, tid if tid else None, "[]" if tid else "X") # This function calls confirm_order(), which calls mark_seats() with different markers: "[]" for updates (when tid exists) or "X" for new bookings (when tid is None)
        
def complete_order(chosen_room, chosen_time, seats, tid, marker_for_booked_seats):
    print("\nConfirm Order: \n---------------")
    print(f"Title: {cinema_info[chosen_room]['Title']} \nRoom: {chosen_room} \nSchedule: {cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}")
    print("Seat(s): ", end = " ")
    for i, seat in enumerate(seats):
        if i < len(seats) - 1: # print last index without comma
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

def confirm_order(chosen_room, chosen_time, price, seats, tid, marker_for_booked_seats): # tid is the order ID
    if tid:
        mark_seats("", orders[tid]["Room"], orders[tid]["Schedule"], orders[tid]["Seat(s)"], True, False) #revert previously booked seats to original seat numbers
    else:
        tid = generate_TID() # if no tid, generate a new TID for a new booking

    orders[tid] = {
        "Title": cinema_info[chosen_room]["Title"],
        "Room": chosen_room,
        "Schedule": cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
        "Seat(s)": seats,
        "Price": price,
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    mark_seats(marker_for_booked_seats, chosen_room, chosen_time, seats, False, True) # mark booked seats
    print("Seat(s) Booked.")
#-----------------------------------------------------------------------------------
def manage_orders_panel():
    global exit
    while True:
        os.system('cls')
        print("What would you like to do?\n1. Search Order\n2. Update Order \n3. Cancel Order\n4. View All Orders")
        manage_choice = tryparse(input("> "))
        if manage_choice == 0: exit = True; return
        elif manage_choice is None or manage_choice > 4 or manage_choice < 1:
            display_invalid_message()
            continue
        else:
            return manage_choice

def search_order_panel():
    while True:
        os.system('cls')
        if not orders:
            print("No orders found.")
            time.sleep(1)
            return
        print("1. Search by TID\n2. Search by Keyword")
        choice = tryparse(input("> "))
        if choice == 0: return
        if not choice or (choice < 0 or choice > 2): 
            display_invalid_message()
            continue
        match(choice):
            case 1: search_id_panel()
            case 2: search_keyword_panel()
        
def search_id_panel():
    while True:
        os.system('cls')
        print("Orders:")
        for tid in orders.keys():
            print(tid)
        search_choice = tryparse(input("\n> Enter TID to search: "))
        if search_choice == 0: return
        elif search_choice is None or search_choice not in orders:
            display_invalid_message()
            continue
        else:
            info = orders[search_choice]
            print(f"Order ID: {search_choice} | Title: {info['Title']} | Room {info['Room']} | Schedule: {info['Schedule']} | Seat(s): {info['Seat(s)']} | Price: {info['Price']} | Order Date: {info['Time']}")
            input("\nPress Enter to continue...")
            return
        
def search_keyword_panel():
    build_string_reference()
    while True:
        os.system('cls')
        search = input("> Search: ")
        if search == "0": return
        if not search: display_invalid_message(); continue
        print()
        matches = [tid for tid in orders_in_strings.keys() if search.replace(" ", "").lower() in orders_in_strings[tid].lower()]
        if not matches:
            print(f"'{search}' not found."); 
        else:
            for match in matches:
                print(f"Order ID: {match} | Title: {orders[match]['Title']} | Room {orders[match]['Room']} | Schedule: {orders[match]['Schedule']} | Seat(s): {orders[match]['Seat(s)']} | Price: {orders[match]['Price']} | Order Date: {orders[match]['Time']}")
        input("\nPress Enter to continue...")

def update_order_panel():
    global current_menu_id, exit # Uses the same global 'exit' variable as other panel functions for menu navigation control
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
            display_invalid_message()
            continue
        else:
            new_room = 0; new_time = 0
            current_menu_id = 1
            while not exit:
                os.system('cls')
                match(current_menu_id):
                    case 1: new_room = select_room_panel(tid)
                    case 2: new_time = select_schedule_panel(new_room, tid, 1)
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
            display_invalid_message()
            continue
        
        print("Are you sure you want to cancel this order?")
        confirmation = input("> Enter Y to Confirm: ")
        if confirmation.capitalize() == "Y":
            mark_seats("", orders[cancel_choice]["Room"], orders[cancel_choice]["Schedule"], orders[cancel_choice]["Seat(s)"], True, False)
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
        print("Sort Orders by:\n1. Room\n2. Schedule\n3. Price\n4. Order Date")
        sort_choice = tryparse(input("> "))
        if sort_choice == 0: return
        elif sort_choice is None or sort_choice > 4 or sort_choice < 1:
            display_invalid_message()
            continue
        else:
            match(sort_choice):
                case 1: sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Room']))
                case 2: sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Schedule']))
                case 3: sorted_orders = dict(sorted(orders.items(), key=lambda item: item[1]['Price']))
                case 4: sorted_orders = dict(sorted(orders.items(), key=lambda item: datetime.strptime(item[1]['Time'], "%Y-%m-%d %H:%M:%S")))
            while True:
                os.system('cls')
                print("Orders:")
                display_all_orders(sorted_orders)
                choice = input("\nEnter R to reverse the list, else any key to exit...")
                if choice.capitalize() == "R":
                    sorted_orders = dict(reversed(sorted_orders.items()))
                else:
                    break

#main----------------------------------------------------------------------
modify_cinema_room(1, "The Loved One", 300, "10:00", "13:00", "16:00")
modify_cinema_room(2, "Call Me Mother", 350, "11:00", "14:00", "17:00")
modify_cinema_room(3, "John Weak", 750, "12:00", "15:00", "18:00")

while True:
    os.system('cls')
    print("WELCOME TO MOVIE TICKET RESERVATION SYSTEM")
    print("(Enter 0 anytime to return to the previous menu)")
    print("\n1. Book Movie Ticket \n2. Manage Orders \n3. Manage Rooms\n4. Exit")
    user_input = tryparse(input("> "))

    if user_input is None or user_input > 5:
        display_invalid_message()
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
                        case 2: time_id = select_schedule_panel(room_num, None, 1)
                        case 3: select_seats_panel(room_num, time_id, None)
            case 2:
                while not exit:
                    choice = manage_orders_panel()
                    match(choice):
                        case 1: search_order_panel()
                        case 2: update_order_panel()
                        case 3: cancel_order_panel()
                        case 4: view_all_orders_panel()

            case 3:
                while not exit:
                    match(current_menu_id):
                        case 1: chosen_room = select_room_panel(None)
                        case 2: modify_title_or_showtimes_panel(chosen_room)
                        case 3: cinema_info[chosen_room]["Title"] = modify_value_panel(cinema_info[chosen_room]["Title"], False, None)
                        case 4: chosen_time = select_schedule_panel(chosen_room, None, 2)
                        case 5: cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"] = modify_value_panel(cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"], True, chosen_room)
            case 4:
                break