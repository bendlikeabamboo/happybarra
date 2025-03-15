import logging

import streamlit as st
from st_pages import hide_pages

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

st.set_page_config(page_title="happybarra", page_icon="🐹")
home_page = st.Page("front-end/home.py", title="Home")
installment_page = st.Page(
    "front-end/credit_card_installment.py", title="Credit Card Installment"
)
credit_card_instance = st.Page(
    "front-end/create_credit_card_instance.py", title="Create Credit Card Instance"
)
login = st.Page("front-end/login.py",title="Access 🐹 happybarra")
hide_pages(["Home", "Credit Card Installment","Create Credit Card Instance"])


if not st.session_state.get("valid_session", False):
    pages_to_show = [login]
    pg = st.navigation(pages_to_show)
    pg.run()

if st.session_state.get("valid_session", False):
    pages_to_show = [home_page, installment_page, credit_card_instance]
    pg = st.navigation(pages_to_show)
    pg.run()





