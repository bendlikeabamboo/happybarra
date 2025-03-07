import datetime as dt

from happybarra.enums import CalendarDirection, WeekEndPolicy


def safe_date(
    year, month, day, direction: CalendarDirection = CalendarDirection.DOWN
) -> dt.date:
    date_valid: bool = False
    day_offset = 0
    while not date_valid:
        try:
            target_date = dt.date(year, month, day + (day_offset * direction.value))
            date_valid = True
        except ValueError:
            day_offset += 1
            date_valid = False
    return target_date


def this_day_next_month(
    date: dt.date,
    day_of_month: int = None,
    direction: CalendarDirection = CalendarDirection.DOWN,
) -> dt.date:
    reference_day = day_of_month or date.day
    return safe_date(date.year, date.month + 1, reference_day, direction=direction)


def weekend_check(reference_date: dt.date, policy: WeekEndPolicy) -> dt.date:
    day_offset: int = 0
    weekday = reference_date.weekday()
    if weekday in {5, 6}:
        if policy == WeekEndPolicy.PREV_BANK_DAY:
            day_offset = -1 * (weekday - 4)
        elif policy == WeekEndPolicy.NEXT_BANK_DAY:
            day_offset = 7 - weekday
    return reference_date + dt.timedelta(days=day_offset)
