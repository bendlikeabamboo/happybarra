import datetime as dt
from functools import partial

from happybarra.banks import *
from happybarra.models import (
    CreditCard,
    CreditCardInstallment,
    DueDateType,
    InstallmentAmountType,
    InstallmentPolicy,
)
from happybarra.network import *
from happybarra.registry import registry

BPI__MASTERCARD__REWARDS = partial(CreditCard, BPI, "Rewards", MASTERCARD)
BPI__MASTERCARD__GOLD = partial(CreditCard, BPI, "Gold", MASTERCARD)


UNIONBANK__VISA__REWARDS_PLATINUM = partial(
    CreditCard, UNIONBANK, "Rewards Platinum", VISA
)
UNIONBANK__VISA__U_VISA_PLATINUM = partial(
    CreditCard, UNIONBANK, "U VISA Platinum", VISA
)
UNIONBANK__VISA__PLAYEVERYDAY = partial(CreditCard, UNIONBANK, "PlayEveryday", VISA)


SECURITY_BANK__MASTERCARD__TRAVEL_PLATINUM = partial(
    CreditCard, SECURITY_BANK, "Travel Platinum", MASTERCARD
)


METROBANK__MASTERCARD__PESO_PLATINUM = partial(
    CreditCard, METROBANK, "Peso Platinum", MASTERCARD
)

EASTWEST__VISA__PLATINUM = partial(CreditCard, EASTWEST, "Platinum", VISA)


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
