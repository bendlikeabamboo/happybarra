import logging
import os
from types import SimpleNamespace

import requests
import streamlit as st
from dotenv import load_dotenv

# Create loggers first
_logger = logging.getLogger("happybarra.logout")
_logger.debug("Loading environment variables")
load_dotenv()

# TODO: Environment scaffold
_logger.debug("Loading constants")
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")

#
# main part
#
st.write("## Logout")
st.write("Are you sure? 🥹")

#
# ERROR HANDLING
# If a failed attempt was done whatever the error is, show the error banner
if st.session_state.get("logout__failed_attempt", False):
    _logger.debug("This is a log-out retry.")
    st.error("Logout failed.")
else:
    _logger.debug("Fresh log-out")


_logger.debug("Assuming logged-in user.")
logged_in = st.session_state.get("login__logged_in", True)

if logged_in:
    log_out = st.button(label="Logout")

    # TODO: Erase session info here
    if log_out:
        _logger.debug("Attempting logout request")
        with st.spinner("Logging out...", show_time=True):
            try:
                # response = requests.post(
                #     f"{BACKEND_URL}/api/v1/logout",
                #     json={"email": email, "password": password},
                # )

                # if dev-ing use this to bypass login request
                # NOTE: this doesn't authenticate you with the database so inserts will
                # mostly be an RLS violation
                import time

                time.sleep(2)
                response = SimpleNamespace(ok=True)

                # if it's good
                if response.ok:
                    _logger.debug("Logout successful.")
                    st.session_state["login__logged_in"] = False
                    st.rerun()

                # if it's not
                raise ValueError

            except requests.exceptions.ConnectionError as err:
                _logger.error(
                    "Trouble connecting to the back-end server. "
                    "Might be the back-end is not instantiated? %s",
                    err,
                )
                st.rerun()

            except ValueError as err:
                _logger.error("Trouble logging in. %s", err)
                st.session_state["logout__failed_attempt"] = True
                if "logout__failed_attempt_counter" in st.session_state:
                    st.session_state["logout__failed_attempt_counter"] += 1
                else:
                    st.session_state["logout__failed_attempt_counter"] = 1
                _logger.error(
                    "Invalid logout attempt # %s",
                    st.session_state["login__failed_attempt_counter"],
                )
                st.rerun()

# for dev purposes
if st.session_state.get("happybarra_config__dev_mode", False):
    st.write(st.session_state)
