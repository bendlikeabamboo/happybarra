import logging
from types import SimpleNamespace

import pandas as pd
import streamlit as st

from happybarra.frontend.models import (
    Bank,
    CreditCard,
    CreditCardInstallment,
    CreditCardInstance,
    InstallmentAmountType,
    Network,
)
from happybarra.frontend.services.helpers import (
    CONFIG_USE_MOCKS_HOOK,
    build_authorization_header,
    bulk_create_new_installment_schedules,
    create_new_installment,
    fetch_list_of_credit_cards,
    get_dues_schedules,
    get_installment_by_name,
)

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")

PAGE_KEY = "credit_card_installment"
PK_KEY_DATE_SELECTION = f"{PAGE_KEY}__key_date_selection"
PK_DEFINE_INSTALLMENT = f"{PAGE_KEY}__define_installment"
PK_INSTALLMENT_SCHEDULE = f"{PAGE_KEY}__installment_schedule"
PK_CREDIT_CARD_SELECTION = f"{PAGE_KEY}__credit_card_selection"
PK_BANK_AND_NETWORK_SELECTION = f"{PAGE_KEY}__bank_and_network_selection"
PK_ADD_TO_DUES = f"{PAGE_KEY}__ADD_TO_DUES"


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
VK_EXISTING_CREDIT_CARD_USED = f"{PAGE_KEY}__EXISTING_CREDIT_CARD_USED"
VK_INSTALLMENT_DF = f"{PAGE_KEY}__INSTALLMENT_DF"
VK_INSTALLMENT_NAME = f"{PAGE_KEY}__INSTALLMENT_NAME"
VK_CREATED_INSTALLMENT_ID = f"{PAGE_KEY}__VK_CREATED_INSTALLMENT_ID"
VK_ERROR_ON_INSTALLMENT_CREATION = f"{PAGE_KEY}__VK_ERROR_ON_INSTALLMENT_CREATION"
VK_SUCCESSFULLY_ADDED_TO_DUES = f"{PAGE_KEY}__VK_SUCCESSFULLY_ADDED_TO_DUES"


BT_USE_EXISTING_CREDIT_CARD = f"{PAGE_KEY}__USE_EXISTING_CREDIT_CARD"

INSTALLMENT_TYPE_CHOICES = {
    "Fixed Monthly": InstallmentAmountType.MONTHLY_FIXED,
    "Fixed Total": InstallmentAmountType.TOTAL_FIXED,
}


_logger = logging.getLogger(f"happybarra.{PAGE_KEY}")

st.markdown("# 🗓️ Installment Schedule")
st.markdown("Get a list of your installment due dates 😉.")

st.info(
    "We don't collect any important credit card  details, "
    "only statement day and due date.",
    icon="📝",
)
st.markdown("---")

# Initialize the app
if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION

# Display the error markdown if there's an invalid combination chosen
if st.session_state.get(VK_INVALID_COMBINATION_CHOSEN, False):
    st.error("Invalid combination chosen. Choose again.")

    # Let's now reset the state so by next st.rerun(), we don't show the error banner
    # again.
    st.session_state[VK_INVALID_COMBINATION_CHOSEN] = False

if st.session_state.get(VK_ERROR_ON_INSTALLMENT_CREATION, False):
    st.error("Something went wrong while adding your installment. Please try again.")
    st.session_state[VK_ERROR_ON_INSTALLMENT_CREATION] = False

if st.session_state.get(VK_SUCCESSFULLY_ADDED_TO_DUES, False):
    st.success(
        "🎉 Installment successfully added. Go to __💸 Dues Tracker__ "
        "to view your dues."
    )
    st.session_state[VK_SUCCESSFULLY_ADDED_TO_DUES] = False

