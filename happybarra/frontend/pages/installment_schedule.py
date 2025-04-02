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

PAGE_KEY = "credit_card_installment"
PK_KEY_DATE_SELECTION = f"{PAGE_KEY}__key_date_selection"
PK_DEFINE_INSTALLMENT = f"{PAGE_KEY}__define_installment"
PK_INSTALLMENT_SCHEDULE = f"{PAGE_KEY}__installment_schedule"
PK_CREDIT_CARD_SELECTION = f"{PAGE_KEY}__credit_card_selection"
PK_BANK_AND_NETWORK_SELECTION = f"{PAGE_KEY}__bank_and_network_selection"


VK_BANK = f"{PAGE_KEY}__bank"
VK_NETWORK = f"{PAGE_KEY}__network"
VK_DUE_DATE_REF = f"{PAGE_KEY}__due_date_ref"
VK_STATEMENT_DATE = f"{PAGE_KEY}__statement_date"
VK_CREDIT_CARD_KEY = f"{PAGE_KEY}__credit_card_key"
VK_INSTALLMENT_TYPE = f"{PAGE_KEY}__installment_type"
VK_CREDIT_CARD_OBJECT = f"{PAGE_KEY}__credit_card_object"
VK_INSTALLMENT_TENURE = f"{PAGE_KEY}__installment_tenure"
VK_INSTALLMENT_AMOUNT = f"{PAGE_KEY}__installment_amount"
VK_CREDIT_CARD_INSTANCE = f"{PAGE_KEY}__credit_card_instance"
VK_INSTALLMENT_INSTANCE = f"{PAGE_KEY}__installment_instance"
VK_INSTALLMENT_DATE_START = f"{PAGE_KEY}__installment_date_start"
VK_INVALID_COMBINATION_CHOSEN = f"{PAGE_KEY}__invalid_combination_chosen"


_logger = logging.getLogger(f"happybarra.{PAGE_KEY}")

st.markdown("# 🗓️ Installment Schedule")
st.markdown("Get a list of your installment due dates 😉.")

# Initialize the app
if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION

# Display the error markdown if there's an invalid combination chosen
if st.session_state.get(VK_INVALID_COMBINATION_CHOSEN, False):
    st.error("Invalid combination chosen. Choose again.")

    # Let's now reset the state so by next st.rerun(), we don't show the error banner
    # again.
    st.session_state[VK_INVALID_COMBINATION_CHOSEN] = False

# Bank and network subpage
if st.session_state[PAGE_KEY] == PK_BANK_AND_NETWORK_SELECTION:
    _logger.debug("Asking for bank and network")
    bank = st.selectbox("Bank", [bank for bank in Bank.registry])
    network = st.selectbox("Network", [network for network in Network.registry])
    bank_and_network_submitted = st.button("Submit")

    if bank_and_network_submitted:
        st.session_state[VK_BANK] = bank
        st.session_state[VK_NETWORK] = network
        st.session_state[PAGE_KEY] = "credit_card_selection"
        st.rerun()

# Credit card selection sub page
if st.session_state[PAGE_KEY] == PK_CREDIT_CARD_SELECTION:
    # credit card pre-selection validation
    bank = st.session_state[VK_BANK]
    network = st.session_state[VK_NETWORK]
    available_cards = [
        cc_name
        for cc_name, cc_object in CreditCard.registry.items()
        if cc_object.bank.name == bank and cc_object.network.name == network
    ]
    if len(available_cards) == 0:
        _logger.debug(
            "No credit card for bank and network combination: %s->%s", bank, network
        )
        st.session_state[VK_INVALID_COMBINATION_CHOSEN] = True
        st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION
        st.rerun()

    # if validation passed, then we ask for credit card
    _logger.debug("Asking for credit card")
    credit_card = st.selectbox("Credit Card", available_cards)
    credit_card_submitted = st.button("Submit")
    if credit_card_submitted:
        st.session_state[VK_CREDIT_CARD_KEY] = credit_card
        st.session_state[VK_CREDIT_CARD_OBJECT] = CreditCard.registry[credit_card]
        st.session_state[PAGE_KEY] = PK_KEY_DATE_SELECTION
        st.rerun()

if st.session_state[PAGE_KEY] == PK_KEY_DATE_SELECTION:
    _logger.debug("Key date selection")
    statement_date = st.select_slider("Select your statement date", range(1, 32))
    due_date_ref = st.select_slider(
        "How many days after your statement does your due date fall?", range(1, 46)
    )
    dates_submitted = st.button("Submit")
    if dates_submitted:
        st.session_state[VK_STATEMENT_DATE] = statement_date
        st.session_state[VK_DUE_DATE_REF] = due_date_ref
        st.session_state[VK_CREDIT_CARD_INSTANCE] = CreditCardInstance(
            credit_card=st.session_state[VK_CREDIT_CARD_OBJECT],
            due_date_ref=due_date_ref,
            statement_day=statement_date,
        )
        st.session_state[PAGE_KEY] = PK_DEFINE_INSTALLMENT
        st.rerun()

if st.session_state[PAGE_KEY] == PK_DEFINE_INSTALLMENT:
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
        st.session_state[VK_INSTALLMENT_TYPE] = installment_type
        st.session_state[VK_INSTALLMENT_AMOUNT] = installment_amount
        st.session_state[VK_INSTALLMENT_TENURE] = installment_tenure
        st.session_state[VK_INSTALLMENT_DATE_START] = date_input
        st.session_state[VK_INSTALLMENT_INSTANCE] = CreditCardInstallment(
            st.session_state[VK_CREDIT_CARD_INSTANCE],
            tenure=installment_tenure,
            amount_type=installment_type_choices[installment_type],
            amount=installment_amount,
            start_date=date_input,
        )
        st.session_state[PAGE_KEY] = PK_INSTALLMENT_SCHEDULE
        st.rerun()

if st.session_state[PAGE_KEY] == PK_INSTALLMENT_SCHEDULE:
    _logger.debug("Showing installment plan.")
    installment: CreditCardInstallment = st.session_state[VK_INSTALLMENT_INSTANCE]
    df = pd.DataFrame(installment.get_charge_dates())
    st.write(df)
    done = st.button("Done")
    if done:
        # cleanup
        for key in st.session_state:
            if PAGE_KEY in key:
                del st.session_state[key]
        st.rerun()
