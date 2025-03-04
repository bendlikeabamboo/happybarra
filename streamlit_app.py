import streamlit as st

st.write("# 🐹 happybarra")

KNOWN_BANKS = ("Unionbank", "Metrobank", "BPI", "Eastwest", "Security Bank")
CARD_TYPES = {
    "Unionbank": ["PlayEveryday", "Rewards Platinum"],
    "Metrobank": ["Visa Peso Platinum", "Visa Titanium"],
    "BPI": ["Visa Amore Cashback", "Mastercard Gold"],
    "Eastwest": ["Visa Platinum"],
    "Security Bank": ["Visa Travel Platinum"]
}


with st.form("bank"):
    st.write("Choose bank")
    bank = st.selectbox("Bank", KNOWN_BANKS)
    # Every form must have a submit button.
    bank_submitted = st.form_submit_button("Submit")

if bank_submitted:
    with st.form("card"):
        st.write("Choose credit card")
        card_type = st.selectbox("Card Type", CARD_TYPES[bank])
        card_type_submitted = st.form_submit_button("Submit")

if card_type_submitted:
    st.write("You have selected the following card:", card_type)

st.write("End application")
