import logging

import streamlit as st

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

home_page = st.Page("front-end/home.py", title="Home")
installment_page = st.Page(
    "front-end/credit_card_installment.py", title="Credit Card Installment"
)
credit_card_instance = st.Page(
    "front-end/credit_card_instance.py", title="Credit Card Instance"
)
pg = st.navigation([home_page, installment_page, credit_card_instance])
st.set_page_config(page_title="happybarra", page_icon="🐹")
pg.run()
