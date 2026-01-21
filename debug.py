import random
from datetime import datetime

#AI LANG TO PANG DEBUG
class DebugTools:
    def __init__(self, cinema_info, orders):
        self.cinema_info = cinema_info
        self.orders = orders

    def generate_TID(self):
        while True:
            tid = random.randint(1000, 9999)
            if tid not in self.orders:
                return tid

    def generate_random_orders(self, num_orders=5):
        """
        Generates and adds a specified number of random orders to the system.
        Each order picks a random room, time, and available seats.
        """
        for _ in range(num_orders):
            if not self.cinema_info:
                print("No cinema rooms available to generate orders.")
                break
            
            # Randomly select a room
            chosen_room = random.choice(list(self.cinema_info.keys()))
            
            # Randomly select a showtime for that room
            chosen_time = random.choice(list(self.cinema_info[chosen_room]["Showtimes"].keys()))
            
            # Get available seats (those not marked as 'X')
            available_seats = [seat for seat in self.cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"] if seat != 'X']
            
            if not available_seats:
                print(f"No available seats for room {chosen_room} at time {chosen_time}. Skipping this order.")
                continue
            
            # Randomly choose 1 to 5 seats (or fewer if not enough available)
            num_seats_to_book = random.randint(1, min(5, len(available_seats)))
            chosen_seats = random.sample(available_seats, num_seats_to_book)
            
            # Calculate price
            price = self.cinema_info[chosen_room]["Price"] * len(chosen_seats)
            
            # Generate TID and add order
            tid = self.generate_TID()
            self.orders[tid] = {
                "Title": self.cinema_info[chosen_room]["Title"],
                "Room Number": chosen_room,
                "Schedule": self.cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
                "Seat(s)": chosen_seats,
                "Price": price,
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Mark seats as booked
            for seat in chosen_seats:
                self.cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"][seat-1] = 'X'
            
            print(f"Generated random order: TID {tid} - {self.cinema_info[chosen_room]['Title']} at {self.cinema_info[chosen_room]['Showtimes'][chosen_time]['Time']}, Seats: {chosen_seats}")
    
    def add_random_order(cinema_info, orders):
        if not cinema_info:
            print("No cinema rooms available.")
            return
        
        
        # Choose random room
        chosen_room = random.choice(list(cinema_info.keys()))
        
        # Choose random time for the room
        chosen_time = random.choice(list(cinema_info[chosen_room]["Showtimes"].keys()))
        
        # Get available seats (not 'X')
        available_seats = [seat for seat in cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"] if seat != 'X']
        
        if not available_seats:
            print("No available seats for this random selection.")
            return
        
        # Choose random number of seats (1 to min(5, available))
        num_seats = random.randint(1, min(5, len(available_seats)))
        
        # Choose random seats without replacement
        chosen_seats = random.sample(available_seats, num_seats)
        
        # Calculate price
        price = cinema_info[chosen_room]["Price"] * len(chosen_seats)
        
        # Generate TID and add order
        tid = None
        while True:
            temp_tid = random.randint(1000, 9999)
            if tid not in orders:
                tid = temp_tid
                break
            
        orders[tid] = {
            "Title": cinema_info[chosen_room]["Title"],
            "Room Number": chosen_room,
            "Schedule": cinema_info[chosen_room]["Showtimes"][chosen_time]["Time"],
            "Seat(s)": chosen_seats,
            "Price": price,
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Mark seats as booked
        for seat in chosen_seats:
            cinema_info[chosen_room]["Showtimes"][chosen_time]["Seats"][seat-1] = 'X'