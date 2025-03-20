import logging.config
import os

import streamlit as st
import yaml

# from st_pages import hide_pages

# Let's first setup the logging
#
# Figure out the pathing
script_path = os.path.abspath(__file__)
dir_name = os.path.dirname(script_path)
config_path = os.path.join(dir_name, "debug_logging_conf.yaml")

# Then load the config yaml to setup the logging
with open(config_path, "rt") as file:
    config = yaml.safe_load(file.read())
logging.config.dictConfig(config=config)

# Now let's get a logger for this module.
_logger = logging.getLogger(__name__)

# Logger setup done.

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
    "pages/create_credit_card_instance.py", title="Create Credit Card Instance"
)
login = st.Page("pages/login.py", title="Access 🐹 happybarra")
# hide_pages(["Home", "Credit Card Installment", "Create Credit Card Instance"])

if not st.session_state.get("login__logged_in", False):
    pages_to_show = [login]
    pg = st.navigation(pages_to_show)
    pg.run()

if st.session_state.get("login__logged_in", False):
    pages_to_show = [home, installment, credit_card]
    pg = st.navigation(pages_to_show)
    pg.run()
