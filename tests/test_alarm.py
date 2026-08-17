from datetime import datetime

import pytest

from alarm_clock.alarm import Alarm, AlarmStore, InvalidTimeError, parse_time
from alarm_clock.scheduler import due_alarms


def test_parse_time_valid():
    assert parse_time("07:05") == (7, 5)
    assert parse_time(" 23:59 ") == (23, 59)


@pytest.mark.parametrize("value", ["", "7", "24:00", "07:60", "-1:00", "aa:bb", "07:05:00"])
def test_parse_time_invalid(value):
    with pytest.raises(InvalidTimeError):
        parse_time(value)


def test_next_trigger_later_today():
    alarm = Alarm(1, 9, 0)
    assert alarm.next_trigger(datetime(2026, 1, 1, 8, 0)) == datetime(2026, 1, 1, 9, 0)


def test_next_trigger_rolls_over_to_tomorrow():
    alarm = Alarm(1, 9, 0)
    assert alarm.next_trigger(datetime(2026, 1, 1, 9, 0)) == datetime(2026, 1, 2, 9, 0)


def test_due_alarms_uses_window_not_real_clock():
    alarms = [Alarm(1, 9, 0), Alarm(2, 10, 0)]
    since = datetime(2026, 1, 1, 8, 59, 59)
    now = datetime(2026, 1, 1, 9, 0, 1)
    assert [a.id for a in due_alarms(alarms, since, now)] == [1]


def test_store_add_list_cancel(tmp_path):
    store = AlarmStore(tmp_path / "alarms.json")
    first = store.add(9, 0, "gym")
    second = store.add(7, 30)

    assert [a.id for a in store.list()] == [second.id, first.id]
    assert store.cancel(first.id) is True
    assert store.cancel(first.id) is False
    assert AlarmStore(tmp_path / "alarms.json").list() == [second]
