from orders import calculate_total_price

class PricingManager:
    def calculate_price(self, room, players, booking_date):
        base_price = players * room.price_per_player
        if 5 <= players <= 6:
            discounted_price = base_price * 0.90 
        elif players >= 7:
            discounted_price = base_price * 0.85 
        else:
            discounted_price = base_price        
        booking_date = datetime.strptime(booking_date_str, "%Y-%m-%d").date()
        is_weekend = booking_date.weekday() in (4, 5)
        if is_weekend:
            final_price = discounted_price * 1.15
        else:
            final_price = discounted_price
        return round(final_price, 2)
    
    def calculate_cancellation_fee(self, booking, current_datetime):
        game_datetime = datetime.strptime(f"{booking.booking_date} {booking.start_time}", "%Y-%m-%d %H:%M")
        if game_datetime <= current_datetime:
            return -1
        time_diff = game_datetime - current_datetime
        hours_left = time_diff.total_seconds() / 3600
        if hours_left > 24:
            return 0.0
        elif 6 <= hours_left <= 24:
            return round(booking.total_price * 0.25, 2)
        else:
            return round(booking.total_price * 0.50, 2)
