import logging

import pandas as pd
import streamlit as st

from happybarra.models import (
    CreditCard,
    CreditCardInstallment,
    Bank,
    Network,
    CreditCardInstance,
)
from happybarra.enums import InstallmentAmountType
from happybarra.banks import *
from happybarra.networks import *
from happybarra.credit_cards import *

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

cci_init = False
st.write("# 🐹 happybarra")
st.write("Do I have enough money for this?")

# initialize the app
if "page_key" not in st.session_state:
    st.session_state["page_key"] = "bank_and_network_selection"

if st.session_state["page_key"] == "bank_and_network_selection":
    bank = st.selectbox("Bank", [bank for bank in Bank.registry])
    network = st.selectbox("Network", [network for network in Network.registry])
    bank_and_network_submitted = st.button("Submit")
    if bank_and_network_submitted:
        st.session_state["bank"] = bank
        st.session_state["network"] = network
        st.session_state["page_key"] = "credit_card_selection"
        st.rerun()

if st.session_state["page_key"] == "credit_card_selection":
    bank = st.session_state["bank"]
    network = st.session_state["network"]
    credit_card = st.selectbox(
        "Credit Card",
        [
            cc_name
            for cc_name, cc_object in CreditCard.registry.items()
            if cc_object.bank.name == bank and cc_object.network.name == network
        ],
    )
    credit_card_submitted = st.button("Submit")
    if credit_card_submitted:
        st.session_state["credit_card_key"] = credit_card
        st.session_state["credit_card_object"] = CreditCard.registry[credit_card]
        st.session_state["page_key"] = "key_date_selection"
        st.rerun()

if st.session_state["page_key"] == "key_date_selection":
    statement_date = st.select_slider("Select your statement date", range(1, 32))
    due_date_ref = st.select_slider(
        "How many days after your statement does your due date fall?", range(1, 46)
    )
    dates_submitted = st.button("Submit")
    if dates_submitted:
        st.session_state["statement_date"] = statement_date
        st.session_state["due_date_ref"] = due_date_ref
        st.session_state["page_key"] = "define_installment"
        st.session_state["credit_card_instance"] = CreditCardInstance(
            credit_card=st.session_state["credit_card_object"],
            due_date_ref=due_date_ref,
            statement_day=statement_date,
        )
        st.rerun()

if st.session_state["page_key"] == "define_installment":
    installment_type = st.radio(
        "What installment amount do you know?", InstallmentAmountType
    )
    installment_amount = st.number_input(
        f"{installment_type} Amount", step=500.0, format="%.2f"
    )
    installment_tenure = st.number_input(
        f"How many months do you have to pay for it?", step=1
    )
    date_input = st.date_input("When is the purchase?", format="YYYY-MM-DD")
    installment_purchase_submitted = st.button("Submit")
    if installment_purchase_submitted:
        st.session_state["installment_type"] = installment_type
        st.session_state["installment_amount"] = installment_amount
        st.session_state["installment_tenure"] = installment_tenure
        st.session_state["date_input"] = date_input
        st.session_state["installment_instance"] = CreditCardInstallment(
            st.session_state["credit_card_instance"],
            tenure=installment_tenure,
            amount_type=installment_type,
            amount=installment_amount,
            start_date=date_input,
        )
        st.session_state["page_key"] = "installment_list"
        st.rerun()

if st.session_state["page_key"] == "installment_list":
    installment: CreditCardInstallment = st.session_state["installment_instance"]
    df = pd.DataFrame(installment.get_charge_dates())
    st.write(df)

    done = st.button("Done!")
    if done:
        # cleanup
        del st.session_state["bank"]
        del st.session_state["network"]
        del st.session_state["credit_card_key"]
        del st.session_state["credit_card_object"]
        del st.session_state["statement_date"]
        del st.session_state["due_date_ref"]
        del st.session_state["credit_card_instance"]
        del st.session_state["installment_type"]
        del st.session_state["installment_amount"]
        del st.session_state["installment_tenure"]
        del st.session_state["date_input"]
        del st.session_state["installment_instance"]
        del st.session_state["page_key"]
        st.session_state.clear()
        st.rerun()


# st.write(
#     f"You have selected the following card: **{bank} - {network} - {credit_card}**",
# )
# installment_type = st.radio(
#     "What installment amount do you know?", InstallmentAmountType
# )
# installment_amount = st.number_input(
#     f"{installment_type} Amount", step=500.0, format="%.2f"
# )

# statement_date = st.select_slider("Select your statement date", range(1, 32))
# due_date_ref = st.select_slider(
#     "How many days after your statement does your due date fall?", range(1, 46)
# )
# installment_tenure = st.number_input(
#     f"How many months do you have to pay for it?", step=1
# )
# date_input = st.date_input("When is the purchase?", format="YYYY-MM-DD")


# try:
#     cci = CreditCardInstallment(
#         get_credit_card((bank, network, credit_card))(
#             due_date_ref=due_date_ref, statement_day=statement_date
#         ),
#         installment_tenure,
#         date_input,
#         amount=installment_amount,
#     )
#     _logger.debug(cci)
#     cci_init = True
# except Exception as e:
#     _logger.debug("cci failed error: ", e)
#     st.write(":)")

# if cci_init:
#     charges = cci.get_charge_dates()
#     _logger.debug(charges)
#     df = pd.DataFrame(charges)
#     _logger.debug(df)
#     st.write(df)
