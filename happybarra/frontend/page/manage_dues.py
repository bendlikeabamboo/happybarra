from types import SimpleNamespace

import pandas as pd
import streamlit as st

from happybarra.frontend.services import (
    CONFIG_USE_MOCKS_HOOK,
    delete_due,
    get_dues_schedules,
    submit_and_go_back_buttons,
    submit_button,
)

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")
st.write("# ⚓ Manage Dues")
st.write("Stay on top! ☝️")
st.markdown("---")

PAGE_KEY = "MANAGE_DUES"
PK_LANDING = f"{PAGE_KEY}__LANDING"
PK_CHOOSE_OPERATION = f"{PAGE_KEY}__CHOOSE_OPERATION"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"


VK_DUE_TO_MODIFY = f"{PAGE_KEY}__DUE_TO_MODIFY"
VK_DELETE_OPERATION_SUCCESS = f"{PAGE_KEY}__DELETE_OPERATION_SUCCESS"
VK_DELETE_OPERATION_FAILED = f"{PAGE_KEY}__DELETE_OPERATION_FAILED"
VK_ = f"{PAGE_KEY}__"
VK_ = f"{PAGE_KEY}__"

WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"

if st.session_state.get(VK_DELETE_OPERATION_SUCCESS, False):
    st.success("Deletiong success 🎉")
    st.session_state[VK_DELETE_OPERATION_SUCCESS] = False

if st.session_state.get(VK_DELETE_OPERATION_FAILED, False):
    st.success("Deletiong failed 😖. Try again.")
    st.session_state[VK_DELETE_OPERATION_FAILED] = False

if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING


if st.session_state[PAGE_KEY] == PK_LANDING:
    dues_light = get_dues_schedules()[
        [
            "financial_commitment__name",
            "source_type",
            "financial_commitment__source_name_extended",
            "financial_commitment__id",
        ]
    ].drop_duplicates()
    dues_light["choices"] = (
        dues_light["financial_commitment__name"]
        + " — "
        + dues_light["financial_commitment__source_name_extended"]
    )
    dues_light = dues_light.set_index("choices", inplace=False)
    dues_index = dues_light.to_dict("index")

    # column renamer so the dataframe looks user friendly
    renamer = {
        "financial_commitment__source_name_extended": "source",
        "financial_commitment__name": "name",
        "source_type": "source_type",
    }
    st.markdown("### Registered Dues")
    st.dataframe(
        dues_light.rename(renamer, axis=1)[["name", "source", "source_type"]],
        hide_index=True,
        use_container_width=True,
        selection_mode="single-row",
    )

    card_to_modify = st.selectbox(
        label="Select due to view, modify, or delete",
        options=dues_light.index,
        help="Something",
    )
    submit = submit_button()
    if submit:
        st.session_state[PAGE_KEY] = PK_CHOOSE_OPERATION
        st.session_state[VK_DUE_TO_MODIFY] = dues_index[card_to_modify]
        st.rerun()

if st.session_state[PAGE_KEY] == PK_CHOOSE_OPERATION:
    st.markdown(
        "##### Details for 📝 "
        f"___{st.session_state.get(VK_DUE_TO_MODIFY)['financial_commitment__name']}___"
    )
    dues: pd.DataFrame = get_dues_schedules()
    due_filter = (
        dues["financial_commitment__id"]
        == st.session_state.get(VK_DUE_TO_MODIFY)["financial_commitment__id"]
    )
    user_friendly_columns = {
        "financial_commitment__name": "name",
        "financial_commitment__source_name_extended": "source",
        "amount": "amount",
        "bill_date": "bill_date",
        "statement_date": "statement_date",
        "due_date": "due_date",
        "source_type": "source_type",
    }

    st.dataframe(
        dues.loc[due_filter, user_friendly_columns.keys()].rename(
            user_friendly_columns, axis=1
        ),
        hide_index=True,
    )
    label = (
        "Choose what you want to do to "
        f"___{st.session_state.get(VK_DUE_TO_MODIFY)['financial_commitment__name']}___"
    )
    operations = ["Delete due"]
    operation = st.selectbox(label=label, options=operations)

    submit, go_back = submit_and_go_back_buttons()

    if go_back:
        st.session_state[PAGE_KEY] = PK_LANDING
        st.rerun()
    if submit:
        with st.spinner(text="Deleting due...", show_time=True):
            if st.session_state[CONFIG_USE_MOCKS_HOOK]:
                from time import sleep

                sleep(2)
                response = SimpleNamespace(ok=True)
            else:
                response = delete_due(
                    st.session_state.get(VK_DUE_TO_MODIFY)["financial_commitment__id"]
                )
            if response.ok:
                st.session_state[VK_DELETE_OPERATION_SUCCESS] = True
                st.session_state[PAGE_KEY] = PK_LANDING
                get_dues_schedules.clear()
                st.rerun()

            else:
                st.session_state[VK_DELETE_OPERATION_FAILED] = True
                st.session_state[PAGE_KEY] = PK_LANDING
                st.rerun()
