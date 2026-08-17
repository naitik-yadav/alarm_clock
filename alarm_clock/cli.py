"""CLI layer: argument parsing, output, exit codes. No scheduling logic here."""

import argparse
import sys
from pathlib import Path

from .alarm import DEFAULT_STORE_PATH, Alarm, AlarmStore, InvalidTimeError, parse_time
from .scheduler import run as run_scheduler


def notify(alarm: Alarm) -> None:
    label = f" {alarm.label}" if alarm.label else ""
    print(f"\a[ALARM] {alarm.time_str}{label}", flush=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="alarm_clock", description="Simple alarm clock")
    parser.add_argument("--store", type=Path, default=DEFAULT_STORE_PATH,
                        help="path to the alarms JSON file")
    sub = parser.add_subparsers(dest="command", required=True)

    set_cmd = sub.add_parser("set", help="set an alarm at HH:MM")
    set_cmd.add_argument("time", help="alarm time in 24h HH:MM format")
    set_cmd.add_argument("--label", default="", help="optional label")

    sub.add_parser("list", help="list alarms")

    cancel_cmd = sub.add_parser("cancel", help="cancel an alarm by id")
    cancel_cmd.add_argument("id", type=int)

    sub.add_parser("run", help="run the scheduler until Ctrl+C")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = AlarmStore(args.store)

    if args.command == "set":
        try:
            hour, minute = parse_time(args.time)
        except InvalidTimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        alarm = store.add(hour, minute, args.label)
        print(f"Alarm {alarm.id} set for {alarm.time_str}")
        return 0

    if args.command == "list":
        alarms = store.list()
        if not alarms:
            print("No alarms set.")
        for alarm in alarms:
            label = f"  {alarm.label}" if alarm.label else ""
            print(f"[{alarm.id}] {alarm.time_str}{label}")
        return 0

    if args.command == "cancel":
        if not store.cancel(args.id):
            print(f"error: no alarm with id {args.id}", file=sys.stderr)
            return 1
        print(f"Cancelled alarm {args.id}")
        return 0

    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        run_scheduler(store, notify)
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0
