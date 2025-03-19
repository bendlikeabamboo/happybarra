from happybarra.banks import BPI, UNIONBANK, SECURITY_BANK, METROBANK, EASTWEST
from happybarra.models import CreditCard as CC
from happybarra.networks import MASTERCARD, VISA, JCB

# BPI Credit Cards
# https://www.bpi.com.ph/personal/cards/credit-cards
CC(bank=BPI, network=VISA, name="BPI Signature Card")
CC(bank=BPI, network=VISA, name="BPI Amore Platinum Cashback Card")
CC(bank=BPI, network=VISA, name="BPI Amore Cashback Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Platinum Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Gold Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="Petron BPI Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Edge Card")
CC(bank=BPI, network=MASTERCARD, name="BPI DOS Card")
CC(bank=BPI, network=MASTERCARD, name="Robinsons Cashback Card")

# Unionbank Credit Cards
# https://www.unionbankph.com/cards/credit-card
CC(bank=UNIONBANK, network=VISA, name="UnionBank Miles+ Visa Signature Credit Card")
CC(bank=UNIONBANK, network=VISA, name="Cebu Pacific Platinum Credit Card")
CC(bank=UNIONBANK, network=VISA, name="Cebu Pacific Gold Credit Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Miles+ Platinum Visa Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Cash Back Visa Platinum Credit Card")
CC(bank=UNIONBANK, network=VISA, name="U Visa Platinum")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Rewards Visa Platinum Credit Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Mercury Visa")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Visa Platinum")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Reserve Visa Infinite")
CC(bank=UNIONBANK, network=VISA, name="UnionBank S&R Visa Platinum")
CC(bank=UNIONBANK, network=VISA, name="Go Rewards Gold Visa Credit Card")
CC(bank=UNIONBANK, network=VISA, name="Go Rewards Platinum Visa Credit Card")
CC(bank=UNIONBANK, network=VISA, name="PlayEveryday")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Gold Visa Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Platinum Visa Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Classic Visa Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Shell Power Visa Platinum")
CC(bank=UNIONBANK, network=VISA, name="Assumption Alumni Association Visa Card")
CC(bank=UNIONBANK, network=VISA, name="La Salle Greenhills Visa Card")
CC(bank=UNIONBANK, network=VISA, name="De La Salle Alumni Visa Card")
CC(bank=UNIONBANK, network=VISA, name="Don Bosco Alumni Association Visa Card")
CC(bank=UNIONBANK, network=VISA, name="Ateneo Alumni Association Visa Card")
CC(
    bank=UNIONBANK,
    network=VISA,
    name="University of the Philippines Alumni Association Visa Card",
)
CC(bank=UNIONBANK, network=VISA, name="Southwestern University Alumni Foundation Visa Card")
CC(bank=UNIONBANK, network=VISA, name="UnionBank Corporate Visa Card")
CC(bank=UNIONBANK, network=VISA, name="Suy Sing Visa Card")
CC(
    bank=UNIONBANK,
    network=VISA,
    name="Couples for Christ Foundation for Family and Life Visa Card",
)
CC(bank=UNIONBANK, network=VISA, name="World Wide Fund Visa Card")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Miles+ World Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Cash Back Titanium Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="U Platinum Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Gold Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Platinum Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Rewards Platinum Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Platinum Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Reserve World Elite Mastercard")
CC(bank=UNIONBANK, network=MASTERCARD, name="UnionBank Lazada Credit Card")

# Security Bank
# https://www.securitybank.com/personal/credit-cards/rewards/
CC(bank=SECURITY_BANK, network=MASTERCARD, name="Gold Mastercard")
CC(bank=SECURITY_BANK, network=MASTERCARD, name="Platinum Mastercard")
CC(bank=SECURITY_BANK, network=MASTERCARD, name="World Mastercard")
CC(bank=SECURITY_BANK, network=MASTERCARD, name="Wave Mastercard")
CC(bank=SECURITY_BANK, network=MASTERCARD, name="Cashback Platinum")

# Metrobank
# https://www.metrobank.com.ph/cards/credit-cards/comparison-page
CC(bank=METROBANK, network=VISA, name="Metrobank Cashback Card")
CC(bank=METROBANK, network=VISA, name="Metrobank Rewards Plus Card")
CC(bank=METROBANK, network=VISA, name="Metrobank Travel Signature Visa")
CC(bank=METROBANK, network=VISA, name="")
CC(bank=METROBANK, network=VISA, name="")
CC(bank=METROBANK, network=VISA, name="")
CC(bank=METROBANK, network=VISA, name="")
CC(bank=METROBANK, network=MASTERCARD, name="Toyota Card")
CC(bank=METROBANK, network=MASTERCARD, name="Metrobank Titanium Mastercard")
CC(bank=METROBANK, network=MASTERCARD, name="Metrobank World Mastercard")
CC(bank=METROBANK, network=MASTERCARD, name="Metrobank Platinum Mastercard")
CC(bank=METROBANK, network=MASTERCARD, name="Metrobank World Mastercard")
CC(bank=METROBANK, network=MASTERCARD, name="Metrobank M Free Card")
CC(bank=METROBANK, network=MASTERCARD, name="PSBank Credit Mastercard")


# Eastwest
# https://www.eastwestbanker.com/cards/creditcards
CC(bank=EASTWEST, network=VISA, name="EastWest Priority Visa Infinite")
CC(bank=EASTWEST, network=VISA, name="Visa Platinum")
CC(bank=EASTWEST, network=VISA, name="EastWest Gold Visa")
CC(bank=EASTWEST, network=VISA, name="EastWest Privilege Visa")
CC(bank=EASTWEST, network=MASTERCARD, name="EastWest Platinum Mastercard")
CC(bank=EASTWEST, network=MASTERCARD, name="EastWest EveryDay Titanium Mastercard")
CC(bank=EASTWEST, network=MASTERCARD, name="EastWest Dolce Vita Titanium Mastercard")
CC(bank=EASTWEST, network=MASTERCARD, name="EastWest Gold Mastercard")
CC(
    bank=EASTWEST,
    network=MASTERCARD,
    name="EastWest Singapore Airlines KrisFlyer Platinum Mastercard",
)
CC(bank=EASTWEST, network=MASTERCARD, name="EastWest Privilege Mastercard")
CC(bank=EASTWEST, network=JCB, name="EastWest JCB Platinum")
CC(
    bank=EASTWEST,
    network=JCB,
    name="EastWest Singapore Airlines KrisFlyer World Mastercard",
)
CC(bank=EASTWEST, network=JCB, name="EastWest JCB Gold")


# CC(bank=EASTWEST, network=VISA, name="")
# CC(bank=EASTWEST, network=MASTERCARD, name="")
# CC(bank=EASTWEST, network=JCB, name="")

# TODO: RCBC
# TODO: HSBC
# TODO: AUB
# TODO: Landbank LOL
# TODO: PNB


if __name__ == "__main__":
    print(CC.registry)
