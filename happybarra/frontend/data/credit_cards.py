from happybarra.frontend.data.networks import (
    AMERICAN_EXPRESS,
    DINERS_CLUB_INTERNATIONAL,
    JCB,
    MASTERCARD,
    UNIONPAY,
    VISA,
)
from happybarra.frontend.models.models import CreditCard as CC

from .banks import (
    AUB,
    BDO,
    BPI,
    CHINABANK,
    EASTWEST,
    HSBC,
    LANDBANK,
    METROBANK,
    PNB,
    RCBC,
    SECURITY_BANK,
    UNIONBANK,
)

# BPI Credit Cards
# https://www.bpi.com.ph/personal/cards/credit-cards
CC(bank=BPI, network=MASTERCARD, name="BPI DOS Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Edge Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Gold Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Platinum Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="BPI Rewards Card")
CC(bank=BPI, network=MASTERCARD, name="Petron BPI Card")
CC(bank=BPI, network=MASTERCARD, name="Robinsons Cashback Card")
CC(bank=BPI, network=VISA, name="BPI Amore Cashback Card")
CC(bank=BPI, network=VISA, name="BPI Amore Platinum Cashback Card")
CC(bank=BPI, network=VISA, name="BPI Signature Card")

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
CC(
    bank=UNIONBANK,
    network=VISA,
    name="Southwestern University Alumni Foundation Visa Card",
)
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

# RCBC
# https://rcbccredit.com/credit-cards
CC(bank=RCBC, network=VISA, name="RCBC Visa Infinite Card")
CC(bank=RCBC, network=VISA, name="RCBC Visa Infinite Card")
CC(bank=RCBC, network=VISA, name="RCBC Visa Platinum")
CC(bank=RCBC, network=VISA, name="RCBC Flex Gold Visa")
CC(bank=RCBC, network=VISA, name="RCBC Flex Visa")
CC(bank=RCBC, network=VISA, name="RCBC AirAsia Credit Card")
CC(bank=RCBC, network=MASTERCARD, name="RCBC World Mastercard")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Black Card Platinum Mastercard")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Diamond Platinum Mastercard")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Hexagon Priority")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Hexagon Club")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Gold Mastercard")
CC(bank=RCBC, network=MASTERCARD, name="RCBC YGC Rewards Plus Program")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Classic Mastercard")
CC(bank=RCBC, network=MASTERCARD, name="RCBC ZALORA Credit Card")
CC(bank=RCBC, network=MASTERCARD, name="RCBC Landmark Anson's Mastercard")
CC(bank=RCBC, network=JCB, name="RCBC JCB Platinum")
CC(bank=RCBC, network=JCB, name="RCBC Gold JCB")
CC(bank=RCBC, network=JCB, name="RCBC Classic JCB")
CC(bank=RCBC, network=UNIONPAY, name="RCBC UnionPay Diamond Card")

# HSBC
# https://www.hsbc.com.ph/credit-cards/products/
CC(bank=HSBC, network=VISA, name="HSBC Live+ Credit Card")
CC(bank=HSBC, network=VISA, name="HSBC Gold Visa Cash Back Credit Card")
CC(bank=HSBC, network=VISA, name="HSBC Platinum Visa Rebate Credit Card")
CC(bank=HSBC, network=MASTERCARD, name="HSBC Red Mastercard")
CC(bank=HSBC, network=MASTERCARD, name="HSBC Premier Mastercard")

# AUB
# https://online.aub.ph/creditcards
CC(bank=AUB, network=MASTERCARD, name="AUB Easy MasterCard")
CC(bank=AUB, network=MASTERCARD, name="AUB Classic MasterCard")
CC(bank=AUB, network=MASTERCARD, name="AUB Gold Mastercard")
CC(bank=AUB, network=MASTERCARD, name="AUB Platinum Mastercard")

# Landbank
# https://www.landbank.com/cards/landbank-credit-card
CC(bank=LANDBANK, network=MASTERCARD, name="Landbank Gold Mastercard")
CC(bank=LANDBANK, network=MASTERCARD, name="Landbank Classic Mastercard")

