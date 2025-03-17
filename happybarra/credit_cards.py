from happybarra.banks import BPI, UNIONBANK, SECURITY_BANK, METROBANK, EASTWEST
from happybarra.models import CreditCard
from happybarra.networks import MASTERCARD, VISA

BPI__MASTERCARD__REWARDS = CreditCard(bank=BPI, name="BPI Rewards", network=MASTERCARD)
BPI__MASTERCARD__GOLD = CreditCard(bank=BPI, name="BPI Gold", network=MASTERCARD)


UNIONBANK__VISA__REWARDS_PLATINUM = CreditCard(
    bank=UNIONBANK, name="Unionbank Rewards Visa Platinum", network=VISA
)
UNIONBANK__VISA__U_VISA_PLATINUM = CreditCard(
    bank=UNIONBANK, name="Unionbank U Visa Platinum", network=VISA
)
UNIONBANK__VISA__PLAYEVERYDAY = CreditCard(
    bank=UNIONBANK, name="Unionbank PlayEveryday", network=VISA
)


SECURITY_BANK__MASTERCARD__TRAVEL_PLATINUM = CreditCard(
    bank=SECURITY_BANK,
    name="Security Bank Travel Platinum Mastercard",
    network=MASTERCARD,
)


METROBANK__MASTERCARD__PESO_PLATINUM = CreditCard(
    bank=METROBANK, name="Metrobank Platinum Mastercard", network=MASTERCARD
)

EASTWEST__VISA__PLATINUM = CreditCard(
    bank=EASTWEST, name="Eastwest Visa Platinum", network=VISA
)


if __name__ == "__main__":
    print(CreditCard.registry)
