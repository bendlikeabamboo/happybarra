from typing import Tuple

import streamlit as st

__all__ = ["submit_button", "submit_and_go_back_buttons", "go_back_button"]


def submit_button():
    _, right = st.columns([5.5, 1])
    with right:
        button = st.button("Submit ➡️")
    return button


def form_submit_button():
    _, right = st.columns([5.0, 1])
    with right:
        button = st.form_submit_button("Submit ➡️")
    return button


def form_submit_and_go_back_buttons():
    left, right = st.columns([5.0, 1])
    with left:
        go_back = st.form_submit_button("⬅️ Go back", type="tertiary")
    with right:
        submit = st.form_submit_button("Submit ➡️")
    return submit, go_back


def submit_and_go_back_buttons() -> Tuple[bool, bool]:
    col1, col2 = st.columns([5.5, 1])
    with col1:
        go_back = st.button("⬅️ Go back", type="tertiary")
    with col2:
        submit = st.button("Submit ➡️", type="secondary")
    return submit, go_back


def go_back_button():
    go_back = st.button("⬅️ Go back", type="tertiary")
    return go_back
