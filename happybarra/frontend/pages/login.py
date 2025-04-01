import logging
import os
from types import SimpleNamespace

import requests
import streamlit as st
from dotenv import load_dotenv

from happybarra.frontend.services import helpers

# Create loggers first
_logger = logging.getLogger("happybarra.login")
_logger.debug("Loading environment variables")
load_dotenv()

# TODO: Environment scaffold
_logger.debug("Loading constants")
BACKEND_URL = os.getenv("LOCAL_BACKEND_URL")

#
# main part
#
st.write("👤 happybarra login")

#
# ERROR HANDLING
# If a failed attempt was done whatever the error is, show the error banner
if st.session_state.get("login__failed_attempt", False):
    _logger.debug("This is a log-in retry.")
    st.error("Invalid credentials")
else:
    _logger.debug("Fresh log-in")


_logger.debug("Assuming logged-out user.")
logged_in = st.session_state.get("login__logged_in", False)

_logger.debug("Asking for login-credentials")
if not logged_in:
    with st.form("login"):
        email = st.text_input("E-mail address:")
        password = st.text_input("Password", type="password")
        creds_submitted = st.form_submit_button(label="Login")

if creds_submitted:
    _logger.debug("Attempting login request")
    with st.spinner("Logging in...", show_time=True):
        try:
            # if dev-ing use this branch to bypass login request
            # NOTE: this doesn't authenticate you with the database so inserts will
            # mostly be an RLS violation
            if st.session_state[helpers.CONFIG_USE_MOCKS_HOOK]:
                import time

                time.sleep(1.5)
                response = SimpleNamespace(ok=True)
                # response = SimpleNamespace(ok=False)

            # For the production case, you will use the back-end API itself
            else:
                response: requests.Response = requests.post(
                    f"{BACKEND_URL}/api/v1/security/login",
                    data={"username": email, "password": password},
                )

            # if it's good
            if response.ok:
                _logger.debug("Login successful.")
                st.session_state["login__logged_in"] = True
                st.session_state["login__access_token"] = response.json()[
                    "access_token"
                ]
                st.session_state["login__token_type"] = response.json()["token_type"]
                st.session_state["login__refresh_token"] = response.json()[
                    "refresh_token"
                ]

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
            st.session_state["login__logged_in"] = False
            st.session_state["login__failed_attempt"] = True
            if "login__failed_attempt_counter" in st.session_state:
                st.session_state["login__failed_attempt_counter"] += 1
            else:
                st.session_state["login__failed_attempt_counter"] = 1
            _logger.error(
                "Invalid login attempt # %s\n",
                st.session_state["login__failed_attempt_counter"],
            )
            st.rerun()

# for dev purposes
if st.session_state.get("happybarra_config__dev_mode", False):
    st.write(st.session_state)
