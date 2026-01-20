import time
import os

def tryparse(value):
    try:
        return int(value)
    except ValueError:
        return None

def display_seats(movie_id, time_id):
    movie_and_time = movie_info[movie_id]["Showtimes"][time_id]["Seats"]
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

#main
max_seats = 50
movie_info = {
    1: {
        "Title": "Movie 1",
        "Showtimes": {
            1: {"Time": "1:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "2:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "3:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    2: {
        "Title": "Movie 2",
        "Showtimes": {
            1: {"Time": "4:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "5:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "6:00", "Seats": list(range(1, (max_seats+1)))}
        }
    },
    3: {
        "Title": "Movie 3",
        "Showtimes": {
            1: {"Time": "7:00", "Seats": list(range(1, (max_seats+1)))},
            2: {"Time": "8:00", "Seats": list(range(1, (max_seats+1)))},
            3: {"Time": "9:00", "Seats": list(range(1, (max_seats+1)))}
        }
    }    
}

while True:
    os.system('cls')
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
                print("Choose a movie:")
                print_all_info(movie_info, "Title")
                chosen_movie = tryparse(input("> "))

                #add error handling here
                os.system('cls')
                print("Choose a time:")
                n = 0
                print_all_info(movie_info[chosen_movie]["Showtimes"], "Time")
                chosen_time = tryparse(input("> "))
                os.system('cls')

                display_seats(chosen_movie, chosen_time)
                print("\n")
                chosen_seat = tryparse(input("> Choose a seat: "))
                #add error handling here

                       
            case 2:
                pass

    input()