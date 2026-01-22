import random
class DebugTools:
    def __init__(self, cinema_info, orders):
        self.cinema_info = cinema_info
        self.orders = orders

    def generate_random_orders(self, count):
        """
        Generates `count` random valid orders using existing system logic.
        """

        for _ in range(count):
            # pick random room
            room = random.choice(list(self.cinema_info.keys()))

            # pick random showtime
            showtimes = self.cinema_info[room]["Showtimes"]
            time_id = random.choice(list(showtimes.keys()))

            # get available seats (non-X seats)
            available_seats = [
                seat for seat in showtimes[time_id]["Seats"]
                if isinstance(seat, int)
            ]

            if not available_seats:
                continue  # no seats left, skip

            # random seat count (1–3, capped by availability)
            seat_count = random.randint(1, min(3, len(available_seats)))
            chosen_seats = random.sample(available_seats, seat_count)

            price = self.cinema_info[room]["Price"] * len(chosen_seats)

            # import here to avoid circular import
            from untitled_update import confirm_order

            # create order using EXISTING function
            confirm_order(
                chosen_room=room,
                chosen_time=time_id,
                price=price,
                seats=chosen_seats,
                tid=None,
                marker_for_booked_seats="X"
            )
