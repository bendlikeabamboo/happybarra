import datetime as dt
from dateutil.relativedelta import relativedelta
from typing import TypeVar
from functools import wraps

from happybarra.enums import CalendarDirection, WeekEndPolicy

T = TypeVar("T")


def safe_date(
    year, month, day, direction: CalendarDirection = CalendarDirection.DOWN
) -> dt.date:
    date_valid: bool = False
    day_offset = 0
    while not date_valid:
        try:
            target_date = dt.date(year, month, day) + dt.timedelta(
                days=day_offset * direction.value
            )
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
