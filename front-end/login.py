import streamlit as st
from supabase import AuthApiError
import logging
from dotenv import load_dotenv
import os
import requests


load_dotenv()
_logger = logging.getLogger(__name__)
logged_in = st.session_state.get("login__logged_in", False)

BACKEND_URL = os.getenv("DEV_BACKEND_URL")


if not logged_in:
    st.write("👤 happybarra login")

    if st.session_state.get("login__failed_attempt", False):
        st.error("Invalid credentials")

    email = st.text_input("E-mail address:")
    password = st.text_input("Password", type="password")
    creds_submitted = st.button("login")

    if creds_submitted:
        try:
            # login via the backend
            response = requests.post(BACKEND_URL, json={
                "email": email,
                "password": password
            })
            if response.ok:
                st.session_state["login__logged_in"] = True
                st.rerun()

        except AuthApiError as err:
            st.session_state["login__logged_in"] = False
            st.session_state["login__failed_attempt"] = True

            if "login__failed_attempt_counter" in st.session_state:
                st.session_state["login__failed_attempt_counter"] += 1
            else:
                st.session_state["login__failed_attempt_counter"] = 1
            
            _logger.error("Invalid Credentials entered. \nError: %s", err)
            st.rerun()
