import json
from pathlib import Path

BASIC_PATH = Path(__file__).parent
rooms_path = BASIC_PATH / "rooms.json"
bookings_path = BASIC_PATH / "bookings.json"

def load_rooms():
    try: 
        with open(rooms_path, "r", encoding="utf-8") as js:
            data = json.load(js)
            return data if data else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def dump_rooms(rooms):
    try:
        with open(rooms_path, "w", encoding="utf-8") as js:
            json.dump(rooms, js, indent=2, ensure_ascii=False )
        print("Saved successfully!")    
        return True
    except (TypeError, OSError) as e:
        print(f"Failed to write file: {e}")
        return False

def load_orders():
    try: 
        with open(bookings_path, "r", encoding="utf-8") as js:
            data = json.load(js)
            return data if data else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def dump_orders(bookings):
    try:
        with open(bookings_path, "w", encoding="utf-8") as js:
            json.dump(bookings, js, indent=2, ensure_ascii=False )
        return True
    except (TypeError, OSError) as e:
        print(f"Failed to write file: {e}")
        return False