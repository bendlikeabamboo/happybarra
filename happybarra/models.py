import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List
from functools import partial
from typing import ClassVar, TypeVar

from happybarra.enums import (
    DueDateType,
    InstallmentAmountType,
    InstallmentPolicy,
    WeekEndPolicy,
)
from happybarra.utils import safe_date, this_day_next_month, weekend_check

T = TypeVar('T')

def registry(registry_type):
    registry: dict = {}

    def decorated(*args):
        return registry.get(registry_type.__name__)(*args)

    def register(name: str = None):
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


def attach_registry(_class: TypeVar[T]) ->  TypeVar[T]:
    """
    Attach a registry to a class
    """

    def _add_to_registry(cls, _self):
        """Register the class instance to the registry"""
        cls.registry[_self.name] = _self

    def __post_init__(self, *args, **kwargs):
        """
        Hook for registering the instance to the registry
        """
        _class._add_to_registry(_class, self)
        if hasattr(_class, "__post_post_init__"):
            self.__post_post_init__(*args, **kwargs)

    _class.registry: ClassVar[dict] = {}
    _class._add_to_registry = _add_to_registry
    
    # put the original post init in a variable called post post init
    if hasattr(_class, "__post_init__"):
        _class.__post_post_init__ = _class.__post_init__

    # inject our own post init
    _class.__post_init__ = __post_init__

    return _class
    

@dataclass
@attach_registry
class Bank:
    name: str


@dataclass
@attach_registry
class Network:
    name: str


@dataclass
@attach_registry
class CreditCard:
    bank: str
    name: str
    network: str
    due_date_type: DueDateType = field(default=DueDateType.X_DAYS_AFTER)
    due_date_policy: WeekEndPolicy = field(default=WeekEndPolicy.NEXT_BANK_DAY)
    statement_policy: WeekEndPolicy = field(default=WeekEndPolicy.PREV_BANK_DAY)
    bill_post_policy: InstallmentPolicy = field(
        default=InstallmentPolicy.ON_STATEMENT_DAY
    )


@dataclass
class CreditCardInstance:
    credit_card: CreditCard
    due_date_ref: int
    statement_day: int
    due_date_ref: int
    statement_day: int

    def due_date(self, reference_date: dt.date) -> dt.date:
        if self.credit_card.due_date_type == DueDateType.X_DAYS_AFTER:
            return self._x_days_after(reference_date)
        if self.credit_card.due_date_type == DueDateType.XTH_OF_MONTH:
            raise NotImplementedError("Due date type not yet implemented")

    def statement_date(self, reference_date: dt.date):
        true_statement_date = safe_date(
            reference_date.year, reference_date.month, self.statement_day
        )

        # weekend_check the true statement_date
        weekend_checked_statement_date = weekend_check(
            true_statement_date, self.credit_card.statement_policy
        )

        if reference_date <= weekend_checked_statement_date:
            return weekend_checked_statement_date

        return self.statement_date(this_day_next_month(true_statement_date))

    def _x_days_after(self, reference_date: dt.date):
        # compute due date from statement date
        statement_date = self.statement_date(reference_date)
        due_date = statement_date + dt.timedelta(days=self.due_date_ref)

        # checks
        validated_due_date = weekend_check(due_date, self.credit_card.due_date_policy)
        return validated_due_date


@dataclass
class CreditCardCharge:
    credit_card_instance: CreditCardInstance
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
        dates: List[CreditCardCharge] = []
        next_charge: dt.date = start_date
        for _ in range(self.tenure):
            next_due_date = self.credit_card_instance.due_date(next_charge)
            next_statement_date = self.credit_card_instance.statement_date(next_charge)
            next_bill_post_date = next_charge

            charge = CreditCardCharge(
                self.credit_card_instance,
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
                self.credit_card_instance,
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

if __name__ == "__main__":
    bank = Bank("BankA")
    bank = Bank("BankB")
    print(Bank.registry)
    cc = CreditCard(Bank, "sample cc","Network")
    cci = CreditCardInstance(cc, 1,2)
    ccin = CreditCardInstallment(cci,3,dt.date(2025,3,7),500.00)
    print(ccin.get_charge_dates())