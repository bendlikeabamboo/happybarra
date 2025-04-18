import datetime as dt
import logging
from dataclasses import dataclass, field
from decimal import Decimal
from functools import partial
from typing import List

from dateutil import relativedelta
from pydantic import BaseModel

from happybarra.frontend.models.enums import (
    DueDateType,
    InstallmentAmountType,
    InstallmentPolicy,
    WeekEndPolicy,
)
from happybarra.frontend.services.helpers import (
    instance_registry,
    safe_date,
    this_day_next_month,
    weekend_check,
)

_logger = logging.getLogger(__name__)


@instance_registry
class Bank(BaseModel):
    name: str


@instance_registry
@dataclass
class Network:
    name: str


@instance_registry
@dataclass
class CreditCard:
    bank: Bank
    name: str
    network: Network
    due_date_type: DueDateType = field(default=DueDateType.X_DAYS_AFTER)
    due_date_policy: WeekEndPolicy = field(default=WeekEndPolicy.NEXT_BANK_DAY)
    statement_policy: WeekEndPolicy = field(default=WeekEndPolicy.PREV_BANK_DAY)
    bill_post_policy: InstallmentPolicy = field(
        default=InstallmentPolicy.ON_PURCHASE_DAY
    )


@dataclass
class CreditCardInstance:
    credit_card: CreditCard
    due_date_ref: int
    statement_day: int

    def due_date(self, post_date: dt.date) -> dt.date:
        if self.credit_card.due_date_type == DueDateType.X_DAYS_AFTER:
            return self._x_days_after(post_date)
        if self.credit_card.due_date_type == DueDateType.XTH_OF_MONTH:
            raise NotImplementedError("Due date type not yet implemented")

    def statement_date(self, post_date: dt.date):
        # Let's first weekend_check the statement day on the posting month
        weekend_checked_statement_day = weekend_check(
            safe_date(post_date.year, post_date.month, self.statement_day),
            WeekEndPolicy.NEXT_BANK_DAY,
        ).day

        # If the posting day is within (i.e. less than) the validated statement day
        # then we select the statement day of the current month, else, get the statement
        # day of the next month
        if post_date.day <= weekend_checked_statement_day:
            return safe_date(
                post_date.year, post_date.month, weekend_checked_statement_day
            )
        return weekend_check(
            safe_date(post_date.year, post_date.month, self.statement_day)
            + relativedelta.relativedelta(months=1),
            WeekEndPolicy.NEXT_BANK_DAY,
        )

    def _x_days_after(self, reference_date: dt.date):
        # compute due date from statement date
        statement_date = self.statement_date(reference_date)
        due_date = statement_date + dt.timedelta(days=self.due_date_ref)

        # checks
        validated_due_date = weekend_check(due_date, self.credit_card.due_date_policy)
        return validated_due_date


@dataclass
class CreditCardCharge:
    credit_card_name: str
    amount: Decimal
    bill_post_date: dt.date
    statement_date: dt.date
    due_date: dt.date


@dataclass
class CreditCardInstallment:
    credit_card_instance: CreditCardInstance
    tenure: int
    start_date: dt.date
    amount: Decimal
    amount_type: InstallmentAmountType = field(
        default=InstallmentAmountType.MONTHLY_FIXED
    )

    def __post_init__(self):
        _logger.debug("Post initialization if credit card installment")
        if self.amount_type == InstallmentAmountType.MONTHLY_FIXED:
            self._monthly_amount = self.amount
            self._total_amount = self.amount * self.tenure
        elif self.amount_type == InstallmentAmountType.TOTAL_FIXED:
            self._total_amount = self.amount
            self._monthly_amount = self.amount / self.tenure

    def get_charge_dates(self):
        policy = self.credit_card_instance.credit_card.bill_post_policy
        if policy == InstallmentPolicy.ON_PURCHASE_DAY:
            self.charges = self._get_dates_on_purchase(self.start_date)
        elif policy == InstallmentPolicy.ON_STATEMENT_DAY:
            self.charges = self._get_dates_on_statement(self.start_date)
        return self.charges

    def _get_dates_on_purchase(self, start_date: dt.date):
        billing_dates: List[dt.date] = [
            weekend_check(
                start_date + relativedelta.relativedelta(months=nth),
                self.credit_card_instance.credit_card.bill_post_policy,
            )
            for nth in range(self.tenure)
        ]
        statement_dates: List[dt.date] = [
            weekend_check(
                self.credit_card_instance.statement_date(date),
                self.credit_card_instance.credit_card.statement_policy,
            )
            for date in billing_dates
        ]
        due_dates: List[dt.date] = [
            weekend_check(
                self.credit_card_instance.due_date(date),
                self.credit_card_instance.credit_card.statement_policy,
            )
            for date in billing_dates
        ]

        # partially filled-out charge
        pcharge = partial(
            CreditCardCharge,
            credit_card_name=self.credit_card_instance.credit_card.name,
            amount=self._monthly_amount,
        )

        charges: List[CreditCardCharge] = [
            pcharge(bill_post_date=bd, statement_date=sd, due_date=dd)
            for bd, sd, dd in zip(billing_dates, statement_dates, due_dates)
        ]

        return charges

    def _get_dates_on_statement(self, start_date: dt.date):
        dates: List[CreditCardCharge] = []

        next_charge: dt.date = start_date
        for idx in range(self.tenure):
            # If first month of the installment, use the bill post date as the next
            # charge. If not, use the statement date as the bill_post_date
            if idx == 0:
                next_bill_post_date = next_charge
            else:
                next_bill_post_date = self.credit_card_instance.statement_date(
                    next_charge
                )

            next_due_date = self.credit_card_instance.due_date(next_charge)
            next_statement_date = self.credit_card_instance.statement_date(next_charge)

            charge = CreditCardCharge(
                self.credit_card_instance.credit_card.name,
                self._monthly_amount,
                next_bill_post_date,
                next_statement_date,
                next_due_date,
            )

            dates.append(charge)
            next_charge = this_day_next_month(
                next_statement_date, self.credit_card_instance.statement_day
            )
        return dates
