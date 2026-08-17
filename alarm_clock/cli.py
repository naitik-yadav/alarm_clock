import sys
from alarm_clock.alarm import Alarm, parse_time
from alarm_clock.scheduler import Scheduler


class CLI:
    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def run(self, args: list[str]) -> None:
        if not args:
            self.print_usage()
            return

        command = args[0]

        if command == "set":
            self.set_alarm(args[1:])
        elif command == "list":
            self.list_alarms()
        elif command == "cancel":
            self.cancel_alarm(args[1:])
        else:
            print(f"Unknown command: {command}")
            self.print_usage()

    def set_alarm(self, args: list[str]) -> None:
        if len(args) != 1:
            print("Usage: set HH:MM")
            return

        time_str = args[0]
        alarm_time = parse_time(time_str)

        if alarm_time is None:
            print(f"Invalid time format: {time_str}. Use HH:MM format (00:00 - 23:59)")
            return

        alarm = Alarm(alarm_time)
        self.scheduler.add_alarm(alarm)
        print(f"Alarm set: {alarm}")

    def list_alarms(self) -> None:
        alarms = self.scheduler.list_alarms()
        if not alarms:
            print("No alarms set")
            return

        print("Alarms:")
        for alarm in alarms:
            print(f"  {alarm}")

    def cancel_alarm(self, args: list[str]) -> None:
        if len(args) != 1:
            print("Usage: cancel <alarm_id>")
            return

        try:
            alarm_id = int(args[0])
        except ValueError:
            print(f"Invalid alarm ID: {args[0]}")
            return

        if self.scheduler.remove_alarm(alarm_id):
            print(f"Alarm {alarm_id} cancelled")
        else:
            print(f"Alarm {alarm_id} not found")

    def print_usage(self) -> None:
        print("Usage:")
        print("  set HH:MM    - Set an alarm")
        print("  list         - List all alarms")
        print("  cancel <id>  - Cancel an alarm by ID")
