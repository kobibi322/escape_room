from datetime import datetime


def validate_int(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        raise ValueError("Must be an integer!")

def validate_float(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        raise ValueError("Must be a number!")

def validate_positive(num: int | float) -> int | float:
    if num <= 0:
        raise ValueError("Must be a positive number!")
    return num

def validate_name(text: str) -> str:
    if not text:
        raise ValueError("Cannot be empty!")
    return text        

def validate_difficulty(text: str) -> bool:
    DIFFICULTY = ("Easy", "Medium", "Hard")
    if text not in DIFFICULTY:
        raise ValueError("Must be Easy, Medium or Hard!")
    return text
    
def validate_booking(date_str: str, time_str: str) -> tuple[str, str]:
    try:
        booking_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        if booking_datetime < datetime.now():
            raise ValueError("Cannot book a game in the past!")
        return date_str, time_str
    except ValueError as e:
        raise ValueError(e)

def validate_booking_date(user_input: str) -> str:
    try:
        parts = user_input.strip().split(" ")
        if len(parts) != 2:
            raise ValueError("Format must be YYYY-MM-DD HH:MM")
        date_str, time_str = parts
        validate_booking(date_str, time_str)
        return user_input.strip()
    except Exception as e:
        raise ValueError(f"Invalid date/time format or past date: {e}")