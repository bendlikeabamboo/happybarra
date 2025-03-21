import logging.config
import os

import streamlit as st
import yaml

from happybarra.frontend.data import banks, credit_cards, networks  # noqa: F401

# NOTE: they say this package hides pages from the sidebar
# from st_pages import hide_pages

#
# Let's first setup the logging
#

# Figure out the pathing for the log config
script_path = os.path.abspath(__file__)
dir_name = os.path.dirname(script_path)
config_path = os.path.join(dir_name, "debug_logging_conf.yaml")

# Then load the config yaml to setup the logging
with open(config_path, "rt") as file:
    config = yaml.safe_load(file.read())
logging.config.dictConfig(config=config)

# Now let's get a logger for this module.
_logger = logging.getLogger("happybarra")

#
# Logger setup done.
#

# Setup streamlit page config
st.set_page_config(page_title="happybarra", page_icon="🐹")

#
# Define the pages
#

home = st.Page("pages/home.py", title="Home")
installment = st.Page(
    "pages/credit_card_installment.py", title="Credit Card Installment"
)
credit_card = st.Page(
    "pages/add_credit_card.py", title="Add Credit Card Tracker"
)
login = st.Page("pages/login.py", title="Access 🐹 happybarra")
logout = st.Page("pages/logout.py", title="Logout")
# hide_pages(["Home", "Credit Card Installment", "Create Credit Card Instance"])

#
# Page control.
#
# At first only show login. After successfully logging in, you can now access the other
# pages.
#

# If dev-ing, you also turn this on:
# st.session_state["login__logged_in"] = True

if not st.session_state.get("login__logged_in", False):
    pages_to_show = {"Login": [login]}
    pg = st.navigation(pages_to_show)
    pg.run()

if st.session_state.get("login__logged_in", False):
    pages_to_show = {
        "": [home],
        "Calculators": [installment],
        "Account": [credit_card, logout],
    }
    pg = st.navigation(pages_to_show)
    pg.run()
