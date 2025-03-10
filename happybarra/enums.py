from enum import Enum
from collections import namedtuple


class CalendarDirection(Enum):
    UP = 1
    DOWN = -1


class WeekEndPolicy(Enum):
    PREV_BANK_DAY = -1
    NEXT_BANK_DAY = 2


class DueDateType(Enum):
    X_DAYS_AFTER = 1
    XTH_OF_MONTH = 2


class InstallmentAmountType(Enum):
    MONTHLY_FIXED = 1
    TOTAL_FIXED = 2


class InstallmentPolicy(Enum):
    ON_STATEMENT_DAY = 1
    ON_PURCHASE_DAY = 2