# PNB
# https://www.pnb.com.ph/index.php/credit-cards?tpl=revamp
CC(bank=PNB, network=VISA, name="PNB Visa Classic")
CC(bank=PNB, network=VISA, name="PNB Visa Gold")
CC(bank=PNB, network=MASTERCARD, name="PNB-PAL Mabuhay Miles World Elite Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB-PAL Mabuhay Miles World Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB-PAL Mabuhay Miles Platinum Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB-PAL Mabuhay Miles NOW Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB Essentials Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB Platinum Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB Ze-Lo Mastercard")
CC(bank=PNB, network=MASTERCARD, name="PNB Cart Mastercard")
CC(
    bank=PNB,
    network=MASTERCARD,
    name="PNB-La Salle Green Hills Alumni Association Platinum Mastercard",
)
CC(bank=PNB, network=UNIONPAY, name="PNB Diamond UnionPay")

# Chinabank
# https://www.chinabank.ph/credit-cards
CC(bank=CHINABANK, network=VISA, name="Chinabank Velvet Visa Signature")
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank Destinations World Mastercard")
CC(
    bank=CHINABANK,
    network=MASTERCARD,
    name="Chinabank Destinations World Dollar Mastercard",
)
CC(
    bank=CHINABANK,
    network=MASTERCARD,
    name="Chinabank Destinations Platinum Mastercard",
)
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank World Mastercard")
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank Cash Rewards Mastercard")
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank Platinum Mastercard")
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank Freedom Mastercard")
CC(bank=CHINABANK, network=MASTERCARD, name="Chinabank Prime Mastercard")

# BDO
# https://www.bdo.com.ph/personal/cards/credit-cards
CC(bank=BDO, network=MASTERCARD, name="BDO ShopMore Mastercard - Purple")
CC(bank=BDO, network=MASTERCARD, name="BDO ShopMore Mastercard - Yellow Green")
CC(bank=BDO, network=MASTERCARD, name="BDO ShopMore Mastercard - Orange")
CC(bank=BDO, network=MASTERCARD, name="BDO Standard Mastercard")
CC(bank=BDO, network=MASTERCARD, name="BDO Bench Mastercard")
CC(bank=BDO, network=MASTERCARD, name="BDO Installment Card")
CC(bank=BDO, network=MASTERCARD, name="BDO Gold Mastercard")
CC(bank=BDO, network=MASTERCARD, name="BDO Platinum Mastercard")
CC(bank=BDO, network=MASTERCARD, name="BDO World Elite Mastercard")
CC(bank=BDO, network=VISA, name="BDO Visa Classic")
CC(bank=BDO, network=VISA, name="BDO Visa Gold")
CC(bank=BDO, network=VISA, name="BDO Visa Platinum")
CC(bank=BDO, network=VISA, name="BDO Visa Signature")
CC(bank=BDO, network=UNIONPAY, name="BDO Gold UnionPay")
CC(bank=BDO, network=UNIONPAY, name="BDO Diamond UnionPay")
CC(bank=BDO, network=JCB, name="BDO JCB Lucky Cat")
CC(bank=BDO, network=JCB, name="BDO JCB Gold")
CC(bank=BDO, network=JCB, name="BDO JCB Platinum")
CC(bank=BDO, network=DINERS_CLUB_INTERNATIONAL, name="BDO Diners Club International")
CC(bank=BDO, network=DINERS_CLUB_INTERNATIONAL, name="BDO Diners Club Premiere")
CC(bank=BDO, network=AMERICAN_EXPRESS, name="Blue from American Express")
CC(bank=BDO, network=AMERICAN_EXPRESS, name="American Express Cashback Credit Card")
CC(bank=BDO, network=AMERICAN_EXPRESS, name="American Express Explorer Credit Card")
CC(bank=BDO, network=AMERICAN_EXPRESS, name="American Express Platinum Credit Card")
