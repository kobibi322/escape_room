from datetime import datetime, timedelta
from Booking import Booking
from Pricing_manager import PricingManager
from DataManager import DataManager

class BookingManager:
    def __init__(self, rooms, bookings):
        self.rooms = rooms
        self.bookings = bookings
        self.pricing_manager = PricingManager()

    def create_booking(self, customer_name, room_id, booking_date, start_time, players):
        target_room = None
        for r in self.rooms:
            if r.room_id == room_id:
                target_room = r
                break
        if not target_room:
            return False, "Room not found."
        if not target_room.is_active:
            return False, "Room is not active."
        if not target_room.is_valid_players(players):
            return False, f"Players count must be between {target_room.min_players} and {target_room.max_players}."
        booking_dt = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
        if booking_dt < datetime.now():
            return False, "Cannot book a game in the past."
        try:
            self.check_operating_hours(start_time, target_room.duration)
        except ValueError as e:
            return False, str(e)
        if not self.check_availability(target_room.room_id, booking_date, start_time, exclude_booking_id=None):
            return False, "Time slot is not available."
        total_price = self.pricing_manager.calculate_price(target_room, players, booking_date)
        booking_id = self.generate_booking_id()
        new_booking = Booking(
            booking_id=booking_id,
            customer_name=customer_name,
            room_id=room_id,
            booking_date=booking_date,
            start_time=start_time,
            players=players,
            total_price=total_price,
            status="Active",
            cancellation_fee=0.0
        )
        self.bookings.append(new_booking)
        data_mgr = DataManager()
        data_mgr.save_bookings(self.bookings)
        return True, f"Order created successfully! Booking ID: {booking_id}"

    def check_operating_hours(self, start_time_str, duration_minutes):
        start_dt = datetime.strptime(start_time_str, "%H:%M")
        end_dt = start_dt + timedelta(minutes=duration_minutes + 15)
        opening = datetime.strptime("10:00", "%H:%M").time()
        closing = datetime.strptime("22:00", "%H:%M").time()
        if start_dt.time() < opening or end_dt.time() > closing:
            raise ValueError("Operating hours are 10:00 to 22:00.")

    def generate_booking_id(self):
        if not self.bookings:
            return "B001"
        max_id = max(int(b.booking_id[1:]) for b in self.bookings)
        return f"B{max_id + 1:03d}"

    def check_availability(self, room_id, booking_date, start_time, exclude_booking_id=None):
        room_duration = 0
        for r in self.rooms:
            if r.room_id == room_id:
                room_duration = r.duration
                break
        new_start = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
        new_end = new_start + timedelta(minutes=room_duration + 15)
        for booking in self.bookings:
            if booking.status == "Cancelled" or booking.room_id != room_id or booking.booking_date != booking_date:
                continue
            if exclude_booking_id and booking.booking_id == exclude_booking_id:
                continue
            existing_start = datetime.strptime(f"{booking.booking_date} {booking.start_time}", "%Y-%m-%d %H:%M")
            existing_end = existing_start + timedelta(minutes=room_duration + 15)
            if new_start < existing_end and new_end > existing_start:
                return False      
        return True

    def get_booking(self, booking_id):
        for b in self.bookings:
            if b.booking_id.upper() == booking_id.upper():
                return b
        return None

    def get_customer_bookings(self, customer_name):
        result = []
        for b in self.bookings:
            if customer_name.lower() in b.customer_name.lower():
                result.append(b)
        return result

    def get_bookings_by_date(self, booking_date):
        result = []
        for b in self.bookings:
            if b.booking_date == booking_date:
                result.append(b)
        return result

    def update_booking(self, booking_id, booking_date, start_time, players):
        booking = self.get_booking(booking_id)     
        if not booking:
            return False, "Order not found!"
        if booking.status == "Cancelled":
            return False, "Cannot update a cancelled order!"
        room = None
        for r in rooms:
            if r.room_id == booking.room_id:
                room = r
                break 
        if not room or not room.is_active:
            return False, "The room associated with this order is no longer active!"
        if not room.is_valid_players(new_players):
            return False, f"Players must be between {room.min_players} and {room.max_players}."
        try:
            new_dt = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M")
            if new_dt < datetime.now():
                return False, "Cannot schedule in the past."
            self.check_operating_hours(new_time, room.duration)
            if not self.check_availability(room.room_id, new_date, new_time, room.duration, exclude_booking_id=booking_id):
                return False, "Time slot not available."
        except ValueError as e:
            return False, str(e)
        new_price = self.pricing_manager.calculate_price(room, new_players, new_date)
        booking.update_details(new_date, new_time, new_players, new_price)
        data_mgr = DataManager()
        data_mgr.save_bookings(self.bookings)
        return True, f"Order updated successfully! New Total: {new_price}₪"

    def cancel_order(self, booking_id, current_datetime):
        booking = self.get_booking(booking_id)
        if not booking:
            return False, "Order not found."
        if booking.status == "Cancelled":
            return False, "Order is already cancelled."
        if game_datetime <= current_datetime:
            return False, "Cannot cancel an order after the game start time!"
        fee = self.pricing_manager.calculate_cancellation_fee(booking, current_datetime)
        if fee == -1:
            return False, "Cannot cancel an order after the game start time."
        booking.cancel(fee)
        data_mgr = DataManager()
        data_mgr.save_bookings(self.bookings)
        return True, f"Order cancelled successfully. Cancellation fee: {fee}₪"