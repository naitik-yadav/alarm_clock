from datetime import datetime, timedelta

import pytest

from alarm_clock.alarm import AlarmStore
from alarm_clock.cli import main
from alarm_clock.scheduler import run


@pytest.fixture
def store_path(tmp_path):
    return tmp_path / "alarms.json"


def test_set_list_cancel(store_path, capsys):
    assert main(["--store", str(store_path), "set", "07:30", "--label", "gym"]) == 0
    assert main(["--store", str(store_path), "list"]) == 0
    assert "[1] 07:30  gym" in capsys.readouterr().out

    assert main(["--store", str(store_path), "cancel", "1"]) == 0
    assert main(["--store", str(store_path), "list"]) == 0
    assert "No alarms set." in capsys.readouterr().out


def test_set_rejects_invalid_time(store_path, capsys):
    assert main(["--store", str(store_path), "set", "25:00"]) == 2
    assert "invalid time" in capsys.readouterr().err


def test_cancel_unknown_id(store_path, capsys):
    assert main(["--store", str(store_path), "cancel", "42"]) == 1
    assert "no alarm with id 42" in capsys.readouterr().err


def test_run_fires_due_alarm_without_waiting(store_path):
    store = AlarmStore(store_path)
    store.add(9, 0, "gym")

    start = datetime(2026, 1, 1, 8, 59, 59)
    times = iter([start, start + timedelta(seconds=2)])
    fired = []

    run(store, fired.append, now_fn=lambda: next(times), sleep_fn=lambda _: None)

    assert [a.label for a in fired] == ["gym"]
    assert store.reload() == []
