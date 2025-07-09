from typing import List
import streamlit as st

import logging

from happybarra.frontend.services import (
    submit_and_go_back_buttons,
    submit_button,
    go_back_button,
    form_submit_button,
    form_submit_and_go_back_buttons,
)

import datetime as dt

import pandas as pd

from dateutil.relativedelta import relativedelta

_logger = logging.getLogger("happybarra.savings_schedule")

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")
st.markdown("# 💰 Savings Schedule")
st.markdown("Create a savings schedule! 🧐")


PAGE_KEY = "SAVINGS_SCHEDULE"
PREV_KEY = "SAVINGS_SCHEDULE_PREV"
PREV_PREV_KEY = "SAVINGS_SCHEDULE_PREV_PREV"
PK_LANDING = f"{PAGE_KEY}__LANDING"
PK_AMOUNT_TYPE_SELECTION = f"{PAGE_KEY}__AMOUNT_TYPE_SELECTION"
PK_AMOUNT_ENTRY = f"{PAGE_KEY}__AMOUNT_ENTRY"
PK_SHOW_SCHEDULE = f"{PAGE_KEY}__SHOW_SCHEDULE"
PK_DATE_ENTRY = f"{PAGE_KEY}__DATE_ENTRY"
PK_NAME_ENTRY = f"{PAGE_KEY}__NAME_ENTRY"
PK_ADD_TO_DUES = f"{PAGE_KEY}__ADD_TO_DUES"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"


VK_AMOUNT = f"{PAGE_KEY}__AMOUNT"
VK_PERIOD = f"{PAGE_KEY}__PERIOD"
VK_AMOUNT_TYPE = f"{PAGE_KEY}__AMOUNT_TYPE"
VK_START_DATE = f"{PAGE_KEY}__START_DATE"
VK_END_DATE = f"{PAGE_KEY}__END_DATE"
VK_SAVINGS_NAME = f"{PAGE_KEY}__SAVINGS_NAME"
VK_ = f"{PAGE_KEY}__"


BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"
BT_ = f"{PAGE_KEY}__"


FK_GOAL_TYPE = f"{PAGE_KEY}__GOAL_TYPE"
FK_AMOUNT_TYPE = f"{PAGE_KEY}__AMOUNT_TYPE"
FK_AMOUNT = f"{PAGE_KEY}__AMOUNT"
FK_ = f"{PAGE_KEY}__"
FK_ = f"{PAGE_KEY}__"
FK_ = f"{PAGE_KEY}__"
FK_ = f"{PAGE_KEY}__"
FK_ = f"{PAGE_KEY}__"


AMOUNT_PER_PERIOD = "Amount per period"
TOTAL_AMOUNT = "Total amount"


def generate_dates(start_date: dt.date, end_date: dt.date, delta: relativedelta):
    date = start_date

    while date < end_date:
        yield date
        date = date + delta


def create_savings_schedule(name: str, dates: List[dt.date], amount_per_period: float):
    return pd.DataFrame(
        [
            {
                "date": date,
                "amount": amount_per_period,
                "name": name,
            }
            for date in dates
        ]
    )


def get_dates(start_date: dt.date, end_date: dt.date, period: str):
    if period == "Monthly":
        delta = relativedelta(months=1)
    elif period == "Quarterly":
        delta = relativedelta(months=3)
    elif period == "Yearly":
        delta = relativedelta(years=1)
    else:
        delta = 0

    return [
        date
        for date in generate_dates(
            start_date=start_date, end_date=end_date, delta=delta
        )
    ]


def previous_page(prev_key):
    # referencing the page before
    if (
        PREV_KEY not in st.session_state
        or st.session_state[PREV_KEY] == st.session_state[PAGE_KEY]
    ):
        st.session_state[PREV_KEY] = prev_key


if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING

