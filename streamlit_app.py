import streamlit as st
import logging
import pandas as pd
from functools import partial

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

from happybarra.models import CreditCard


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
        "Rewards",
        "Gold",
    ],
    ("Eastwest", "VISA"): ["Platinum"],
    ("Security Bank", "Mastercard"): ["Travel Platinum"],
}
INSTALLMENT_TYPES = ("Monthly", "Annual")

cci_init = False
st.write("# 🐹 happybarra")
st.write("Do I have enough money for this?")
bank = st.selectbox("Bank", BANKS)
network = st.selectbox("Network", NETWORKS)
credit_card = st.selectbox(
    "Card Type", CARD_TYPES.get((bank, network), "No cards of this type.")
)


from happybarra.credit_cards import BPI__MASTERCARD__REWARDS


def get_credit_card(cc_key: tuple) -> partial[CreditCard]:
    _logger.debug("getting credit card")
    ccs = {("BPI", "Mastercard", "Rewards"): BPI__MASTERCARD__REWARDS}
    return ccs.get(cc_key, "error")


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

statement_date = st.select_slider("Select your statement date", range(1, 32))
due_date_ref = st.select_slider(
    "How many days after your statement does your due date fall?", range(1, 46)
)
installment_tenure = st.number_input(
    f"How many months do you have to pay for it?", step=1
)

date_input = st.date_input("When is the purchase?", format="YYYY-MM-DD")


try:
    cci = CreditCardInstallment(
        get_credit_card((bank, network, credit_card))(
            due_date_ref=due_date_ref, statement_day=statement_date
        ),
        installment_tenure,
        date_input,
        amount=installment_amount,
    )
    _logger.debug(cci)
    cci_init = True
except Exception as e:
    _logger.debug("cci failed error: ",e )
    st.write(":)")

if cci_init:
    charges = cci.get_charge_dates()
    _logger.debug(charges)
    df = pd.DataFrame(charges)
    _logger.debug(df)
    st.write(df)
