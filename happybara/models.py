from dataclasses import dataclass, field
import datetime as dt
from enum import Enum
from decimal import Decimal
from typing import List


class DueDateType(Enum):
    X_DAYS_AFTER = 1
    XTH_OF_MONTH = 2


class InstallmentAmountType(Enum):
    MONTHLY_FIXED = 1
    TOTAL_FIXED = 2


class WeekEndPolicy(Enum):
    PREV_BANK_DAY = -1
    NEXT_BANK_DAY = 2


class InstallmentPolicy(Enum):
    ON_STATEMENT_DAY = 1
    ON_PURCHASE_DAY = 2


class CalendarDirection(Enum):
    UP = 1
    DOWN = -1


def safe_date(year, month, day, direction: CalendarDirection = CalendarDirection.DOWN):
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


@dataclass
class CreditCard:
    bank: str
    name: str
    network: str
    due_date_ref: int
    statement_day: int
    due_date_type: DueDateType = field(default=DueDateType.X_DAYS_AFTER)
    due_date_policy: WeekEndPolicy = field(default=WeekEndPolicy.NEXT_BANK_DAY)
    statement_policy: WeekEndPolicy = field(default=WeekEndPolicy.PREV_BANK_DAY)

    def due_date(self, reference_date: dt.date) -> dt.date:
        if self.due_date_type == DueDateType.X_DAYS_AFTER:
            return self._x_days_after(reference_date)
        if self.due_date_type == DueDateType.XTH_OF_MONTH:
            raise NotImplementedError("Due date type not yet implemented")

    def statement_date(self, reference_date: dt.date):
        true_statement_date = safe_date(
            reference_date.year, reference_date.month, self.statement_day
        )

        # weekend_check the true statement_date
        weekend_checked_statement_date = weekend_check(
            true_statement_date, self.statement_policy
        )

        if reference_date <= weekend_checked_statement_date:
            return weekend_checked_statement_date

        return self.statement_date(this_day_next_month(true_statement_date))

    def _x_days_after(self, reference_date: dt.date):
        # compute due date from statement date
        statement_date = self.statement_date(reference_date)
        due_date = statement_date + dt.timedelta(days=self.due_date_ref)

        # checks
        validated_due_date = weekend_check(due_date, self.due_date_policy)
        return validated_due_date


@dataclass
class CreditCardCharge:
    amount: Decimal
    bill_post_date: dt.date
    statement_date: dt.date
    due_date: dt.date


@dataclass
class CreditCardInstallment:
    credit_card: CreditCard
    tenure: int
    start_date: dt.date
    policy: InstallmentPolicy  # place this on cc attribute
    amount: Decimal
    amount_type: InstallmentAmountType

    def __post_init__(self):
        if self.amount_type == InstallmentAmountType.MONTHLY_FIXED:
            self._monthly_amount = self.amount
            self._total_amount = self.amount * self.tenure
        elif self.amount_type == InstallmentAmountType.TOTAL_FIXED:
            self._total_amount = self.amount
            self._monthly_amount = self.amount / self.tenure

    def get_charge_dates(self):
        if self.policy == InstallmentPolicy.ON_PURCHASE_DAY:
            self.charges = self._get_dates_on_purchase(self.start_date)
        elif self.policy == InstallmentPolicy.ON_STATEMENT_DAY:
            self.charges = self._get_dates_on_statement(self.start_date)
        return self.charges

    def _get_dates_on_purchase(self, start_date: dt.date):
        dates: List[CreditCardCharge] = []
        next_charge: dt.date = start_date
        for _ in range(self.tenure):
            next_due_date = self.credit_card.due_date(next_charge)
            next_statement_date = self.credit_card.statement_date(next_charge)
            next_bill_post_date = next_charge

            charge = CreditCardCharge(
                self._monthly_amount,
                next_bill_post_date,
                next_statement_date,
                next_due_date,
            )
            dates.append(charge)

            next_charge = this_day_next_month(
                next_charge, self.credit_card.statement_day
            )
        return dates

    def _get_dates_on_statement(self, start_date: dt.date): ...


if __name__ == "__main__":
    print("Hello world")
