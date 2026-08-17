import time as time_module
from alarm_clock.scheduler import Scheduler
from alarm_clock.cli import CLI


def main():
    scheduler = Scheduler()
    cli = CLI(scheduler)

    # Handle CLI commands first
    import sys
    if len(sys.argv) > 1:
        cli.run(sys.argv[1:])
        return

    # Run scheduler loop
    print("Alarm clock running. Press Ctrl+C to exit.")
    print("Use commands: set HH:MM, list, cancel <id>")

    try:
        while True:
            due_alarm = scheduler.check_alarms()
            if due_alarm:
                print(f"\nALARM! {due_alarm}")
                scheduler.remove_alarm(due_alarm.id)
            time_module.sleep(1)
    except KeyboardInterrupt:
        print("\nAlarm clock stopped.")


if __name__ == "__main__":
    main()
