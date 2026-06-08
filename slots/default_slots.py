"""Default weekly consultation slot patterns for local/dev seeding."""
from datetime import time

from slots.models import SlotType, Weekday

_DEFAULT_TIMES = (
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)),
    (time(14, 0), time(15, 0)),
    (time(15, 0), time(16, 0)),
    (time(16, 0), time(17, 0)),
)

_SATURDAY_TIMES = (
    (time(10, 0), time(11, 0)),
    (time(11, 0), time(12, 0)),
    (time(12, 0), time(13, 0)),
)

DEFAULT_SLOTS = [
    *((
        weekday,
        start_time,
        end_time,
        SlotType.BOTH,
    ) for weekday in (
        Weekday.MONDAY,
        Weekday.TUESDAY,
        Weekday.WEDNESDAY,
        Weekday.THURSDAY,
        Weekday.FRIDAY,
    ) for start_time, end_time in _DEFAULT_TIMES),
    *((
        Weekday.SATURDAY,
        start_time,
        end_time,
        SlotType.BOTH,
    ) for start_time, end_time in _SATURDAY_TIMES),
]
