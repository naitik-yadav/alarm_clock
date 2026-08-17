import re
from datetime import time
from typing import Optional


class Alarm:
    _id_counter = 1

    def __init__(self, alarm_time: time):
        self.id = Alarm._id_counter
        Alarm._id_counter += 1
        self.time = alarm_time

    def __repr__(self):
        return f"Alarm(id={self.id}, time={self.time.strftime('%H:%M')})"


def parse_time(time_str: str) -> Optional[time]:
    """Parse HH:MM format and return time object. Returns None if invalid."""
    if not re.match(r'^\d{2}:\d{2}$', time_str):
        return None
    
    try:
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            return None
        return time(hour, minute)
    except ValueError:
        return None
