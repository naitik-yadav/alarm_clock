import pytest
import os
from datetime import time
from alarm_clock.alarm import Alarm, parse_time
from alarm_clock.scheduler import Scheduler


@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Clean up test JSON files before and after each test."""
    if os.path.exists("test_alarms.json"):
        os.remove("test_alarms.json")
    if os.path.exists("test_cli_alarms.json"):
        os.remove("test_cli_alarms.json")
    Alarm._id_counter = 1
    yield
    if os.path.exists("test_alarms.json"):
        os.remove("test_alarms.json")
    if os.path.exists("test_cli_alarms.json"):
        os.remove("test_cli_alarms.json")
    Alarm._id_counter = 1


def test_valid_alarm_creation():
    """Test creating an alarm with valid time."""
    alarm_time = time(14, 30)
    alarm = Alarm(alarm_time)
    assert alarm.time == alarm_time
    assert alarm.id == 1


def test_multiple_alarms():
    """Test creating multiple alarms with incrementing IDs."""
    Alarm._id_counter = 1  # Reset counter
    alarm1 = Alarm(time(9, 0))
    alarm2 = Alarm(time(10, 0))
    assert alarm1.id == 1
    assert alarm2.id == 2


def test_parse_time_valid():
    """Test parsing valid time strings."""
    assert parse_time("09:15") == time(9, 15)
    assert parse_time("23:59") == time(23, 59)
    assert parse_time("00:00") == time(0, 0)


def test_parse_time_invalid_format():
    """Test parsing invalid time formats."""
    assert parse_time("9:15") is None  # Missing leading zero
    assert parse_time("09:15:30") is None  # Seconds included
    assert parse_time("invalid") is None
    assert parse_time("") is None


def test_parse_time_invalid_range():
    """Test parsing times with invalid hour/minute ranges."""
    assert parse_time("25:00") is None  # Invalid hour
    assert parse_time("09:60") is None  # Invalid minute
    assert parse_time("-1:00") is None  # Negative hour


def test_scheduler_add_alarm():
    """Test adding alarm to scheduler."""
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    assert len(scheduler.list_alarms()) == 1
    assert scheduler.list_alarms()[0].id == alarm.id


def test_scheduler_list_alarms():
    """Test listing alarms from scheduler."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm1 = Alarm(time(9, 0))
    alarm2 = Alarm(time(10, 0))
    scheduler.add_alarm(alarm1)
    scheduler.add_alarm(alarm2)
    
    alarms = scheduler.list_alarms()
    assert len(alarms) == 2
    assert alarms[0].id == 1
    assert alarms[1].id == 2


def test_scheduler_cancel_alarm():
    """Test cancelling an existing alarm."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    
    result = scheduler.remove_alarm(alarm.id)
    assert result is True
    assert len(scheduler.list_alarms()) == 0


def test_scheduler_cancel_nonexistent_alarm():
    """Test cancelling a non-existent alarm."""
    scheduler = Scheduler(data_file="test_alarms.json")
    result = scheduler.remove_alarm(999)
    assert result is False


def test_scheduler_due_alarm_triggers():
    """Test that due alarm is detected."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    
    # Mock current time to match alarm time
    scheduler.get_current_time = lambda: time(14, 30)
    due_alarm = scheduler.check_alarms()
    
    assert due_alarm is not None
    assert due_alarm.id == alarm.id


def test_scheduler_inactive_alarm_not_triggering():
    """Test that cancelled alarms don't trigger."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    scheduler.remove_alarm(alarm.id)
    
    # Mock current time to match cancelled alarm time
    scheduler.get_current_time = lambda: time(14, 30)
    due_alarm = scheduler.check_alarms()
    
    assert due_alarm is None


def test_scheduler_no_due_alarm():
    """Test that no alarm is detected when time doesn't match."""
    Alarm._id_counter = 1
    scheduler = Scheduler(data_file="test_alarms.json")
    alarm = Alarm(time(14, 30))
    scheduler.add_alarm(alarm)
    
    # Mock current time to not match alarm time
    scheduler.get_current_time = lambda: time(15, 0)
    due_alarm = scheduler.check_alarms()
    
    assert due_alarm is None
