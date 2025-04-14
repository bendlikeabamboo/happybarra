import logging
import os
from types import SimpleNamespace

import requests
import streamlit as st
from dotenv import load_dotenv

from happybarra.frontend.models import Bank, CreditCard, Network
from happybarra.frontend.services import helpers

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")

_logger = logging.getLogger("happybarra.add_credit_card")


# Page Keys
PAGE_KEY = "add_credit_card"
PK_BANK_AND_NETWORK = f"{PAGE_KEY}__BANK_AND_NETWORK"
PK_CREDIT_CARD_SELECTION = f"{PAGE_KEY}__CREDIT_CARD_SELECTION"
PK_CREDIT_CARD_NAME_ENTRY = f"{PAGE_KEY}__CREDIT_CARD_NAME_ENTRY"
PK_CREDIT_CARD_SUBMISSION = f"{PAGE_KEY}__CREDIT_CARD_SUBMISSION"
PK_DATE_REFERENCES_SELECTION = f"{PAGE_KEY}__DATE_REFERENCES_SELECTION"
PK_CREDIT_CARD_SUBMISSION_SUCCESS = f"{PAGE_KEY}__CREDIT_CARD_SUBMISSION_SUCCESS"

# Variable Keys
VK_BANK = f"{PAGE_KEY}__BANK"
VK_NETWORK = f"{PAGE_KEY}__NETWORK"
VK_CREDIT_CARD = f"{PAGE_KEY}__CREDIT_CARD"
VK_STATEMENT_DAY = f"{PAGE_KEY}__STATEMENT_DAY"
VK_CREDIT_CARD_NAME = f"{PAGE_KEY}__CREDIT_CARD_NAME"
VK_DUE_DATE_REFERENCE = f"{PAGE_KEY}__DUE_DATE_REFERENCE"
VK_CREDIT_CARD_SUBMITTED = f"{PAGE_KEY}__CREDIT_CARD_SUBMITTED"
VK_API_ERROR_ENCOUNTERED = f"{PAGE_KEY}__API_ERROR_ENCOUNTERED"
VK_INVALID_COMBINATION_CHOSEN = f"{PAGE_KEY}__INVALID_COMBINATION_CHOSEN"


load_dotenv()
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")

st.markdown("# 💳 Add Credit Card")
st.markdown("Let's track your cards!")


# Define the page start point
if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK

#
# ERROR HANDLING:
# If an invalid combination is chosen later in the script, show the error banner
if st.session_state.get(VK_INVALID_COMBINATION_CHOSEN, False):
    # show the banner
    st.error("Invalid combination chosen.")
    # reset the state so we don't show this again next page
    st.session_state[VK_INVALID_COMBINATION_CHOSEN] = False

#
# ERROR HANDLING:
# If an API error is found later in the script, show the error banner
if st.session_state.get(VK_API_ERROR_ENCOUNTERED, False):
    # show the banner
    st.error(
        "There was an error encountered while adding credit card. Try again later."
    )
    # reset the state so we don't show this again next page
    st.session_state[VK_API_ERROR_ENCOUNTERED] = False

# Bank and network selection
if st.session_state[PAGE_KEY] == PK_BANK_AND_NETWORK:
    _logger.debug("Selecting bank and network")
    bank = st.selectbox("Select bank", Bank.registry)
    network = st.selectbox("Select network", Network.registry)
    submit = st.button("Submit")
    if submit:
        st.session_state[VK_BANK] = bank
        st.session_state[VK_NETWORK] = network
        st.session_state[PAGE_KEY] = PK_CREDIT_CARD_SELECTION
        st.rerun()

# credit card selection
if st.session_state[PAGE_KEY] == PK_CREDIT_CARD_SELECTION:
    # create variables from previous page:
    bank: str = st.session_state[VK_BANK]
    network: str = st.session_state[VK_NETWORK]

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
        st.session_state[VK_INVALID_COMBINATION_CHOSEN] = True
        st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK
        st.rerun()

    # use the retrieved ccs here:
    credit_card = st.selectbox("Select Credit Card", matching_ccs)
    btn = st.button(label="Submit")
    if btn:
        st.session_state[VK_CREDIT_CARD] = credit_card
        st.session_state[PAGE_KEY] = PK_DATE_REFERENCES_SELECTION
        st.rerun()

# date references selection
if st.session_state[PAGE_KEY] == PK_DATE_REFERENCES_SELECTION:
    statement_date = st.select_slider("Select statement date", range(1, 32))
    due_days_after_statement = st.select_slider(
        "How many days after your statement is your due date?", range(1, 45)
    )
    submit = st.button("Submit")
    if submit:
        st.session_state[VK_STATEMENT_DAY] = statement_date
        st.session_state[VK_DUE_DATE_REFERENCE] = due_days_after_statement
        st.session_state[PAGE_KEY] = PK_CREDIT_CARD_NAME_ENTRY
        st.rerun()

# choose credit card nickname
if st.session_state[PAGE_KEY] == PK_CREDIT_CARD_NAME_ENTRY:
    nickname = st.text_input("Give your credit card a nick name:", max_chars=30)
    submit = st.button("Create Credit Card")
    if submit:
        st.session_state[VK_CREDIT_CARD_NAME] = nickname
        st.session_state[PAGE_KEY] = PK_CREDIT_CARD_SUBMISSION
        st.rerun()

if st.session_state[PAGE_KEY] == PK_CREDIT_CARD_SUBMISSION:
    # Let's now call the back-end

    # build the url
    api_url = f"{BACKEND_URL}/api/v1/credit_cards"
    _logger.info("Submitting credit card info to %s", api_url)

    # build the headers
    access_token = st.session_state.get("login__access_token", None)
    headers = {"Authorization": f"Bearer {access_token}"}

    # build the request body
    body = {
        "name": st.session_state[VK_CREDIT_CARD_NAME],
        "credit_card": st.session_state[VK_CREDIT_CARD],
        "statement_day": str(st.session_state[VK_STATEMENT_DAY]),
        "due_date_reference": int(st.session_state[VK_DUE_DATE_REFERENCE]),
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
                st.session_state[PAGE_KEY] = PK_CREDIT_CARD_SUBMISSION_SUCCESS
                helpers.fetch_list_of_credit_cards.clear()
                st.rerun()
            else:
                raise ValueError

        except requests.exceptions.ConnectionError as err:
            _logger.error("Connection error found: %s", err)

        except Exception as gen:
            st.session_state[VK_API_ERROR_ENCOUNTERED] = True
            st.session_state[PK_BANK_AND_NETWORK] = PK_BANK_AND_NETWORK
            _logger.info("Something went wrong on the API call: %s", api_url)
            _logger.info("%s", response.content)
            _logger.info("Then this led to: %s", gen)
            st.rerun()


# Yey, show the success banner
if st.session_state[PAGE_KEY] == PK_CREDIT_CARD_SUBMISSION_SUCCESS:
    st.success("Credit card added! 🎉")
    st.write(
        f"👀 We're now watching you, ___{st.session_state[VK_CREDIT_CARD_NAME]}___..."
    )
    create_another = st.button("Create another")
    if create_another:
        for key in st.session_state:
            if PAGE_KEY in key:
                del st.session_state[key]
        st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK
        st.rerun()
