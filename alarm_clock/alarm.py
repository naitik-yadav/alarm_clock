"""Core domain: alarm model, time parsing, and the alarm store.

No CLI, no printing, no sleeping — everything here is testable in isolation.
"""

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_STORE_PATH = Path.home() / ".alarm_clock" / "alarms.json"


class InvalidTimeError(ValueError):
    """Raised when an alarm time string is not a valid HH:MM value."""


def parse_time(value: str) -> tuple[int, int]:
    """Parse 'HH:MM' into (hour, minute), rejecting anything else."""
    parts = value.strip().split(":")
    if len(parts) != 2:
        raise InvalidTimeError(f"invalid time '{value}': expected HH:MM")
    hour_text, minute_text = parts
    if not (hour_text.isdigit() and minute_text.isdigit()):
        raise InvalidTimeError(f"invalid time '{value}': expected digits, got '{value}'")
    hour, minute = int(hour_text), int(minute_text)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise InvalidTimeError(f"invalid time '{value}': out of range 00:00-23:59")
    return hour, minute


@dataclass(frozen=True)
class Alarm:
    id: int
    hour: int
    minute: int
    label: str = ""

    @property
    def time_str(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}"

    def next_trigger(self, now: datetime) -> datetime:
        """First datetime strictly after `now` when this alarm is due.

        `now` is a parameter, so scheduling can be tested without waiting.
        """
        candidate = now.replace(
            hour=self.hour, minute=self.minute, second=0, microsecond=0
        )
        if candidate <= now:
            candidate += timedelta(days=1)
        return candidate

    def to_dict(self) -> dict:
        return {"id": self.id, "hour": self.hour, "minute": self.minute,
                "label": self.label}

    @classmethod
    def from_dict(cls, data: dict) -> "Alarm":
        return cls(int(data["id"]), int(data["hour"]), int(data["minute"]),
                   str(data.get("label", "")))


class AlarmStore:
    """Holds alarms and persists them to a JSON file.

    A plain file keeps separate CLI invocations ('set' then 'run') working
    without a database.
    """

    def __init__(self, path: Path = DEFAULT_STORE_PATH):
        self.path = Path(path)
        self._alarms: list[Alarm] = self._read()

    def _read(self) -> list[Alarm]:
        if not self.path.exists():
            return []
        try:
            return [Alarm.from_dict(item) for item in json.loads(self.path.read_text())]
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            return []

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps([a.to_dict() for a in self._alarms], indent=2))
        os.replace(tmp, self.path)

    def list(self) -> "list[Alarm]":
        """Alarms sorted by time of day."""
        return sorted(self._alarms, key=lambda a: (a.hour, a.minute, a.id))

    def add(self, hour: int, minute: int, label: str = "") -> Alarm:
        alarm = Alarm(self._next_id(), hour, minute, label)
        self._alarms.append(alarm)
        self._write()
        return alarm

    def cancel(self, alarm_id: int) -> bool:
        """Remove an alarm by id; returns False if no such id."""
        remaining = [a for a in self._alarms if a.id != alarm_id]
        if len(remaining) == len(self._alarms):
            return False
        self._alarms = remaining
        self._write()
        return True

    def reload(self) -> "list[Alarm]":
        """Re-read from disk so a running scheduler sees new alarms."""
        self._alarms = self._read()
        return self.list()

    def _next_id(self) -> int:
        return max((a.id for a in self._alarms), default=0) + 1
