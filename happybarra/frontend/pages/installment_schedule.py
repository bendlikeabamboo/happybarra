import logging

import pandas as pd
import streamlit as st

from happybarra.frontend.models.enums import InstallmentAmountType
from happybarra.frontend.models.models import (
    Bank,
    CreditCard,
    CreditCardInstallment,
    CreditCardInstance,
    Network,
)

PAGE_NAME = "credit_card_installment"
_logger = logging.getLogger(f"happybarra.{PAGE_NAME}")

st.markdown("# 🗓️ Installment Schedule")
st.markdown("Get a list of your installment due dates 😉.")

# Initialize the app
if f"{PAGE_NAME}__page_key" not in st.session_state:
    st.session_state[f"{PAGE_NAME}__page_key"] = "bank_and_network_selection"

# Display the error markdown if there's an invalid combination chosen
if st.session_state.get(f"{PAGE_NAME}__invalid_combination_chosen", False):
    st.error("Invalid combination chosen. Choose again.")

    # Let's now reset the state so by next st.rerun(), we don't show the error banner
    # again.
    st.session_state[f"{PAGE_NAME}__invalid_combination_chosen"] = False

# Bank and network subpage
if st.session_state[f"{PAGE_NAME}__page_key"] == "bank_and_network_selection":
    _logger.debug("Asking for bank and network")
    bank = st.selectbox("Bank", [bank for bank in Bank.registry])
    network = st.selectbox("Network", [network for network in Network.registry])
    bank_and_network_submitted = st.button("Submit")

    if bank_and_network_submitted:
        st.session_state[f"{PAGE_NAME}__bank"] = bank
        st.session_state[f"{PAGE_NAME}__network"] = network
        st.session_state[f"{PAGE_NAME}__page_key"] = "credit_card_selection"
        st.rerun()

# Credit card selection sub page
if st.session_state[f"{PAGE_NAME}__page_key"] == "credit_card_selection":
    # credit card pre-selection validation
    bank = st.session_state[f"{PAGE_NAME}__bank"]
    network = st.session_state[f"{PAGE_NAME}__network"]
    available_cards = [
        cc_name
        for cc_name, cc_object in CreditCard.registry.items()
        if cc_object.bank.name == bank and cc_object.network.name == network
    ]
    if len(available_cards) == 0:
        _logger.debug(
            "No credit card for bank and network combination: %s->%s", bank, network
        )
        st.session_state[f"{PAGE_NAME}__invalid_combination_chosen"] = True
        st.session_state[f"{PAGE_NAME}__page_key"] = "bank_and_network_selection"
        st.rerun()

    # if validation passed, then we ask for credit card
    _logger.debug("Asking for credit card")
    credit_card = st.selectbox("Credit Card", available_cards)
    credit_card_submitted = st.button("Submit")
    if credit_card_submitted:
        st.session_state[f"{PAGE_NAME}__credit_card_key"] = credit_card
        st.session_state[f"{PAGE_NAME}__credit_card_object"] = CreditCard.registry[
            credit_card
        ]
        st.session_state[f"{PAGE_NAME}__page_key"] = "key_date_selection"
        st.rerun()

if st.session_state[f"{PAGE_NAME}__page_key"] == "key_date_selection":
    _logger.debug("Key date selection")
    statement_date = st.select_slider("Select your statement date", range(1, 32))
    due_date_ref = st.select_slider(
        "How many days after your statement does your due date fall?", range(1, 46)
    )
    dates_submitted = st.button("Submit")
    if dates_submitted:
        st.session_state[f"{PAGE_NAME}__statement_date"] = statement_date
        st.session_state[f"{PAGE_NAME}__due_date_ref"] = due_date_ref
        st.session_state[f"{PAGE_NAME}__page_key"] = "define_installment"
        st.session_state[f"{PAGE_NAME}__credit_card_instance"] = CreditCardInstance(
            credit_card=st.session_state[f"{PAGE_NAME}__credit_card_object"],
            due_date_ref=due_date_ref,
            statement_day=statement_date,
        )
        st.rerun()

if st.session_state[f"{PAGE_NAME}__page_key"] == "define_installment":
    _logger.debug("asking for installment")

    installment_type_choices = {
        "Fixed Monthly": InstallmentAmountType.MONTHLY_FIXED,
        "Fixed Total": InstallmentAmountType.TOTAL_FIXED,
    }
    installment_type = st.radio(
        "What installment amount do you know?", installment_type_choices
    )

    # TODO: Check if thousand separator is now supported by sprintf.js 🥲
    installment_amount = st.number_input(
        f"{installment_type} Amount", step=500.00, format="%.2f"
    )
    installment_tenure = st.number_input(
        "How many months do you have to pay for it?", step=1
    )
    date_input = st.date_input("When is the purchase?", format="YYYY-MM-DD")
    installment_purchase_submitted = st.button("Submit")

    if installment_purchase_submitted:
        st.session_state[f"{PAGE_NAME}__installment_type"] = installment_type
        st.session_state[f"{PAGE_NAME}__installment_amount"] = installment_amount
        st.session_state[f"{PAGE_NAME}__installment_tenure"] = installment_tenure
        st.session_state[f"{PAGE_NAME}__date_input"] = date_input
        st.session_state[f"{PAGE_NAME}__installment_instance"] = CreditCardInstallment(
            st.session_state[f"{PAGE_NAME}__credit_card_instance"],
            tenure=installment_tenure,
            amount_type=installment_type_choices[installment_type],
            amount=installment_amount,
            start_date=date_input,
        )
        st.session_state[f"{PAGE_NAME}__page_key"] = "installment_list"
        st.rerun()

if st.session_state[f"{PAGE_NAME}__page_key"] == "installment_list":
    _logger.debug("Showing installment plan.")
    installment: CreditCardInstallment = st.session_state[
        f"{PAGE_NAME}__installment_instance"
    ]
    df = pd.DataFrame(installment.get_charge_dates())
    st.write(df)
    done = st.button("Done")
    if done:
        # cleanup
        for key in st.session_state:
            if f"{PAGE_NAME}__" in key:
                del st.session_state[key]
        st.rerun()
