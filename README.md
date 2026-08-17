# alarm_clock

A small command-line alarm clock. Python standard library only (`pytest` for tests).

## Usage

```bash
python -m alarm_clock set 07:30 --label gym   # set an alarm (24h HH:MM)
python -m alarm_clock list                    # list alarms with their ids
python -m alarm_clock cancel 1                # cancel by id
python -m alarm_clock run                     # run the scheduler until Ctrl+C
```

`run` stays in the foreground and prints a line plus a terminal bell when an alarm
is due; the alarm is then removed. Alarms are stored in `~/.alarm_clock/alarms.json`
(override with `--store PATH`), so `set` and `run` can be different invocations.

## Layout

| File | Responsibility |
| --- | --- |
| `alarm_clock/alarm.py` | `Alarm` model, `parse_time` validation, `AlarmStore` persistence |
| `alarm_clock/scheduler.py` | `due_alarms` (pure) and the polling `run` loop |
| `alarm_clock/cli.py` | argparse commands, output, exit codes |
| `alarm_clock/__main__.py` | `python -m alarm_clock` entry point |

## Design notes

- Core logic is separate from the CLI: `alarm.py` and `scheduler.py` never print or
  parse arguments, and `cli.py` holds no scheduling logic.
- Timing is testable without waiting: `Alarm.next_trigger(now)` and
  `due_alarms(alarms, since, now)` take timestamps as parameters, and `run` accepts
  injected `now_fn` / `sleep_fn`.
- A time that has already passed today rolls over to tomorrow.
- Invalid times are rejected with exit code 2; an unknown cancel id exits 1.
- `Ctrl+C` during `run` exits cleanly.

## Tests

```bash
pip install -r requirements.txt
python -m pytest
```

## Not implemented (deliberately)

Recurring/weekday alarms, snooze, background daemon or cron integration, timezones,
and audio playback.
