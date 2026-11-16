from datetime import datetime, timedelta
from data import load_rooms, load_orders, dump_orders
from rooms import id_maker
from validations import validate_int, validate_positive, validate_booking_date

def print_orders_menu():
    print("""
---------- ORDERS MANAGEMENT ----------
1. Create New Order
2. Show All Orders
3. Search Order By ID
4. Show Orders By Customer Name
5. Show Orders By Date
6. Update Order Details
7. Cancel Order
8. Back to Main Menu
""")

def check_operating_hours(start_time_str: str, duration_minutes: int):
    start_dt = datetime.strptime(start_time_str, "%H:%M")
    end_dt = start_dt + timedelta(minutes=duration_minutes + 15)
    opening = datetime.strptime("10:00", "%H:%M").time()
    closing = datetime.strptime("22:00", "%H:%M").time()
    if start_dt.time() < opening or end_dt.time() > closing:
        raise ValueError("Operating hours are 10:00 to 22:00.")

def check_room_availability(room_id: str, date_str: str, start_time_str: str, ignore_booking_id: str = None) -> bool:
    rooms = load_rooms()
    room_duration = 0
    for room in rooms:
        if room["room_id"] == room_id:
            room_duration = room["duration"]
    orders = load_orders()
    new_start = datetime.strptime(f"{date_str} {start_time_str}", "%Y-%m-%d %H:%M")
    new_end = new_start + timedelta(minutes=duration + 15)
    for order in orders:
        if order.get("status") == "Cancelled" or order["room_id"] != room_id or order["booking_date"] != date_str:
            continue
        if ignore_booking_id and order["booking_id"] == ignore_booking_id:
            continue
        existing_start = datetime.strptime(f"{order['booking_date']} {order['start_time']}", "%Y-%m-%d %H:%M")
        existing_end = existing_start + timedelta(minutes=room_duration + 15)
        if new_start < existing_end and new_end > existing_start:
            return False      
    return True

def make_order():
    rooms = load_rooms()
    if not rooms:
        print("No rooms available for booking.")
        return
    print("\n--- Available Active Rooms ---")
    active_rooms = []
    for r in rooms:
        if r.get("is_active", True):
            active_rooms.append(r)
    if not active_rooms:
        print("No active rooms available right now.")
        return
    for r in active_rooms:
        print(f"ID: {r['room_id']}, Name: {r['name']}, Duration: {r['duration']}min,  Players: {r['min_players']}-{r['max_players']}, Price for player: {r['price_per_player']}")      
    room_id = in56put("\nEnter Room ID to book: ").strip()
    target_room = None
    for r in active_rooms:
        if r["room_id"] == room_id:
            target_room = r
            break    
    if not target_room:
        print("Room not found or not active!")
        return    
    customer_name = input("Enter customer name: ").strip()
    if not customer_name:
        print("Customer name cannot be empty!")
        return    
    while True:
        try:
            user_time = validate_booking_date(input("Enter booking date and start time (YYYY-MM-DD HH:MM): ").strip())
            booking_date, start_time = user_time.split(" ")
            check_operating_hours(start_time, target_room["duration"])
            if not check_room_availability(room_id, booking_date, start_time, target_room["duration"]):
                print("Time slot is not available due to another booking!")
                continue
            break
        except ValueError as e:
            print(f"Error: {e} Try again.")      
    while True:
        try:
            players_text = input(f"Enter number of players ({target_room['min_players']}-{target_room['max_players']}): ").strip()
            players = validate_positive(validate_int(players_text))
            if players < target_room["min_players"] or players > target_room["max_players"]:
                raise ValueError(f"Players must be between {target_room['min_players']} and {target_room['max_players']}!")
            break
        except ValueError as e:
            print(f"Error: {e} Try again.")
    total_price = calculate_total_price(target_room["price_per_player"], players, booking_date_str)
    new_order = {
        "booking_id": id_maker("B", "order"),
        "customer_name": customer_name,
        "room_id": room_id,
        "booking_date": booking_date,
        "start_time": start_time,
        "players": players,
        "duration": target_room["duration"],
        "total_price": total_price,
        "status": "Active",
        "cancellation_fee": 0.0
    }
    orders = load_orders()
    orders.append(new_order)
    dump_orders(orders)
    print(f"Order created successfully! Booking ID: {new_order['booking_id']}, Total Price: {total_price}₪")

def calculate_total_price(base_price_per_player: int, players: int, booking_date) -> float:
    base_price = players * base_price_per_player
    if 5 <= players <= 6:
        discounted_price = base_price * 0.90 
    elif players >= 7:
        discounted_price = base_price * 0.85 
    else:
        discounted_price = base_price        
    is_weekend = booking_date.weekday() in (4, 5)  
    if is_weekend:
        final_price = discounted_price * 1.15
    else:
        final_price = discounted_price
    return round(final_price, 2)

def show_all_orders():
    orders = load_orders()
    if not orders:
        print("\nNo orders found in the system.")
        return []
    print("\n--------- All Orders ---------")
    for order in orders:
        print(f"""
[ID: {order['booking_id']}] Customer: {order['customer_name']} | Room: {order['room_id']} 
Date: {order['booking_date']} at {order['start_time']} | Players: {order['players']} 
Price: {order['total_price']}₪ | Status: {order['status']} (Cancellation Fee: {order.get('cancellation_fee', 0.0)}₪)""")
    return orders

