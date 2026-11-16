from data import load_rooms, dump_rooms
from validations import validate_name, validate_difficulty, validate_positive, validate_int

def print_rooms_menu():
    print("""
----------- ROOMS MANAGEMENT -----------
1. Show All Rooms
2. Show Room By ID
3. Add New Room
4. Update Room
5. Change Room Status
6. Back
""")

# 1
def show_all_rooms():
    rooms = load_rooms()
    print("\n--------- Existing Rooms ---------")
    for room in rooms:
        print(f"""
[{room["room_id"]}] {room["name"]}: {room["difficulty"]}, {room["duration"]} min, from {room["min_players"]} to {room["max_players"]} players, Price per player: {room["price_per_player"]}, The room is{"" if room["is_active"] else " not"} active.""")

# 2
def show_room_by_id():
    rooms = load_rooms()
    not_found = True
    while not_found: 
        input_id = input("Enter ID: ")
        for room in rooms:
            if room["room_id"] == input_id:
                not_found = False
                print(f"""
[{room["room_id"]}] {room["name"]}: {room["difficulty"]}, {room["duration"]} min, from {room["min_players"]} to {room["max_players"]}, Price per player:{room["price_per_player"]}, The room is {"" if room["is_active"] else "not"} active. 
    """)        
                return
        print("Room not found!")


# 3
def add_new_room():
    room = make_room()
    rooms = load_rooms()
    rooms.append(room)
    dump_rooms(rooms)

def make_room():
    room = {}
    room["room_id"] = id_maker("R", "room")
    enter_name(room)
    enter_difficulty(room)
    enter_duration(room)
    enter_min_players(room)
    enter_max_players(room)
    enter_price(room)
    room["is_active"] = True
    return room

def id_maker(id_type, list_type):
    if list_type == "room":
        rooms = load_rooms()
        if not rooms:
            return f"{id_type}001"
        max_id = max(int(room["room_id"][1:]) for room in rooms)
    else:
        orders = load_orders()
        if not orders:
            return f"{id_type}001"
        max_id = max(int(order["booking_id"][1:]) for order in orders)
    return f"{id_type}{max_id + 1:03d}"

def enter_name(room):
    while True:
        try:
            val = input("Enter name: ").strip().capitalize()
            room["name"] = validate_name(val)
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

def enter_difficulty(room):
    while True:
        try:
            val = input("Enter difficulty (Easy, Medium, Hard): ").strip().capitalize()
            room["difficulty"] = validate_difficulty(val)
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

def enter_duration(room):
    while True:
        try:
            text = input("Enter duration: ").strip()
            room["duration"] = validate_positive(validate_int(text))
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

def enter_min_players(room):
    while True:
        try:
            text = input("Enter min players: ").strip()
            room["min_players"] = validate_positive(validate_int(text))
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

def enter_max_players(room):
    while True:
        try:
            text = input("Enter max players: ").strip()
            max_p = validate_positive(validate_int(text))
            if max_p < room["min_players"]:
                raise ValueError(f"Max players must be >= {room['min_players']}!")     
            room["max_players"] = max_p
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

def enter_price(room):
   while True:
        try:
            text = input("Enter price per player: ").strip()
            room["price_per_player"] = validate_positive(validate_int(text))
            break
        except ValueError as e:
            print(f"Error: {e} Try again. 😡")

# 4
def update_room():
    result = check_room()
    if not result:
        return
    target_room, rooms = result
    update_room_menu(target_room, rooms)   

def print_update(room):
    print(f"""
--- Updating Room: {room['name']} (ID: {room['room_id']}) ---
1. Update Name
2. Update Difficulty
3. Update Duration
4. Update Min Players
5. Update Max Players
6. Update Price per Player
7. Save and Return to Main Menu""")

def update_room_menu(target_room, rooms):       
    user_choice = ""
    while user_choice != "7":
        print_update(target_room)
        user_choice = input("Choose 1-7: ").strip()
        if user_choice == "1":
            enter_name(target_room)
        elif user_choice == "2":
            enter_difficulty(target_room)
        elif user_choice == "3":
            enter_duration(target_room)
        elif user_choice == "4":
           enter_min_players(target_room)
        elif user_choice == "5":
            enter_max_players(target_room)
        elif user_choice == "6":
            enter_price(target_room)
        elif user_choice == "7":
            dump_rooms(rooms)
        else:
            print("Must be 1-7! Try again!")

# 5
def change_room_status():
    result = check_room()
    if not result:
        return
    target_room, rooms = result
    target_room["is_active"] = not target_room["is_active"]
    dump_rooms(rooms)
    
def check_room():
    rooms = load_rooms()
    if not rooms:
        print("No rooms available to update.")
        return
    show_all_rooms()
    room_id_to_update = input("\nEnter the ID of the room to update (e.g., R001): ").strip()
    target_room = None
    for room in rooms:
        if room["room_id"] == room_id_to_update:
            target_room = room
            break
    if not target_room:
        print(f"Room with ID '{room_id_to_update}' not found!")
        return
    return target_room, rooms