import streamlit as st
import requests

from dotenv import load_dotenv

import os
import logging

from happybarra.frontend.services.helpers import (
    build_authorization_header,
    get_dues_schedules,
)

import pandas as pd
from bokeh.plotting import figure, show
from bokeh.palettes import HighContrast3, GnBu6, Bokeh8, OrRd9, Inferno, inferno, Paired12
from streamlit_bokeh import streamlit_bokeh

import datetime as dt
import math
from dateutil.relativedelta import relativedelta
from bokeh.core.enums import HatchPattern



_logger = logging.getLogger("happybarra.dues_tracker")

load_dotenv()

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")


BACKEND_URL = os.getenv("LOCAL_BACKEND_URL", "http://localhost:8000")

# Page title

PAGE_KEY = "manage_dues"

PK_LANDING = f"{PAGE_KEY}__LANDING"

if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING

if st.session_state[PAGE_KEY] == PK_LANDING:
    st.markdown("# 📉 Dues Tracker")
    st.markdown("Care to see your dues 😓")

    data = get_dues_schedules()
    if len(data) == 0:
        st.success("No dues as of the moment 🥳")
    else:
        data["due_month"] = (
            pd.to_datetime(data["due_date"]).dt.to_period("M").dt.to_timestamp()
        )
        lean_cols = ["financial_commitment__name", "due_month", "amount"]
        lean_df = data[lean_cols]

        pivoted_df = lean_df.pivot_table(
            values="amount",
            index="financial_commitment__name",
            columns="due_month",
        )
        pivoted_df = pivoted_df.fillna(0)
        unique_installment_id = pivoted_df.index.unique().to_list()

        # st.write(pivoted_df)
        pivoted_df.columns = pivoted_df.columns.strftime("%b %Y")
        b_data = {"monthyear": pivoted_df.columns.to_list()}
        for idx in pivoted_df.index.to_list():
            b_data[idx] = pivoted_df.loc[idx, :].to_list()
        # st.write(b_data)

        max_amount = data["amount"].max()
        # st.write(pivoted_df)
        range_series = b_data["monthyear"]

        pats = list(HatchPattern)

        FIGURE = figure(
            x_range=range_series,
            title="Credit card installments per month",
            x_axis_label="Month",
            y_axis_label="Amount (₱)",
            y_minor_ticks=3
        )

        FIGURE.vbar_stack(
            unique_installment_id,
            x="monthyear",
            width=0.5,
            color=Paired12[:len(unique_installment_id)],
            hatch_pattern=pats[: len(unique_installment_id)],
            legend_label=unique_installment_id,
            source=b_data,
        )
        FIGURE.xaxis.major_label_orientation = math.pi / 4

        streamlit_bokeh(FIGURE)
