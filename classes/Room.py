class Room:
    def __init__(self, room_id, name, difficulty, duration, min_players, max_players, price_per_player, is_active=True):
        self.room_id = room_id
        self.name = name
        self.difficulty = difficulty
        self.duration = duration
        self.min_players = min_players
        self.max_players = max_players
        self.price_per_player = price_per_player
        self.is_active = is_active
    
    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False

    def is_valid_players(self, players):
        return self.min_players <= players <= self.max_players

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "name": self.name,
            "difficulty": self.difficulty,
            "duration": self.duration,
            "min_players": self.min_players,
            "max_players": self.max_players,
            "price_per_player": self.price_per_player,
            "is_active": self.is_active
        }
    @classmethod
    def dict_from(cls, data):
        return cls(
                room_id=data["room_id"],
                name=data["name"],
                difficulty=data["difficulty"],
                duration=data["duration"],
                min_players=data["min_players"],
                max_players=data["max_players"],
                price_per_player=data["price_per_player"],
                is_active=data["is_active"]
            )
