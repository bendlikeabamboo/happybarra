import logging
import os
import time

import requests
import streamlit as st
from dotenv import load_dotenv

from happybarra.frontend.data import (
    banks,  # noqa: F401
    credit_cards,  # noqa: F401
    networks,  # noqa: F401
)
from happybarra.frontend.models.models import Bank, CreditCard, Network

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

load_dotenv()
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")

st.markdown("# 💳 Create Credit Card Instance")
st.markdown("Let's track your cards!")

PAGE_STATE = "cci_page_state"

try:
    if PAGE_STATE not in st.session_state:
        st.session_state[PAGE_STATE] = "bank_and_network"

    if st.session_state[PAGE_STATE] == "bank_and_network":
        bank = st.selectbox("Select bank", Bank.registry)
        network = st.selectbox("Select network", Network.registry)
        submit = st.button("Submit")
        if submit:
            st.session_state[f"{PAGE_STATE}__bank"] = bank
            st.session_state[f"{PAGE_STATE}__network"] = network
            st.session_state[PAGE_STATE] = "credit_card"
            st.rerun()

    if st.session_state[PAGE_STATE] == "credit_card":
        # from the provided bank and network, retrieve all credit cards
        matching_ccs = {
            key
            for key, value in CreditCard.registry.items()
            if value.bank.name == st.session_state[f"{PAGE_STATE}__bank"]
            and value.network.name == st.session_state[f"{PAGE_STATE}__network"]
        }

        # use the retrieved ccs here:
        credit_card = st.selectbox("Select Credit Card", matching_ccs)

        submit = st.button("Submit")
        if submit:
            st.session_state[f"{PAGE_STATE}__credit_card"] = credit_card
            st.session_state[PAGE_STATE] = "date_references"
            st.rerun()

    if st.session_state[PAGE_STATE] == "date_references":
        statement_date = st.select_slider("Select statement date", range(1, 32))
        due_days_after_statement = st.select_slider(
            "How many days after your statement is your due date?", range(1, 45)
        )
        submit = st.button("Submit")
        if submit:
            st.session_state[f"{PAGE_STATE}__statement_date"] = statement_date
            st.session_state[f"{PAGE_STATE}__due_days_after_statement"] = (
                due_days_after_statement
            )
            st.session_state[PAGE_STATE] = "credit_card_nickname"
            st.rerun()

    if st.session_state[PAGE_STATE] == "credit_card_nickname":
        nickname = st.text_input("Give your credit card a nick name:", max_chars=15)
        submit = st.button("Create Credit Card")
        if submit:
            st.session_state[f"{PAGE_STATE}__nickname"] = nickname
            st.session_state[PAGE_STATE] = "credit_card_instance_submitted"
            st.rerun()

    if st.session_state[PAGE_STATE] == "credit_card_instance_submitted":
        # call back-end api
        body = {
            "name": st.session_state[f"{PAGE_STATE}__nickname"],
            "bank": st.session_state[f"{PAGE_STATE}__bank"],
            "network": st.session_state[f"{PAGE_STATE}__network"],
            "credit_card": st.session_state[f"{PAGE_STATE}__credit_card"],
            "statement_day": st.session_state[f"{PAGE_STATE}__statement_date"],
            "due_date_reference": st.session_state[
                f"{PAGE_STATE}__due_days_after_statement"
            ],
        }

        api_url = f"{BACKEND_URL}/api/v1/create_credit_card"
        _logger.info("Submitting credit card info to %s", api_url)
        _logger.debug("%s", body)
        response = requests.post(api_url, json=body)
        if response.ok:
            _logger.info("Credit Card info submitted.")
            st.write(f"Say welcome to {st.session_state[f'{PAGE_STATE}__nickname']}!")
        else:
            _logger.info("Something went wrong.")
        restart = st.button("Home")
        if restart:
            st.session_state[PAGE_STATE] = f"{PAGE_STATE}__page_tear_down"
            st.rerun()

except Exception as general_exception:
    st.session_state[PAGE_STATE] = f"{PAGE_STATE}__page_tear_down"
    st.write("Something went wrong... Reloading")
    st.error(f"{general_exception}")
    time.sleep(3)
    st.rerun()


if st.session_state[PAGE_STATE] == f"{PAGE_STATE}__page_tear_down":
    for key in st.session_state:
        if PAGE_STATE in key:
            del st.session_state[key]

st.write(st.session_state)
