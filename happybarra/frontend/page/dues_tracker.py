import logging
import math
import os
from typing import List

import pandas as pd
import streamlit as st
from bokeh.core.enums import HatchPattern
from bokeh.models import AdaptiveTicker, FactorRange, NumeralTickFormatter
from bokeh.plotting import figure
from dotenv import load_dotenv
from streamlit_bokeh import streamlit_bokeh

from happybarra.frontend.services import get_dues_schedules, happy

_logger = logging.getLogger("happybarra.dues_tracker")

load_dotenv()

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="wide")


BACKEND_URL = os.getenv("LOCAL_BACKEND_URL", "http://localhost:8000")

# Page title

PAGE_KEY = "DUES_TRACKER"

PK_LANDING = f"{PAGE_KEY}__LANDING"
PK_NO_DUES = f"{PAGE_KEY}__NO_DUES"

VK_YEAR_SELECTION = f"{PAGE_KEY}__YEAR_SELECTION"
VK_GROUP_BY = f"{PAGE_KEY}__GROUP_BY"
VK_SOURCE_NAME_EXTENDED = f"{PAGE_KEY}__SOURCE_NAME_EXTENDED"
VK_NAME = f"{PAGE_KEY}__NAME"

FK_FILTERS = f"{PAGE_KEY}__FILTERS"

st.markdown("# 📉 Dues Tracker")
st.markdown("Have a look! 🥳")
st.markdown("---")
if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING

if st.session_state[PAGE_KEY] == PK_LANDING:
    with st.spinner(text="Getting your dues...", show_time=True):
        data = get_dues_schedules()

    # If no dues, proceed to another page
    if len(data) == 0:
        st.session_state[PAGE_KEY] = PK_NO_DUES
        st.rerun()

    ###
    #   Dashboard
    ###

    data["year"] = pd.to_datetime(data["due_date"]).dt.year
    data["due_month"] = (
        pd.to_datetime(data["due_date"]).dt.to_period("M").dt.to_timestamp()
    )
    years: List[int] = list(data["year"].unique())
    source_name_extended: List[str] = list(
        data["financial_commitment__source_name_extended"].unique()
    )
    names: List[str] = list(list(data["financial_commitment__name"].unique()))
    lean_cols = [
        "financial_commitment__name",
        "due_month",
        "amount",
        "year",
        "financial_commitment__source_name_extended",
        "source_type",
    ]
    user_friendly_groupers = {
        "Due Name": "financial_commitment__name",
        "Due Source": "financial_commitment__source_name_extended",
        "Source Type": "source_type",
    }

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("##### Filters ")
        with st.form(key=FK_FILTERS, border=True):
            i_col1, i_col2 = st.columns(2)
            with i_col1:
                year_selection = st.selectbox(
                    label="Select year", options=years, key=VK_YEAR_SELECTION
                )
            with i_col2:
                groupby = st.selectbox(
                    label="Group by", options=user_friendly_groupers, key=VK_GROUP_BY
                )
            name_filters = st.multiselect(
                label="Select due", options=names, key=VK_NAME
            )
            source_name_filters = st.multiselect(
                label="Select due source",
                options=source_name_extended,
                key=VK_SOURCE_NAME_EXTENDED,
            )
            st.form_submit_button(label="Apply filters")

    with col2:
        # st.dataframe(data)
        year_filter = data["year"] == year_selection

        if name_filters:
            name_filter = data["financial_commitment__name"].isin(name_filters)
        else:
            name_filter = True

        if source_name_filters:
            source_name_filter = data[
                "financial_commitment__source_name_extended"
            ].isin(source_name_filters)
        else:
            source_name_filter = True

        lean_df = data.loc[year_filter & source_name_filter & name_filter, lean_cols]
        if len(lean_df) == 0:
            st.success("🥳 No dues found!")
        else:
            pivoted_df = lean_df.pivot_table(
                values="amount",
                index=user_friendly_groupers[groupby],
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

            max_amount = max(pivoted_df.sum())
            # st.write(pivoted_df)
            range_series = b_data["monthyear"]

            pats = list(HatchPattern)

            chart = figure(
                x_range=range_series,
                y_range=(0, max_amount * 1.33),
                title="Dues per month",
                x_axis_label="Month",
                y_axis_label="Amount (₱)",
                toolbar_location="above",
            )

            chart.vbar_stack(
                unique_installment_id,
                x="monthyear",
                width=0.5,
                color=happy[: len(unique_installment_id)],
                hatch_pattern=pats[: len(unique_installment_id)],
                legend_label=unique_installment_id,
                source=b_data,
            )
            chart.xaxis.major_label_orientation = math.pi / 4
            chart.x_range = FactorRange(*b_data["monthyear"])
            chart.window_axis = "y"
            chart.yaxis[0].formatter = NumeralTickFormatter(format=",.00")
            chart.yaxis[0].ticker = AdaptiveTicker(
                desired_num_ticks=10, num_minor_ticks=4
            )
            chart.max_height = 600
            chart.legend.click_policy = "hide"
            chart.legend.location = "top_center"
            chart.legend.orientation = "horizontal"

            # chart.x_range.bounds = b_data["monthyear"][:12]

            streamlit_bokeh(
                chart,
                use_container_width=True,
            )

if st.session_state[PAGE_KEY] == PK_NO_DUES:
    st.success("No dues as of the moment 🥳")
