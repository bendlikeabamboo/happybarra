import streamlit as st
import logging


logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


BANKS = ("Unionbank", "Metrobank", "BPI", "Eastwest", "Security Bank")
NETWORKS = ("VISA", "Mastercard", "American Express", "Discover", "Paypal")
CARD_TYPES = {
    ("Unionbank", "VISA"): ["PlayEveryday", "Rewards Platinum"],
    ("Metrobank", "VISA"): ["Titanium"],
    ("Metrobank", "Mastercard"): ["Peso Platinum"],
    ("BPI", "VISA"): [
        "Amore Cashback",
    ],
    ("BPI", "Mastercard"): [
        "Rewards Card",
        "Gold",
    ],
    ("Eastwest", "VISA"): ["Platinum"],
    ("Security Bank", "Mastercard"): ["Travel Platinum"],
}
INSTALLMENT_TYPES = ("Monthly", "Annual")


st.write("# 🐹 happybarra")
st.write("Do I have enough money for this?")
bank = st.selectbox("Bank", BANKS)
network = st.selectbox("Network", NETWORKS)
credit_card = st.selectbox(
    "Card Type", CARD_TYPES.get((bank, network), "No cards of this type.")
)

# Every form must have a submit button.
# _logger.debug("Form [bank_submitted]: %s", bank_submitted)

# if bank_submitted:
#     with st.form("card"):
#         st.write("Choose credit card")
#         card_type = st.selectbox("Card Type", CARD_TYPES[bank])
#         card_type_submitted = st.form_submit_button("Submit")

#         if card_type_submitted:
#             st.write("You have selected the following card:", card_type)


st.write(
    f"You have selected the following card: **{bank} - {network} - {credit_card}**",
)
installment_type = st.radio("What installment amount do you know?", INSTALLMENT_TYPES)
installment_amount = st.number_input(
    f"{installment_type} Amount", step=500.0, format="%.2f"
)

from happybarra.models import CreditCardInstallment

CreditCardInstallment()
