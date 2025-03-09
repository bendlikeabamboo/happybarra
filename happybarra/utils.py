import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import TypeVar
from functools import wraps

from happybarra.enums import CalendarDirection, WeekEndPolicy

T = TypeVar("T")


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


def registry(registry_type):
    registry: dict = {}

    def decorated(*args):
        return registry.get(registry_type.__name__)(*args)

    def register(name: str = ""):
        def inner(callable_):
            class_name = name or callable_.__name__
            parametrized_callable_ = partial(callable_, class_name)
            registry[class_name] = parametrized_callable_
            print("New process type registered: {class_name}")
            return parametrized_callable_

        return inner

    decorated.register = register
    decorated.registry = registry
    return decorated


def instance_registry(cls: T) -> T:
    "Attach a registry to a class"

    # save the original init method to a variable
    original_init = cls.__init__

    # declare an empty registry
    cls.registry = dict()

    # new init method that registers the instance, yey
    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        cls.registry[self.name] = self

    # replace init with new init method
    cls.__init__ = new_init
    cls.__annotations__["registry"] = dict
    return cls
