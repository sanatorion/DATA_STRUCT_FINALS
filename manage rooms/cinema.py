from untitled_update import *

class ManageCinema:
    def modify_cinema_room(cinema_collection, room_num, movie_name, price, time1, time2, time3): #add or edit any cinema details using this function
        cinema_collection[room_num] = { 
            "Title": movie_name,
            "Price": price,
            "Showtimes": {
                1: {"Time": time1, "Seats": list(range(1, (max_seats+1)))},
                2: {"Time": time2, "Seats": list(range(1, (max_seats+1)))},
                3: {"Time": time3, "Seats": list(range(1, (max_seats+1)))}
            }
        }

    def delete_room_panel():
        print("")
    def delete_showtime_panel():
        pass
