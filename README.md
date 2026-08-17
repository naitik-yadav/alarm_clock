# Alarm Clock

A simple command-line alarm clock application written in Python. Set, list, and cancel alarms with an easy-to-use CLI interface.

## Features

- Set alarms using HH:MM format
- List all active alarms
- Cancel alarms by ID
- Persistent alarm storage (JSON file)
- Graceful Ctrl+C handling
- Time validation
- Multiple alarm support

## Requirements

- Python 3.14+
- No external dependencies (uses Python standard library only)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd alarm_clock
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Set an alarm
```bash
python -m alarm_clock set 14:30
```

### List all alarms
```bash
python -m alarm_clock list
```

### Cancel an alarm by ID
```bash
python -m alarm_clock cancel 1
```

### Run the scheduler
```bash
python -m alarm_clock
```
The scheduler will check for due alarms every second and notify when an alarm triggers. Press Ctrl+C to exit.

## Time Format

Alarms must be set in HH:MM format (24-hour):
- Valid: `09:15`, `23:59`, `00:00`
- Invalid: `9:15` (missing leading zero), `25:00` (invalid hour), `09:60` (invalid minute)

## Testing

Install pytest:
```bash
pip install pytest
```

Run tests:
```bash
pytest tests/
```

Run tests with coverage:
```bash
pytest tests/ -v
```

## Project Structure

```
alarm_clock/
├── alarm_clock/
│   ├── __init__.py
│   ├── __main__.py      # Entry point
│   ├── alarm.py         # Alarm class and time validation
│   ├── cli.py           # Command-line interface
│   └── scheduler.py     # Alarm scheduling and persistence
├── tests/
│   ├── test_alarm.py    # Core logic tests
│   └── test_cli.py      # CLI tests
├── requirements.txt
└── README.md
```

## Implementation Notes

- Alarms are persisted in `alarms.json` in the project directory
- Each alarm has a unique ID that auto-increments
- The scheduler checks for due alarms by comparing current time (hour/minute) with alarm times
- Tests use dependency injection to mock time for deterministic testing