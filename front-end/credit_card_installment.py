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
from happybarra import banks  # noqa: F401
from happybarra import networks  # noqa: F401
from happybarra import credit_cards  # noqa: F401

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

st.markdown("# 🗓️ Credit Card Installment")
st.markdown("Get a list of your installment due dates 😉.")

# initialize the app
if "cci__page_key" not in st.session_state:
    st.session_state["cci__page_key"] = "bank_and_network_selection"
try:
    if st.session_state["cci__page_key"] == "bank_and_network_selection":
        _logger.debug("asking for bankF and network")
        bank = st.selectbox("Bank", [bank for bank in Bank.registry])
        network = st.selectbox("Network", [network for network in Network.registry])
        bank_and_network_submitted = st.button("Submit")
        if bank_and_network_submitted:
            st.session_state["cci__bank"] = bank
            st.session_state["cci__network"] = network
            st.session_state["cci__page_key"] = "credit_card_selection"
            st.rerun()

    if st.session_state["cci__page_key"] == "credit_card_selection":
        _logger.debug("asking for credit card")
        bank = st.session_state["cci__bank"]
        network = st.session_state["cci__network"]

        available_cards = [
            cc_name
            for cc_name, cc_object in CreditCard.registry.items()
            if cc_object.bank.name == bank and cc_object.network.name == network
        ]
        if len(available_cards) > 0:
            credit_card = st.selectbox("Credit Card", available_cards)
        else:
            st.session_state["cci__page_key"] = "no_available_options"
            st.rerun()
        credit_card_submitted = st.button("Submit")
        if credit_card_submitted:
            st.session_state["cci__credit_card_key"] = credit_card
            st.session_state["cci__credit_card_object"] = CreditCard.registry[
                credit_card
            ]
            st.session_state["cci__page_key"] = "key_date_selection"
            st.rerun()

    if st.session_state["cci__page_key"] == "key_date_selection":
        _logger.debug("key_date_selection")
        statement_date = st.select_slider("Select your statement date", range(1, 32))
        due_date_ref = st.select_slider(
            "How many days after your statement does your due date fall?", range(1, 46)
        )
        dates_submitted = st.button("Submit")
        if dates_submitted:
            st.session_state["cci__statement_date"] = statement_date
            st.session_state["cci__due_date_ref"] = due_date_ref
            st.session_state["cci__page_key"] = "define_installment"
            st.session_state["cci__credit_card_instance"] = CreditCardInstance(
                credit_card=st.session_state["cci__credit_card_object"],
                due_date_ref=due_date_ref,
                statement_day=statement_date,
            )
            st.rerun()

    if st.session_state["cci__page_key"] == "define_installment":
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
            st.session_state["cci__installment_type"] = installment_type
            st.session_state["cci__installment_amount"] = installment_amount
            st.session_state["cci__installment_tenure"] = installment_tenure
            st.session_state["cci__date_input"] = date_input
            st.session_state["cci__installment_instance"] = CreditCardInstallment(
                st.session_state["cci__credit_card_instance"],
                tenure=installment_tenure,
                amount_type=installment_type_choices[installment_type],
                amount=installment_amount,
                start_date=date_input,
            )
            st.session_state["cci__page_key"] = "installment_list"
            st.rerun()

    if st.session_state["cci__page_key"] == "installment_list":
        _logger.debug("Showing installment plan.")
        installment: CreditCardInstallment = st.session_state[
            "cci__installment_instance"
        ]
        df = pd.DataFrame(installment.get_charge_dates())
        st.write(df)
        done = st.button("Done!")
        if done:
            # cleanup
            for key in st.session_state:
                if "cci__" in key:
                    del st.session_state[key]
            st.rerun()

    if st.session_state["cci__page_key"] == "no_available_options":
        st.write("We found no available options for your input. Please restart.")
        go_back = st.button("Go back")
        if go_back:
            for key in st.session_state:
                if "cci__" in key:
                    del st.session_state[key]
            st.rerun()

except Exception as gen_ex:
    go_back = st.button("Go back")
    _logger.error(gen_ex, exc_info=True)
    if go_back:
        for key in st.session_state:
            if "cci__" in key:
                del st.session_state[key]
        st.rerun()
