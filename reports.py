from datetime import datetime, timedelta
from data import load_rooms, load_orders

def print_reports_menu():
    print("""
---------- REPORTS MANAGEMENT ----------
1. Total Active Orders
2. Total Cancelled Orders
3. Total Revenue (Active Orders)
4. Total Cancellation Fees
5. Most Popular Room
6. Number of Orders per Room
7. Room Occupancy Rate on a Given Date
8. Back to Main Menu
""")


def show_active_orders_count():
    orders = load_orders()
    active = []
    for o in orders:
        if o.get("status") == "Active":
            active.append(o)
    print(f"\nTotal Active Orders: {len(active)}")

def show_cancelled_orders_count():
    orders = load_orders()
    cancelled = []
    for o in orders:
        if o.get("status") == "Cancelled":
            cancelled.append(o)
    print(f"\nTotal Cancelled Orders: {len(cancelled)}")

def show_active_revenue():
    orders = load_orders()
    revenue = 0
    for o in orders:
        if o.get("status") == "Active":
            revenue += o["total_price"]
    print(f"\nTotal Revenue from Active Orders: {revenue}₪")

def show_cancellation_fees_total():
    orders = load_orders()
    fees = 0
    for o in orders:
        if o.get("status") == "Cancelled":
            fees += o.get("cancellation_fee", 0.0)
    print(f"\nTotal Cancellation Fees Collected: {fees}₪")

def show_most_popular_room():
    orders = load_orders()
    rooms = load_rooms()
    if not rooms:
        print("\nNo rooms found.")
        return
    room_counts = {}
    room_names = {}
    for r in rooms:
        room_counts[r["room_id"]] = 0
        room_names[r["room_id"]] = r["name"]
    for o in orders:
        if o.get("status") == "Active" and o["room_id"] in room_counts:
            room_counts[o["room_id"]] += 1
    max_orders = 0
    for count in room_counts.values():
        if count > max_orders:
            max_orders = count
    if max_orders == 0:
        print("\nNo active orders to determine popular room.")
        return
    popular_rooms = []
    for rid, count in room_counts.items():
        if count == max_orders:
            popular_rooms.append(room_names[rid])
    print(f"\nMost Popular Room(s): {', '.join(popular_rooms)} with {max_orders} active order(s).")

def show_orders_per_room():
    orders = load_orders()
    rooms = load_rooms()
    if not rooms:
        print("\nNo rooms found.")
        return
    print("\n--- Orders per Room ---")
    for r in rooms:
        r_id = r["room_id"]
        total = 0
        active = 0
        cancelled = 0
        for o in orders:
            if o["room_id"] == r_id:
                total += 1
                if o.get("status") == "Active":
                    active += 1
                elif o.get("status") == "Cancelled":
                    cancelled += 1
        print(f"Room [{r_id}] {r['name']}: Total: {total} (Active: {active}, Cancelled: {cancelled})")

def show_room_occupancy_rate():
    rooms = load_rooms()
    if not rooms:
        print("\nNo rooms found.")
        return
    print("\n--- Rooms ---")
    for r in rooms:
        print(f"ID: {r['room_id']} | Name: {r['name']}")
    room_id = input("Enter Room ID: ").strip()
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    target_room = None
    for r in rooms:
        if r["room_id"] == room_id:
            target_room = r
            break
    if not target_room:
        print("Room not found!")
        return
    orders = load_orders()
    active_orders_count = 0
    for o in orders:
        if o["room_id"] == room_id and o["booking_date"] == date_str and o.get("status") == "Active":
            active_orders_count += 1
    game_duration_with_setup = target_room["duration"] + 15
    occupied_minutes = active_orders_count * game_duration_with_setup
    total_operating_minutes = 720
    occupancy_rate = (occupied_minutes / total_operating_minutes) * 100
    print(f"\nOccupancy rate for room {target_room['name']} on {date_str}: {occupancy_rate:.2f}% ({occupied_minutes} mins out of {total_operating_minutes} mins)")