import datetime as dt
import logging

import streamlit as st
from dateutil.relativedelta import relativedelta

from happybarra.frontend.models.enums import CalendarDirection, WeekEndPolicy

__all__ = [
    "safe_date",
    "this_day_next_month",
    "weekend_check",
    "build_authorization_header",
]

_logger = logging.getLogger(__name__)


def safe_date(
    year, month, day, direction: CalendarDirection = CalendarDirection.DOWN
) -> dt.date:
    # validation for february
    if month == 2 and day in (30, 31, 29):
        # handle leap year if direction is down
        if year % 4 == 0 and day == 29 and direction == CalendarDirection.DOWN:
            day = 29

        # snap to 28 if not leap year
        elif direction == CalendarDirection.DOWN:
            day = 28

        # handle case when we want the date to move up the calendar
        else:
            month = 3
            day = 1

    # validation for months with 30
    if day == 31 and month in (4, 6, 9, 11):
        if direction == CalendarDirection.DOWN:
            day = 30
        else:
            month += 1
            day = 1

    target_date = dt.date(year, month, day)
    return target_date


def this_day_next_month(
    date: dt.date,
    day_of_month: int = None,
    direction: CalendarDirection = CalendarDirection.DOWN,
) -> dt.date:
    reference_day = day_of_month or date.day
    return safe_date(
        date.year, date.month, reference_day, direction=direction
    ) + relativedelta(months=1)


def weekend_check(reference_date: dt.date, policy: WeekEndPolicy) -> dt.date:
    day_offset: int = 0
    weekday = reference_date.weekday()
    if weekday in {5, 6}:
        if policy == WeekEndPolicy.PREV_BANK_DAY:
            day_offset = -1 * (weekday - 4)
        elif policy == WeekEndPolicy.NEXT_BANK_DAY:
            day_offset = 7 - weekday
    return reference_date + dt.timedelta(days=day_offset)


def build_authorization_header() -> dict:
    access_token = st.session_state.get("login__access_token", None)
    header = {"Authorization": f"Bearer {access_token}"}
    return header