def show_order_by_id():
    orders = load_orders()
    if not orders:
        print("\nNo orders available.")
        return
    while True:
        booking_id = input("Enter Booking ID (e.g., B001): ").strip()
        target_order = None
        for o in orders:
            if o["booking_id"] == booking_id.capitalize():
                target_order = o
                break
        if target_order:
            print(f"""
--- Order Details ---
ID: {target_order['booking_id']}
Customer: {target_order['customer_name']}
Room ID: {target_order['room_id']}
Date: {target_order['booking_date']}
Start Time: {target_order['start_time']}
Players: {target_order['players']}
Total Price: {target_order['total_price']}₪
Status: {target_order['status']}
Cancellation Fee: {target_order.get('cancellation_fee', 0.0)}₪
""")
            return
        print("Order not found! Try again.")

def show_orders_by_customer():
    orders = load_orders()
    if not orders:
        print("\nNo orders available.")
        return
    name_query = input("Enter customer name to search: ").strip().lower()
    matching_orders = []
    for o in orders:
        if name_query in o['customer_name'].lower():
            matching_orders.append(o)    
    if not matching_orders:
        print(f"No orders found for customer matching '{name_query}'.")
        return
    print(f"\n--- Orders for '{name_query}' ---")
    for order in matching_orders:
        print(f"[ID: {order['booking_id']}] Room: {order['room_id']} | Date: {order['booking_date']} {order['start_time']} | Status: {order['status']}")

def show_orders_by_date():
    orders = load_orders()
    if not orders:
        print("\nNo orders available.")
        return
    date_query = input("Enter date (YYYY-MM-DD): ").strip()
    matching_orders = []
    for o in orders:
        if o['booking_date'] == date_query:
            matching_orders.append(o)
    if not matching_orders:
        print(f"No orders found on date {date_query}.")
        return
    print(f"\n--- Orders on {date_query} ---")
    for order in matching_orders:
        print(f"[ID: {order['booking_id']}] Customer: {order['customer_name']} | Room: {order['room_id']} | Time: {order['start_time']} | Status: {order['status']}")

def update_order():
    orders = load_orders()
    if not orders:
        print("\nNo orders available to update.")
        return
    booking_id = input("Enter Booking ID to update: ").strip()
    target_order = None
    for o in orders:
        if o["booking_id"].upper() == booking_id.upper():
            target_order = o
            break
    if not target_order:
        print("Order not found!")
        return
    if target_order["status"] == "Cancelled":
        print("Cannot update a cancelled order!")
        return
    original_data = target_order.copy()
    print(f"\nUpdating Order: {target_order['booking_id']} (Customer: {target_order['customer_name']})")
    print("Press Enter to keep current values.")
    rooms = load_rooms()
    room = None
    for r in rooms:
        if r["room_id"] == target_order["room_id"]:
            room = r
            break 
    if not room or not room.get("is_active", True):
        print("The room associated with this order is no longer active!")
        return
    booking_date = target_order["booking_date"]
    start_time = target_order["start_time"]
    new_datetime_input = input(f"Enter new date and start time (YYYY-MM-DD HH:MM) [{booking_date} {start_time}]: ").strip()
    if new_datetime_input:
        try:
            date_part, time_part = new_datetime_input.split(" ")
            new_dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
            if new_dt < datetime.now():
                raise ValueError("Cannot book a game in the past!")
            check_operating_hours(time_part, room["duration"])
            if not check_room_availability(room["room_id"], date_part, time_part, room["duration"], ignore_booking_id=target_order["booking_id"]):
                raise ValueError("Time slot is not available due to another booking!")
            booking_date = date_part
            start_time = time_part
        except ValueError as e:
            print(f"Error in date/time update: {e}.")
            target_order.update(original_data)
            return
    players_input = input(f"Enter new players count [{target_order['players']}]: ").strip()
    players = target_order["players"]
    if players_input:
        try:
            new_players = validate_positive(validate_int(players_input))
            if room and (new_players < room["min_players"] or new_players > room["max_players"]):
                raise ValueError(f"Players must be between {room['min_players']} and {room['max_players']}!")
            players = new_players
        except ValueError as e:
            print(f"Invalid input for players: {e} Update aborted.")
            target_order.update(original_data)
            return
    target_order["booking_date"] = booking_date
    target_order["start_time"] = start_time
    target_order["players"] = players
    target_order["total_price"] = calculate_total_price(room["price_per_player"], players, booking_date)
    dump_orders(orders)
    print("Order updated successfully!")

def cancel_order():
    orders = load_orders()
    if not orders:
        print("\nNo orders available.")
        return
    booking_id = input("Enter Booking ID to cancel: ").strip()
    target_order = None
    for o in orders:
        if o["booking_id"].upper() == booking_id.upper():
            target_order = o
            break
    if not target_order:
        print("Order not found!")
        return
    if target_order["status"] == "Cancelled":
        print("Order is already cancelled!")
        return
    game_datetime = datetime.strptime(f"{target_order['booking_date']} {target_order['start_time']}", "%Y-%m-%d %H:%M")
    now = datetime.now()
    if game_datetime <= now:
        print("Cannot cancel an order after the game start time!")
        return
    time_diff = game_datetime - now
    hours_left = time_diff.total_seconds() / 3600
    if hours_left > 24:
        cancellation_fee = 0.0
        print("Cancellation more than 24 hours in advance: No cancellation fee!")
    elif 6 <= hours_left <= 24:
        cancellation_fee = round(target_order["total_price"] * 0.25, 2)
        print(f"Cancellation between 6 and 24 hours: 25% fee ({cancellation_fee}₪).")
    else:
        cancellation_fee = round(target_order["total_price"] * 0.50, 2)
        print(f"Cancellation less than 6 hours: 50% fee ({cancellation_fee}₪).")
    target_order["status"] = "Cancelled"
    target_order["cancellation_fee"] = cancellation_fee
    dump_orders(orders)
    print(f"Order {target_order['booking_id']} cancelled successfully.")