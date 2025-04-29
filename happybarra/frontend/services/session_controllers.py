import streamlit as st


def reset_session_state_for_page(page_key: str):
    for key in [key for key in st.session_state if key.startswith(page_key)]:
        del st.session_state[key]
