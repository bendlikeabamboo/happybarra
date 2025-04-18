import logging
import time
from types import SimpleNamespace

import pandas as pd
import requests
import streamlit as st

from happybarra.frontend.services.helpers import (
    BACKEND_URL,
    CONFIG_USE_MOCKS_HOOK,
    build_authorization_header,
    fetch_list_of_credit_cards,
)

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")
_logger = logging.getLogger("happybarra.manage_credit_cards")

if not BACKEND_URL:
    raise ValueError("No backend found.")

# API endpoints
API_V1_CREDIT_CARDS_DELETE = f"{BACKEND_URL}/api/v1/credit_cards"

# Page keys
PAGE_KEY = "manage_credit_cards"
PK_LANDING = f"{PAGE_KEY}__landing"
PK_CHOOSE_OPERATION = f"{PAGE_KEY}__choosing_operation"

PK_OPERATION_FAILED = f"{PAGE_KEY}__operation_failed"
PK_OPERATION_SUCCESS = f"{PAGE_KEY}__operation_success"
PK_CONFIRM_CHANGES = f"{PAGE_KEY}__confirming_deleting_card"
PK_CHANGE_STATEMENT_DATE = f"{PAGE_KEY}__changing_statement_date"
PK_CHANGE_DUE_DATE_REFERENCE = f"{PAGE_KEY}__changing_due_date_reference"

PK_DELETE_CREDIT_CARD = f"{PAGE_KEY}__deleting_card"
PK_CONFIRM_DELETE_CREDIT_CARD = f"{PAGE_KEY}__confirming_deleting_card"

# Variable keys
VK_ERROR = f"{PAGE_KEY}__error"
VK_CHOSEN_CREDIT_CARD = f"{PAGE_KEY}__chosen_credit_card"
VK_CHOSEN_STATEMENT_DATE = f"{PAGE_KEY}__chosen_statement_date"
VK_CHOSEN_DUE_DATE_REFERENCE = f"{PAGE_KEY}__chosen_due_date_reference"


st.markdown("""## 🛠️ Manage Credit Cards""")
st.markdown("""Modify or delete one your existing credit cards""")


if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING


if st.session_state.get(PAGE_KEY) == PK_LANDING:
    _logger.debug("Querying credit cards from back-end")

    access_token = st.session_state.get("login__access_token", None)
    headers = {"Authorization": f"Bearer {access_token}"}

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
        # build out the request body

        # headers
        access_token = st.session_state.get("login__access_token", None)
        headers = {"Authorization": f"Bearer {access_token}"}

        # request body
        body = {}

        credit_card: list = st.session_state[VK_CHOSEN_CREDIT_CARD]
        body["id"] = credit_card[0]["credit_card_instance__id"]
        body["statement_day"] = str(statement_date)

        with st.spinner(text="Updating your card...", show_time=True):
            response = requests.post(
                f"{BACKEND_URL}/api/v1/credit_cards/update_credit_card_statement_date",
                headers=headers,
                json=body,
            )

            if response.ok:
                _logger.debug("request successful")
                st.session_state[PAGE_KEY] = PK_OPERATION_SUCCESS
                st.rerun()
            else:
                _logger.debug("request unsuccessful")
                st.error("Wow somethign went wrong here...")
                time.sleep(5)
                st.rerun()

if st.session_state.get(PAGE_KEY) == PK_CHANGE_DUE_DATE_REFERENCE:
    due_date_reference: int = st.select_slider(
        "Select new due date reference", range(1, 46)
    )
    submit = st.button("Submit")
    if submit:
        # build out the request body

        # headers
        access_token = st.session_state.get("login__access_token", None)
        headers = {"Authorization": f"Bearer {access_token}"}

        # request body
        body = {}

        credit_card: list = st.session_state[VK_CHOSEN_CREDIT_CARD]
        body["id"] = credit_card[0]["credit_card_instance__id"]
        body["due_date_reference"] = int(due_date_reference)

        with st.spinner(text="Updating your card...", show_time=True):
            response = requests.post(
                f"{BACKEND_URL}/api/v1/credit_cards/"
                "update_credit_card_due_date_reference",
                headers=headers,
                json=body,
            )
            if response.ok:
                _logger.debug("request successful")
                st.session_state[PAGE_KEY] = PK_OPERATION_SUCCESS
                st.rerun()
            else:
                _logger.debug("request unsuccessful")
                st.error("Wow something went wrong here...")
                time.sleep(5)
                st.rerun()

if st.session_state.get(PAGE_KEY) == PK_DELETE_CREDIT_CARD:
    credit_card = st.session_state.get(VK_CHOSEN_CREDIT_CARD)
    name = st.session_state[VK_CHOSEN_CREDIT_CARD][0]["credit_card_instance__name"]
    st.markdown(f"You are deleting your credit card **{name or '[blank name]'}**")
    st.markdown("Are you sure? 🥹")
    sure = st.button(label="I am sure 😔", type="primary")
    if sure:
        # build authorization header

        with st.spinner("Deleting card..."):
            if st.session_state[CONFIG_USE_MOCKS_HOOK]:
                response = SimpleNamespace(ok=True)
                # response = SimpleNamespace(ok=False, content="Mocking Failure")
            else:
                data = {"name": name}
                headers = build_authorization_header()
                response = requests.delete(
                    API_V1_CREDIT_CARDS_DELETE, headers=headers, json=data
                )

        if response.ok:
            st.session_state[PAGE_KEY] = PK_OPERATION_SUCCESS
            st.rerun()
        else:
            st.session_state[VK_ERROR] = response.content
            st.session_state[PAGE_KEY] = PK_OPERATION_FAILED
            st.rerun()


if st.session_state.get(PAGE_KEY) == PK_OPERATION_SUCCESS:
    st.success(body="Credit card operation success 🎉")
    go_back = st.button(label="Go back")
    if go_back:
        keys_to_delete = [key for key in st.session_state if key.startswith(PAGE_KEY)]
        for key in keys_to_delete:
            del st.session_state[key]
        st.session_state[PAGE_KEY] = PK_LANDING
        fetch_list_of_credit_cards.clear()
        st.rerun()

if st.session_state.get(PAGE_KEY) == PK_OPERATION_FAILED:
    st.error(
        body=f"Credit card operation failed 🥹. Error: {st.session_state[VK_ERROR]}"
    )
    go_back = st.button(label="Go back")
    if go_back:
        keys_to_delete = [key for key in st.session_state if key.startswith(PAGE_KEY)]
        for key in keys_to_delete:
            del st.session_state[key]
        st.session_state[PAGE_KEY] = PK_LANDING
        fetch_list_of_credit_cards.clear()
        st.rerun()
