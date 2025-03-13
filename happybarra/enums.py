from enum import Enum
from collections import namedtuple


class CalendarDirection(str, Enum):
    UP = "DOWN"
    DOWN = "DOWN"


class WeekEndPolicy(str, Enum):
    PREV_BANK_DAY = "PREV_BANK_DAY"
    NO_CHANGE = "NO_CHANGE"
    NEXT_BANK_DAY = "NEXT_BANK_DAY"


class DueDateType(str, Enum):
    X_DAYS_AFTER = "X_DAYS_AFTER"
    XTH_OF_MONTH = "XTH_OF_MONTH"


class InstallmentAmountType(str, Enum):
    MONTHLY_FIXED = "MONTHLY_FIXED"
    TOTAL_FIXED = "TOTAL_FIXED"


class InstallmentPolicy(str, Enum):
    ON_STATEMENT_DAY = "ON_STATEMENT_DAY"
    ON_PURCHASE_DAY = "ON_PURCHASE_DAY"
