import pytest
import os
from datetime import time
from alarm_clock.alarm import Alarm
from alarm_clock.scheduler import Scheduler
from alarm_clock.cli import CLI
from io import StringIO
import sys


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test JSON files before and after each test."""
    if os.path.exists("test_cli_alarms.json"):
        os.remove("test_cli_alarms.json")
    Alarm._id_counter = 1
    yield
    if os.path.exists("test_cli_alarms.json"):
        os.remove("test_cli_alarms.json")
    Alarm._id_counter = 1


def test_cli_set_alarm_valid():
    """Test CLI set command with valid time."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    cli.run(["set", "14:30"])
    
    alarms = scheduler.list_alarms()
    assert len(alarms) == 1
    assert alarms[0].time == time(14, 30)


def test_cli_set_alarm_invalid_format():
    """Test CLI set command with invalid time format."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    # Capture stdout to check error message
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["set", "invalid"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Invalid time format" in output
    assert len(scheduler.list_alarms()) == 0


def test_cli_set_alarm_invalid_range():
    """Test CLI set command with invalid time range."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["set", "25:00"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Invalid time format" in output
    assert len(scheduler.list_alarms()) == 0


def test_cli_set_alarm_missing_args():
    """Test CLI set command with missing time argument."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["set"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Usage: set HH:MM" in output


def test_cli_list_alarms():
    """Test CLI list command with alarms."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    scheduler.add_alarm(Alarm(time(9, 0)))
    scheduler.add_alarm(Alarm(time(10, 0)))
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["list"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Alarms:" in output
    assert "Alarm(id=1, time=09:00)" in output
    assert "Alarm(id=2, time=10:00)" in output


def test_cli_list_empty():
    """Test CLI list command with no alarms."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["list"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "No alarms set" in output


def test_cli_cancel_alarm():
    """Test CLI cancel command with valid ID."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["cancel", "1"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Alarm 1 cancelled" in output
    assert len(scheduler.list_alarms()) == 0


def test_cli_cancel_nonexistent_alarm():
    """Test CLI cancel command with non-existent ID."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["cancel", "999"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Alarm 999 not found" in output


def test_cli_cancel_invalid_id():
    """Test CLI cancel command with invalid ID format."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["cancel", "invalid"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Invalid alarm ID" in output


def test_cli_cancel_missing_args():
    """Test CLI cancel command with missing ID argument."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["cancel"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Usage: cancel <alarm_id>" in output


def test_cli_unknown_command():
    """Test CLI with unknown command."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run(["unknown"])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Unknown command: unknown" in output
    assert "Usage:" in output


def test_cli_no_args():
    """Test CLI with no arguments."""
    scheduler = Scheduler(data_file="test_cli_alarms.json")
    cli = CLI(scheduler)
    
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    
    cli.run([])
    
    output = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "Usage:" in output
