# Movie Ticket Reservation System - Code Structure Overview:
# Main file: untitled_update.py

# Data Structures:
# - cinema_info: Dict of rooms (room_num -> {'Title': str, 'Price': int, 'Showtimes': {time_id: {'Time': str, 'Seats': list}}})
# - orders: Dict of TIDs (transaction IDs) to order details ({'Title', 'Room Number', 'Schedule', 'Seat(s)', 'Price', 'Time'})
# - max_seats: Int constant for max seats per showtime (default 50)

# Key Functions:
# - Selection Panels: select_room_panel, select_schedule_panel, select_seats_panel (handle input/validation for booking)
# - Management Panels: search_order_panel, update_order_panel, cancel_order_panel, view_all_orders_panel (CRUD for orders)
# - Utilities: mark_seats (update seat status), generate_TID (unique ID), confirm_order (finalize booking), display functions

# Globals:
# - current_menu_id: Int for menu navigation (1=room selection panel, 2=time selection panel, 3=seats selection panel)
# - exit: Bool to break out of panel loops

# Program Flow: Main while loop displays menu options; booking traverses selection panels (room -> time -> seats) sequentially using current_menu_id; management enters sub-menus for order operations (search, update, cancel, view with sorting/reversing).