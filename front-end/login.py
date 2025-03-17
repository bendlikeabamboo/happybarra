import streamlit as st

if not st.session_state.get("login_attempt", False):
    st.write("👤 happybarra login")
    st.write("Email:")
    email_address = st.text_input("e-mail address")
    password = st.text_input("password", type="password")
    creds_submitted = st.button("login")
    if creds_submitted:
        st.session_state["valid_session"] = True
        st.rerun()
