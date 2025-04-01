import logging
import os

import dotenv
import streamlit as st
import requests
import pandas as pd
from io import StringIO

dotenv.load_dotenv()

_logger = logging.getLogger("happybarra.manage_credit_cards")


BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")


if not BACKEND_URL:
    raise ValueError("No backend found.")


st.markdown("""## 📂💳 Manage Credit Cards""")
st.markdown("""Add, delete, or modify your existing credit cards""")


@st.cache_data
def fetch_list_of_credit_cards(*, headers):
    _logger.debug("Fetching lists of credit cards")
    response = requests.get(
        f"{BACKEND_URL}/api/v1/credit_cards/credit_cards", headers=headers
    )
    return response


# Page keys
PAGE_KEY = "manage_credit_cards"
PK_LANDING = f"{PAGE_KEY}__landing"
PK_CHOOSE_OPERATION = f"{PAGE_KEY}__choosing_operation"

PK_CHANGE_STATEMENT_DATE = f"{PAGE_KEY}__changing_statement_date"
PK_CHANGE_DUE_DATE_REFERENCE = f"{PAGE_KEY}__changing_due_date_reference"
PK_CONFIRM_CHANGES = f"{PAGE_KEY}__confirming_deleting_card"
PK_OPERATION_SUCCESS = f"{PAGE_KEY}__operation_success"


PK_DELETE_CREDIT_CARD = f"{PAGE_KEY}__deleting_card"
PK_CONFIRM_DELETE_CREDIT_CARD = f"{PAGE_KEY}__confirming_deleting_card"

# Variable keys
VK_CHOSEN_CREDIT_CARD = f"{PAGE_KEY}__chosen_credit_card"
VK_CHOSEN_STATEMENT_DATE = f"{PAGE_KEY}__chosen_statement_date"
VK_CHOSEN_DUE_DATE_REFERENCE = f"{PAGE_KEY}__chosen_due_date_reference"


if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING


if st.session_state.get(PAGE_KEY) == PK_LANDING:
    _logger.debug("Querying credit cards from back-end")

    access_token = st.session_state.get("login__access_token", None)
    headers = {"Authorization": f"Bearer {access_token}"}

    _logger.debug("Using authorization header: %s", headers)

    with st.spinner("Loading credit cards...", show_time=True):
        st.markdown("### Credit Cards List")
        st.markdown("You have registered the following credit cards")

        # Here we're just going to display the credit cards
        response = fetch_list_of_credit_cards(headers=headers)
        df = pd.DataFrame.from_records((response.json()["data"]))

        col_rename = {
            "credit_card_instance__name": "name",
            "credit_card__name": "credit_card",
            "bank__name": "bank",
            "network__name": "network",
            "credit_card_instance__due_date_reference": "due_date_reference",
            "credit_card_instance__statement_day": "statement_day",
        }
        cols_in_user_view = [
            "name",
            "credit_card",
            "statement_day",
            "due_date_reference",
            "bank",
            "network",
        ]
        user_view_df = df.rename(col_rename, axis=1)
        st.dataframe(user_view_df[cols_in_user_view], hide_index=True)

        # Ask the user what they want to modify
        card_to_modify = st.selectbox(
            label="Select credit card to modify:",
            options=user_view_df["name"].to_list(),
        )
        submit_modify = st.button(label="Modify", key="Modify")

        if submit_modify:
            # isolate the card to modify
            card_filter = df["credit_card_instance__name"] == card_to_modify
            chosen_credit_card = df.loc[card_filter].to_dict(orient="records")

            # data validation
            if len(chosen_credit_card) > 1:
                st.error(
                    "There are two cards, related to the selected name. "
                    "Please annoy the developer into fixing this."
                )
                raise ValueError("Two credit card names exist for a user")

            _logger.debug("Card to modify: %s", card_to_modify)

            # modify st.session_state
            st.session_state[PAGE_KEY] = PK_CHOOSE_OPERATION
            st.session_state[VK_CHOSEN_CREDIT_CARD] = chosen_credit_card
            st.rerun()

if st.session_state.get(PAGE_KEY) == PK_CHOOSE_OPERATION:
    card_to_modify = st.session_state[VK_CHOSEN_CREDIT_CARD]

    operations_available = [
        "Change statement date",
        "Change due date reference",
        "Delete card",
    ]

    operation = st.selectbox(
        label="What do you want to do?", options=operations_available
    )
    submit_operation = st.button(label="Submit")
    if submit_operation:
        operation_to_page_key_mapper = {
            "Change statement date": PK_CHANGE_STATEMENT_DATE,
            "Change due date reference": PK_CHANGE_DUE_DATE_REFERENCE,
            "Delete card": PK_DELETE_CREDIT_CARD,
        }
        # modify st.session_state
        st.session_state[PAGE_KEY] = operation_to_page_key_mapper.get(operation)
        st.rerun()

if st.session_state.get(PAGE_KEY) == PK_CHANGE_STATEMENT_DATE:
    statement_date: int = st.select_slider("Select new statement date", range(1, 32))
    submit = st.button("Submit")
    if submit:
        credit_card: list = st.session_state[VK_CHOSEN_CREDIT_CARD]
        credit_card[0]["credit_card_instance__statement_day"] = statement_date
        print(credit_card)

        st.session_state[VK_CHOSEN_STATEMENT_DATE] = statement_date
        st.session_state[PAGE_KEY] = PK_OPERATION_SUCCESS
        st.rerun()

    # due_days_after_statement = st.select_slider(
    #     "How many days after your statement is your due date?", range(1, 45)
    # )
st.session_state
