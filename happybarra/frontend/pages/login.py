import logging
import os

import requests
import streamlit as st
from dotenv import load_dotenv

# Create loggers first
_logger = logging.getLogger(__name__)

_logger.debug("Loading environment variables")
load_dotenv()

# TODO: Environment scaffold
_logger.debug("Loading constants")
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")


# Functions we're going to use
def login(email: str, password: str) -> None:
    # login in the back-end
    response = requests.post(
        f"{BACKEND_URL}/api/v1/login",
        json={"email": email, "password": password},
    )

    # if it's good
    if response.ok:
        st.session_state["{__name__}__logged_in"] = True
        st.rerun()

    # if it's not
    else:
        st.session_state["{__name__}__logged_in"] = False
        st.session_state["{__name__}__failed_attempt"] = True
        if "{__name__}__failed_attempt_counter" in st.session_state:
            st.session_state["{__name__}__failed_attempt_counter"] += 1
        else:
            st.session_state["{__name__}__failed_attempt_counter"] = 1

        _logger.error(
            "Invalid login attempt # %s",
            st.session_state["{__name__}__failed_attempt_counter"],
        )
        st.rerun()


#
# main part
#

_logger.debug("Assuming logged-out user.")
logged_in = st.session_state.get("{__name__}__logged_in", False)

_logger.debug("Asking for login-credentials")
st.write("👤 happybarra login")
if not logged_in:
    if st.session_state.get("{__name__}__failed_attempt", False):
        _logger.debug("This is a log-in retry.")
        st.error("Invalid credentials")
    else:
        _logger.debug("Fresh log-in")

    with st.form(key=__name__):
        email = st.text_input("E-mail address:")
        password = st.text_input("Password", type="password")
        creds_submitted = st.form_submit_button(
            label="Login", on_click=login, args=(email, password)
        )
