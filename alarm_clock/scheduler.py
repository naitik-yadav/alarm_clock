import json
from datetime import datetime, time
from typing import Callable, List, Optional
from alarm_clock.alarm import Alarm


class Scheduler:
    def __init__(self, get_current_time: Callable[[], time] = None, data_file: str = "alarms.json"):
        self.alarms: List[Alarm] = []
        self.get_current_time = get_current_time or self._default_get_time
        self.data_file = data_file
        self._load_alarms()

    def _default_get_time(self) -> time:
        return datetime.now().time()

    def _load_alarms(self) -> None:
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                max_id = 0
                for alarm_data in data:
                    alarm_time = time(alarm_data['hour'], alarm_data['minute'])
                    alarm = Alarm(alarm_time)
                    alarm.id = alarm_data['id']
                    self.alarms.append(alarm)
                    if alarm.id > max_id:
                        max_id = alarm.id
                Alarm._id_counter = max_id + 1
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass

    def _save_alarms(self) -> None:
        data = []
        for alarm in self.alarms:
            data.append({
                'id': alarm.id,
                'hour': alarm.time.hour,
                'minute': alarm.time.minute
            })
        with open(self.data_file, 'w') as f:
            json.dump(data, f)

    def add_alarm(self, alarm: Alarm) -> None:
        self.alarms.append(alarm)
        self._save_alarms()

    def remove_alarm(self, alarm_id: int) -> bool:
        for i, alarm in enumerate(self.alarms):
            if alarm.id == alarm_id:
                self.alarms.pop(i)
                self._save_alarms()
                return True
        return False

    def list_alarms(self) -> List[Alarm]:
        return self.alarms.copy()

    def check_alarms(self) -> Optional[Alarm]:
        """Check if any alarm is due. Returns the alarm if due, None otherwise."""
        current_time = self.get_current_time()
        for alarm in self.alarms:
            if alarm.time.hour == current_time.hour and alarm.time.minute == current_time.minute:
                return alarm
        return None
