import logging

import pandas as pd
import streamlit as st
import traceback
from happybarra.models import (
    CreditCard,
    CreditCardInstallment,
    Bank,
    Network,
    CreditCardInstance,
)
from happybarra.enums import InstallmentAmountType
from happybarra.banks import *
from happybarra.networks import *
from happybarra.credit_cards import *

logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)


pg = st.navigation(
    [
        st.Page("streamlit_app.py", title="Home"),
        st.Page("page/credit_card_installment.py", title="Credit Card Installment"),
    ]
)
pg.run()
# st.set_page_config(
#     page_title="happybarra",
#     page_icon="🐹",
# )


# st.write(st.session_state)


# st.write(
#     f"You have selected the following card: **{bank} - {network} - {credit_card}**",
# )
# installment_type = st.radio(
#     "What installment amount do you know?", InstallmentAmountType
# )
# installment_amount = st.number_input(
#     f"{installment_type} Amount", step=500.0, format="%.2f"
# )

# statement_date = st.select_slider("Select your statement date", range(1, 32))
# due_date_ref = st.select_slider(
#     "How many days after your statement does your due date fall?", range(1, 46)
# )
# installment_tenure = st.number_input(
#     f"How many months do you have to pay for it?", step=1
# )
# date_input = st.date_input("When is the purchase?", format="YYYY-MM-DD")


# try:
#     cci = CreditCardInstallment(
#         get_credit_card((bank, network, credit_card))(
#             due_date_ref=due_date_ref, statement_day=statement_date
#         ),
#         installment_tenure,
#         date_input,
#         amount=installment_amount,
#     )
#     _logger.debug(cci)
#     cci_init = True
# except Exception as e:
#     _logger.debug("cci failed error: ", e)
#     st.write(":)")

# if cci_init:
#     charges = cci.get_charge_dates()
#     _logger.debug(charges)
#     df = pd.DataFrame(charges)
#     _logger.debug(df)
#     st.write(df)
