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
from happybarra.networks import *

BPI__MASTERCARD__REWARDS = CreditCard(BPI, "BPI Rewards", MASTERCARD)
BPI__MASTERCARD__GOLD = CreditCard(BPI, "BPI Gold", MASTERCARD)


UNIONBANK__VISA__REWARDS_PLATINUM = CreditCard(
    UNIONBANK, "Unionbank Rewards Visa Platinum", VISA
)
UNIONBANK__VISA__U_VISA_PLATINUM = CreditCard(
    UNIONBANK, "Unionbank U Visa Platinum", VISA
)
UNIONBANK__VISA__PLAYEVERYDAY = CreditCard(UNIONBANK, "Unionbank PlayEveryday", VISA)


SECURITY_BANK__MASTERCARD__TRAVEL_PLATINUM = CreditCard(
    SECURITY_BANK, "Security Bank Travel Platinum Mastercard", MASTERCARD
)


METROBANK__MASTERCARD__PESO_PLATINUM = CreditCard(
    METROBANK, "Metrobank Platinum Mastercard", MASTERCARD
)

EASTWEST__VISA__PLATINUM = CreditCard(EASTWEST, "Eastwest Visa Platinum", VISA)


if __name__ == "__main__":
    print(CreditCard.registry)