if st.session_state[PAGE_KEY] == PK_LANDING:
    previous_page(PK_LANDING)
    period = st.radio(
        "How often do you plan to save?",
        ["Monthly", "Quarterly", "Yearly", "One-off savings"],
        captions=["", "", "", "For bonuses or lottery jackpots 🤑"],
    )
    amount_type = st.radio(
        "Do you have a total goal amount or goal amount per period?",
        [
            AMOUNT_PER_PERIOD,
            TOTAL_AMOUNT,
        ],
    )
    submit = submit_button()
    if submit:
        st.session_state[VK_PERIOD] = period
        st.session_state[VK_AMOUNT_TYPE] = amount_type
        st.session_state[PAGE_KEY] = PK_AMOUNT_ENTRY
        st.session_state[PREV_KEY] = PK_LANDING
        st.rerun()

if st.session_state[PAGE_KEY] == PK_AMOUNT_ENTRY:
    previous_page(PK_LANDING)
    if st.session_state[VK_AMOUNT_TYPE] == AMOUNT_PER_PERIOD:
        label = "Enter " + st.session_state[VK_PERIOD].lower() + " amount"
    else:
        label = "Enter total amount"
    amount = st.number_input(
        label=label,
        step=500.00,
        format="%.2f",
        value=0.00,
    )
    submit, go_back = submit_and_go_back_buttons()
    if submit:
        st.session_state[VK_AMOUNT] = amount
        st.session_state[PAGE_KEY] = PK_DATE_ENTRY
        st.session_state[PREV_KEY] = PK_AMOUNT_ENTRY
        st.rerun()
    if go_back:
        st.session_state[PAGE_KEY] = st.session_state[PREV_KEY]
        st.rerun()

if st.session_state[PAGE_KEY] == PK_DATE_ENTRY:
    previous_page(PK_AMOUNT_ENTRY)
    start_date = st.date_input(
        "When does your savings plan start?", format="YYYY-MM-DD"
    )
    end_date = st.date_input("When does your savings plan end?", format="YYYY-MM-DD")
    submit, go_back = submit_and_go_back_buttons()
    if submit:
        st.session_state[VK_START_DATE] = start_date
        st.session_state[VK_END_DATE] = end_date
        st.session_state[PAGE_KEY] = PK_NAME_ENTRY
        st.session_state[PREV_KEY] = PK_DATE_ENTRY
        st.rerun()
    if go_back:
        st.session_state[PAGE_KEY] = st.session_state[PREV_KEY]
        st.rerun()

if st.session_state[PAGE_KEY] == PK_NAME_ENTRY:
    previous_page(PK_DATE_ENTRY)
    name = st.text_input("Name your savings plan 🤓", max_chars=100)
    submit, go_back = submit_and_go_back_buttons()
    if submit:
        st.session_state[VK_SAVINGS_NAME] = name
        st.session_state[PAGE_KEY] = PK_SHOW_SCHEDULE
        st.rerun()
    if go_back:
        st.session_state[PAGE_KEY] = st.session_state[PREV_KEY]
        st.rerun()

if st.session_state[PAGE_KEY] == PK_SHOW_SCHEDULE:
    previous_page(PK_NAME_ENTRY)
    amount = st.session_state[VK_AMOUNT]
    amount_type = st.session_state[VK_AMOUNT_TYPE]
    start_date = st.session_state[VK_START_DATE]
    end_date = st.session_state[VK_END_DATE]
    period = st.session_state[VK_PERIOD]
    name = st.session_state[VK_SAVINGS_NAME]
    dates = get_dates(start_date=start_date, end_date=end_date, period=period)

    if amount_type == AMOUNT_PER_PERIOD:
        amount_per_period = amount
    elif amount_type == TOTAL_AMOUNT:
        cycles = len(dates)
        amount_per_period = amount / cycles

    savings_df = create_savings_schedule(
        name=name, dates=dates, amount_per_period=amount_per_period
    )
    
    st.dataframe(
        savings_df,
        hide_index=True,
    )

    go_back = go_back_button()
    add_to_dues = st.button(label="Add to Dues", type="primary")
    if go_back:
        st.session_state[PAGE_KEY] = st.session_state[PREV_KEY]
        st.rerun()
    if add_to_dues:
        st.session_state[PAGE_KEY] = st.session_state[PK_ADD_TO_DUES]