# Bank and network subpage
if st.session_state[PAGE_KEY] == PK_BANK_AND_NETWORK_SELECTION:
    _logger.debug("Asking for bank and network")
    st.markdown("Enter your credit card info:")
    bank = st.selectbox("Bank", [bank for bank in Bank.registry])
    network = st.selectbox("Network", [network for network in Network.registry])
    bank_and_network_submitted = st.button("Submit")

    _logger.debug("Also offering user a list of his credit cards")
    headers = build_authorization_header()
    credit_cards = pd.DataFrame(
        fetch_list_of_credit_cards(headers=headers).json()["data"]
    )
    names = (
        credit_cards["credit_card_instance__name"]
        + " — "
        + credit_cards["credit_card__name"]
    ).to_list()
    if len(names) != 0:
        st.markdown("---")
        st.markdown("Or use one of your tracked credit cards")
        user_credit_card_selection = st.selectbox("", options=names)
        use_credit_card_submitted = st.button(
            key=BT_USE_EXISTING_CREDIT_CARD, label="Submit"
        )

    if bank_and_network_submitted:
        st.session_state[VK_BANK] = bank
        st.session_state[VK_NETWORK] = network
        st.session_state[PAGE_KEY] = PK_CREDIT_CARD_SELECTION
        st.rerun()

    if use_credit_card_submitted:
        selected_cc = user_credit_card_selection.split(" — ")[0]
        matched_cc = credit_cards[
            credit_cards["credit_card_instance__name"] == selected_cc
        ]

        # data validation
        if len(matched_cc) != 1:
            raise ValueError(
                "We're only suppose to have one credit card with this name."
            )

        matched_cc = matched_cc.to_dict(orient="records")[0]

        st.session_state[VK_BANK] = matched_cc["bank__name"]
        st.session_state[VK_NETWORK] = matched_cc["network__name"]
        st.session_state[VK_STATEMENT_DATE] = matched_cc[
            "credit_card_instance__statement_day"
        ]
        st.session_state[VK_DUE_DATE_REF] = matched_cc[
            "credit_card_instance__due_date_reference"
        ]
        st.session_state[VK_CREDIT_CARD_KEY] = matched_cc["credit_card__name"]
        st.session_state[VK_CREDIT_CARD_OBJECT] = CreditCard.registry[
            matched_cc["credit_card__name"]
        ]
        st.session_state[VK_CREDIT_CARD_INSTANCE] = CreditCardInstance(
            credit_card=st.session_state[VK_CREDIT_CARD_OBJECT],
            statement_day=st.session_state[VK_STATEMENT_DATE],
            due_date_ref=st.session_state[VK_DUE_DATE_REF],
        )
        st.session_state[PAGE_KEY] = PK_DEFINE_INSTALLMENT
        st.session_state[VK_EXISTING_CREDIT_CARD_USED] = matched_cc
        st.rerun()

        # st.session_state[VK_BANK] =

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

    installment_type = st.radio(
        "What installment amount do you know?", INSTALLMENT_TYPE_CHOICES
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
            amount_type=INSTALLMENT_TYPE_CHOICES[installment_type],
            amount=installment_amount,
            start_date=date_input,
        )
        st.session_state[PAGE_KEY] = PK_INSTALLMENT_SCHEDULE
        st.rerun()

if st.session_state[PAGE_KEY] == PK_INSTALLMENT_SCHEDULE:
    _logger.debug("Showing installment plan.")
    installment: CreditCardInstallment = st.session_state[VK_INSTALLMENT_INSTANCE]
    df = pd.DataFrame(installment.get_charge_dates())
    st.dataframe(df, hide_index=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        done = st.button("Done", type="secondary")
    with col3:
        if st.session_state.get(VK_EXISTING_CREDIT_CARD_USED, False):
            add_to_dues = st.button("Add to dues", type="primary")

    if done:
        # cleanup
        for key in st.session_state:
            if PAGE_KEY in key:
                del st.session_state[key]
        st.rerun()
    if add_to_dues:
        st.session_state[PAGE_KEY] = PK_ADD_TO_DUES
        st.session_state[VK_INSTALLMENT_DF] = df
        st.rerun()


if st.session_state[PAGE_KEY] == PK_ADD_TO_DUES:
    df: pd.DataFrame = st.session_state.get(VK_INSTALLMENT_DF)
    st.write(df)

    installment_name = st.text_input(
        label="Name your installment:", key=VK_INSTALLMENT_NAME, max_chars=100
    )
    submit_installment_name = st.button(label="Submit")

    credit_card_instance_id = st.session_state[VK_EXISTING_CREDIT_CARD_USED][
        "credit_card_instance__id"
    ]

    if submit_installment_name:
        # {
        #     "name": "string",
        #     "credit_card_instance_id": "string",
        #     "amount_type": "string",
        #     "amount": 0,
        # }

        data = {
            "name": installment_name,
            "credit_card_instance_id": credit_card_instance_id,
            "amount_type": INSTALLMENT_TYPE_CHOICES[
                st.session_state[VK_INSTALLMENT_TYPE]
            ],
            "amount": st.session_state[VK_INSTALLMENT_AMOUNT],
        }
        headers = build_authorization_header()
        if not st.session_state[CONFIG_USE_MOCKS_HOOK]:
            st.write(data)
            st.write(headers)
            response = create_new_installment(data=data, headers=headers)
        else:
            response = SimpleNamespace(ok=True)
            # response = SimpleNamespace(ok=False)
        if not response.ok:
            st.session_state[VK_ERROR_ON_INSTALLMENT_CREATION] = True
            st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION
            st.rerun()

        # Get the newly created installment's ID
        response = get_installment_by_name(name=installment_name, headers=headers)
        if not response.ok:
            st.session_state[VK_ERROR_ON_INSTALLMENT_CREATION] = True
            st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION
            st.rerun()
        new_installment_id = response.json()["data"][0]["id"]

        # Using the obtained ID, begin upload sequence for the installment schedule
        df = df.rename({"bill_post_date": "bill_date"}, axis=1)
        df["credit_card_installment_id"] = new_installment_id
        df = df.drop("credit_card_name", axis=1)
        date_cols = ["due_date", "bill_date", "statement_date"]
        for date_col in date_cols:
            df[date_col] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
        body = df.to_dict(orient="records")
        headers = build_authorization_header()
        response = bulk_create_new_installment_schedules(data=body, headers=headers)

        if not response.ok:
            st.session_state[VK_ERROR_ON_INSTALLMENT_CREATION] = True
            st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION
            st.rerun()

        get_dues_schedules.clear()
        st.session_state[VK_SUCCESSFULLY_ADDED_TO_DUES] = True
        st.session_state[PAGE_KEY] = PK_BANK_AND_NETWORK_SELECTION
        st.rerun()
