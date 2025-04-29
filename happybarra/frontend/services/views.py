import logging

import pandas as pd
import requests
import streamlit as st

from .constants import BACKEND_URL
from .helpers import build_authorization_header
from .model_controllers import API_GET_DUES_SCHEDULE

_logger: logging.Logger = logging.getLogger(__name__)


@st.cache_data
def fetch_list_of_credit_cards(*, headers):
    _logger.debug("Fetching lists of credit cards")
    response = requests.get(f"{BACKEND_URL}/api/v1/credit_cards", headers=headers)
    return response


@st.cache_data
def get_dues_schedules():
    headers = build_authorization_header()
    response = requests.get(API_GET_DUES_SCHEDULE, headers=headers)
    return pd.DataFrame(response.json()["data"])
