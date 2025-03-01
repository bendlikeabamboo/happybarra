from dataclasses import dataclass, field
import datetime as dt
from enum import Enum
from decimal import Decimal


class DueDateType(Enum):
    X_DAYS_AFTER = 1
    XTH_OF_MONTH = 2


class WeekendCheckPolicy(Enum):
    PREVIOUS_BUSINESS_DAY = -1
    NEXT_BUSINESS_DAY = 2


@dataclass
class CreditCard:
    bank: str
    name: str
    network: str
    due_date_type: DueDateType
    due_date_reference: int
    statement_day: int
    due_date_policy: WeekendCheckPolicy = field(default=WeekendCheckPolicy.NEXT_BUSINESS_DAY)
    statement_day_policy: WeekendCheckPolicy = field(default=WeekendCheckPolicy.PREVIOUS_BUSINESS_DAY)

    def next_payment(self, purchase_date: dt.date) -> dt.date:
        if self.due_date_type == DueDateType.X_DAYS_AFTER:
            return self._x_days_after(purchase_date)

    def _weekend_check(self, date: dt.date, policy: WeekendCheckPolicy) -> dt.date:
        day_offset: int = 0
        weekday = date.weekday()
        if weekday in {5, 6}:
            if policy == WeekendCheckPolicy.PREVIOUS_BUSINESS_DAY:
                day_offset = -1 * (weekday - 4)
            elif policy == WeekendCheckPolicy.NEXT_BUSINESS_DAY:
                day_offset = 7 - weekday

        return date + dt.timedelta(days=day_offset)

    def _next_statement(self, date: dt.date):
        if date <= dt.date(date.year, date.month, self.statement_day):
            statement_date = dt.date(date.year, date.month, self.statement_day)
        else:
            statement_date = dt.date(date.year, date.month + 1, self.statement_day)

        statement_date = self._weekend_check(statement_date, self.statement_day_policy)
        return statement_date

    def _x_days_after(self, date: dt.date):
        # compute due date from statement date
        statement_date = self._next_statement(date)
        due_date = statement_date + dt.timedelta(days=self.due_date_reference)

        # checks
        validated_due_date = self._weekend_check(due_date, self.due_date_policy)

        return validated_due_date

    def _before_statement(self): ...

    def _on_statement(self): ...

    def _after_statement(self): ...


@dataclass
class CreditCardInstallment:
    credit_card: CreditCard
    tenure: int
    start_date: dt.date
    total_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))
    monthly_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))

    def __post_init__(self):
        self.total_amount = self.total_amount.quantize(Decimal("0.00"))
        self.monthly_amount = self.monthly_amount.quantize(Decimal("0.00"))
        self.payment_dates = None


if __name__ == "__main__":
    class A(Enum):
        a =1
        b = 1
    
    policy = A.a
    print(A.a == policy)
