"""Scheduling logic: a pure due-check plus a loop with injected clock/sleep."""

import time
from datetime import datetime

from .alarm import Alarm

POLL_SECONDS = 1.0


def due_alarms(alarms: list[Alarm], since: datetime, now: datetime) -> list[Alarm]:
    """Alarms whose trigger time falls in the window (since, now].

    Pure function: tests pass timestamps instead of waiting on the clock.
    """
    return [a for a in alarms if since < a.next_trigger(since) <= now]


def run(store, notify, now_fn=datetime.now, sleep_fn=time.sleep) -> None:
    """Poll the store and notify for every alarm that becomes due.

    `now_fn` and `sleep_fn` are injected so the loop can be driven
    deterministically in tests; a StopIteration from either ends the loop.
    """
    since = now_fn()
    while True:
        try:
            sleep_fn(POLL_SECONDS)
            now = now_fn()
        except StopIteration:
            return
        for alarm in due_alarms(store.reload(), since, now):
            notify(alarm)
            store.cancel(alarm.id)
        since = now
