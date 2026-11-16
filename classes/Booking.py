class Booking:
    def __init__(self, booking_id, customer_name, room_id, booking_date, start_time, players, total_price, status="Active", cancellation_fee=0.0):
        self.booking_id = booking_id
        self.customer_name = customer_name
        self.room_id = room_id
        self.booking_date = booking_date
        self.start_time = start_time
        self.players = players
        self.total_price = total_price
        self.status = status
        self.cancellation_fee = cancellation_fee
    
    def cancel(self, fee):
        self.status = "Canceled"
        self.cancellation_fee = fee
    
    def update_details(self, booking_date, start_time, players, total_price):
        self.booking_date = booking_date
        self.start_time = start_time
        self.players = players
        self.total_price = total_price

    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "customer_name": self.customer_name,
            "room_id": self.room_id,
            "booking_date": self.booking_date,
            "start_time": self.start_time,
            "players": self.players,
            "total_price": self.total_price,
            "status": self.status,
            "cancellation_fee": self.cancellation_fee
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            booking_id=data["booking_id"],
            customer_name=data["customer_name"],
            room_id=data["room_id"],
            booking_date=data["booking_date"],
            start_time=data["start_time"],
            players=data["players"],
            total_price=data["total_price"],
            status=data["status"],
            cancellation_fee=data["cancellation_fee"]
        )