import json
from pathlib import Path
from Room import Room
from Booking import Booking

class DataManager:
    def __init__(self, rooms_file="rooms.json", bookings_file="bookings.json"):
        base_path = Path(__file__).parent
        self.rooms_file = base_path / rooms_file
        self.bookings_file = base_path / bookings_file
    
    def load_rooms(self):
        try:
            with open(self.rooms_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Room.from_dict(d) for d in data] if data else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def load_bookings(self):
        try:
            with open(self.bookings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Booking.from_dict(d) for d in data] if data else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_rooms(self, rooms):
        try:
            data = [room.to_dict() for room in rooms]
            with open(self.rooms_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (TypeError, OSError) as e:
            print(f"Failed to save rooms: {e}")
            return False

    def save_bookings(self, bookings):
        try:
            data = [booking.to_dict() for booking in bookings]
            with open(self.bookings_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except (TypeError, OSError) as e:
            print(f"Failed to save bookings: {e}")
            return False