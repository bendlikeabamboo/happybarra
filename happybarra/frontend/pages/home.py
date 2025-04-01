import streamlit as st

st.markdown("# 🐹 happybarra")
st.markdown("Do you have enough money for this?")

# for dev purposes
if st.session_state.get("happybarra_config__dev_mode", False):
    st.write(st.session_state)

