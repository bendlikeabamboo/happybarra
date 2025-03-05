from functools import partial
import datetime as dt
from happybarra.models import (
    CreditCard,
    DueDateType,
    CreditCardInstallment,
    InstallmentPolicy,
    InstallmentAmountType,
)
from happybarra.banks import BPI
from happybarra.network import VISA

BPI__MASTERCARD__REWARDS = partial(CreditCard, BPI, "Rewards", VISA)

if __name__ == "__main__":
    cc = BPI__MASTERCARD__REWARDS(20, 15)
    cci = CreditCardInstallment(
        cc,
        6,
        dt.date(2025, 3, 5),
        InstallmentPolicy.ON_PURCHASE_DAY,
        500.00,
        InstallmentAmountType.MONTHLY_FIXED,
    )
    print(cci.get_charge_dates())
