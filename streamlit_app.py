import logging

import pandas as pd
import streamlit as st

from happybarra.models import CreditCard, CreditCardInstallment, Bank, Network
from happybarra.enums import InstallmentAmountType

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

cci_init = False
st.write("# 🐹 happybarra")
st.write("Do I have enough money for this?")
bank = st.selectbox("Bank", [bank for bank in Bank.registry])
network = st.selectbox("Network", [network for network in Network.registry])
credit_card = st.selectbox(
    "Credit Card",
    [
        cc_name
        for cc_name, cc_object in CreditCard.registry.items()
        if cc_object.bank.name == bank and cc_object.network.name == network
    ],
)

st.write(
    f"You have selected the following card: **{bank} - {network} - {credit_card}**",
)
installment_type = st.radio(
    "What installment amount do you know?", InstallmentAmountType
)
installment_amount = st.number_input(
    f"{installment_type} Amount", step=500.0, format="%.2f"
)

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
    _logger.debug("cci failed error: ", e)
    st.write(":)")

if cci_init:
    charges = cci.get_charge_dates()
    _logger.debug(charges)
    df = pd.DataFrame(charges)
    _logger.debug(df)
    st.write(df)
