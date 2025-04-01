import logging
import os
from types import SimpleNamespace

import requests
import streamlit as st
from dotenv import load_dotenv

from happybarra.frontend.models.models import Bank, CreditCard, Network
from happybarra.frontend.services import helpers

_logger = logging.getLogger("happybarra.add_credit_card")
PAGE_NAME = "add_credit_card"

load_dotenv()
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")

st.markdown("# 💳 Add Credit Card")
st.markdown("Let's track your cards!")


# Define the page start point
if PAGE_NAME not in st.session_state:
    st.session_state[PAGE_NAME] = "bank_and_network"

#
# ERROR HANDLING:
# If an invalid combination is chosen later in the script, show the error banner
if st.session_state.get(f"{PAGE_NAME}__invalid_combination_chosen", False):
    # show the banner
    st.error("Invalid combination chosen.")
    # reset the state so we don't show this again next page
    st.session_state[f"{PAGE_NAME}__invalid_combination_chosen"] = False

#
# ERROR HANDLING:
# If an API error is found later in the script, show the error banner
if st.session_state.get(f"{PAGE_NAME}__api_error_encountered", False):
    # show the banner
    st.error(
        "There was an error encountered while adding credit card. Try again later."
    )
    # reset the state so we don't show this again next page
    st.session_state[f"{PAGE_NAME}__api_error_encountered"] = False

# Bank and network selection
if st.session_state[PAGE_NAME] == "bank_and_network":
    _logger.debug("Selecting bank and network")
    bank = st.selectbox("Select bank", Bank.registry)
    network = st.selectbox("Select network", Network.registry)
    submit = st.button("Submit")
    if submit:
        st.session_state[f"{PAGE_NAME}__bank"] = bank
        st.session_state[f"{PAGE_NAME}__network"] = network
        st.session_state[PAGE_NAME] = "credit_card"
        st.rerun()

# credit card selection
if st.session_state[PAGE_NAME] == "credit_card":
    # create variables from previous page:
    bank: str = st.session_state[f"{PAGE_NAME}__bank"]
    network: str = st.session_state[f"{PAGE_NAME}__network"]

    # from the provided bank and network, retrieve all credit cards
    matching_ccs = {
        key
        for key, value in CreditCard.registry.items()
        if value.bank.name == bank and value.network.name == network
    }

    #
    # INPUT VALIDATION
    # credit card pre-selection validation:
    if len(matching_ccs) == 0:
        _logger.info(
            "Invalid combinations of bank and network: %s -> %s", bank, network
        )
        st.session_state[f"{PAGE_NAME}__invalid_combination_chosen"] = True
        st.session_state[PAGE_NAME] = "bank_and_network"
        st.rerun()

    # use the retrieved ccs here:
    credit_card = st.selectbox("Select Credit Card", matching_ccs)
    btn = st.button(label="Submit")
    if btn:
        st.session_state[f"{PAGE_NAME}__credit_card"] = credit_card
        st.session_state[PAGE_NAME] = "date_references"
        st.rerun()

# date references selection
if st.session_state[PAGE_NAME] == "date_references":
    statement_date = st.select_slider("Select statement date", range(1, 32))
    due_days_after_statement = st.select_slider(
        "How many days after your statement is your due date?", range(1, 45)
    )
    submit = st.button("Submit")
    if submit:
        st.session_state[f"{PAGE_NAME}__statement_date"] = statement_date
        st.session_state[f"{PAGE_NAME}__due_days_after_statement"] = (
            due_days_after_statement
        )
        st.session_state[PAGE_NAME] = "credit_card_nickname"
        st.rerun()

# choose credit card nickname
if st.session_state[PAGE_NAME] == "credit_card_nickname":
    nickname = st.text_input("Give your credit card a nick name:", max_chars=15)
    submit = st.button("Create Credit Card")
    if submit:
        st.session_state[f"{PAGE_NAME}__nickname"] = nickname
        st.session_state[PAGE_NAME] = "credit_card_instance_submitted"
        st.rerun()

if st.session_state[PAGE_NAME] == "credit_card_instance_submitted":
    # Let's now call the back-end

    # build the url
    api_url = f"{BACKEND_URL}/api/v1/credit_cards"
    _logger.info("Submitting credit card info to %s", api_url)

    # build the headers
    access_token = st.session_state.get("login__access_token", None)
    headers = {"Authorization": f"Bearer {access_token}"}

    # build the request body
    body = {
        "name": st.session_state[f"{PAGE_NAME}__nickname"],
        "credit_card": st.session_state[f"{PAGE_NAME}__credit_card"],
        "statement_day": str(st.session_state[f"{PAGE_NAME}__statement_date"]),
        "due_date_reference": int(
            st.session_state[f"{PAGE_NAME}__due_days_after_statement"]
        ),
    }
    _logger.debug("%s", body)

    # do the request
    with st.spinner("Adding credit card...", show_time=True):
        try:
            # If we're mocking, go here
            if st.session_state[helpers.CONFIG_USE_MOCKS_HOOK]:
                import time

                time.sleep(2.0)
                # testing the success
                response = SimpleNamespace(ok=True, content=None)

                # testing the fail
                # response = SimpleNamespace(ok=False, content=None)

            # otherwise, do the real api call
            else:
                response = requests.put(api_url, json=body, headers=headers)

            if response.ok:
                _logger.info("credit card added.")
                st.session_state[PAGE_NAME] = "credit_card_successfully_added"
                helpers.fetch_list_of_credit_cards.clear()
                st.rerun()
            else:
                raise ValueError

        except requests.exceptions.ConnectionError as err:
            _logger.error("Connection error found: %s", err)

        except Exception as gen:
            st.session_state[f"{PAGE_NAME}__api_error_encountered"] = True
            st.session_state[f"{PAGE_NAME}"] = "bank_and_network"
            _logger.info("Something went wrong on the API call: %s", api_url)
            _logger.info("%s", response.content)
            _logger.info("Then this lead to: %s", gen)
            st.rerun()


# Yey, show the success banner
if st.session_state[PAGE_NAME] == "credit_card_successfully_added":
    st.success("Credit card added! 🎉")
    st.write(
        "👀 We're now watching you"
        f", ___{st.session_state[f'{PAGE_NAME}__nickname']}___..."
    )
    create_another = st.button("Create another")
    if create_another:
        st.session_state[PAGE_NAME] = "bank_and_network"
        st.rerun()

# for dev purposes
if st.session_state.get("happybarra_config__dev_mode", False):
    st.write(st.session_state)
