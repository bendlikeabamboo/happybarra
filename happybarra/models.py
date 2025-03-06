import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List

from happybarra.enums import (
    DueDateType,
    InstallmentAmountType,
    InstallmentPolicy,
    WeekEndPolicy,
)
from happybarra.utils import safe_date, this_day_next_month, weekend_check


@dataclass
class Bank:
    name: str


@dataclass
class Network:
    name: str


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
    amount: Decimal
    policy: InstallmentPolicy = field(
        default=InstallmentPolicy.ON_PURCHASE_DAY
    )  # place this on cc attribute
    amount_type: InstallmentAmountType = field(
        default=InstallmentAmountType.MONTHLY_FIXED
    )

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
                next_statement_date, self.credit_card.statement_day
            )
        return dates

    def _get_dates_on_statement(self, start_date: dt.date): ...
