import streamlit as st
import pandas as pd

from happybarra.frontend.services.helpers import get_dues_schedules

st.set_page_config(page_title="happybarra", page_icon="🐹", layout="centered")
st.write("# ⚓ Manage Dues")

PAGE_KEY = "MANAGE_DUES"
PK_LANDING = f"{PAGE_KEY}__LANDING"
PK_CHOOSE_OPERATION = f"{PAGE_KEY}__CHOOSE_OPERATION"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"
PK_ = f"{PAGE_KEY}__"


VK_DUE_TO_MODIFY = f"{PAGE_KEY}__DUE_TO_MODIFY"
VK_ = f"{PAGE_KEY}__"
VK_ = f"{PAGE_KEY}__"
VK_ = f"{PAGE_KEY}__"
VK_ = f"{PAGE_KEY}__"

WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"
WK = f"{PAGE_KEY}__"


if PAGE_KEY not in st.session_state:
    st.session_state[PAGE_KEY] = PK_LANDING


if st.session_state[PAGE_KEY] == PK_LANDING:
    dues_light = get_dues_schedules()[
        [
            "financial_commitment__name",
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
    }
    st.dataframe(
        dues_light.rename(renamer, axis=1)[["name", "source"]], hide_index=True
    )

    card_to_modify = st.selectbox(
        label="Select due to modify or delete",
        options=dues_light.index,
    )
    submit_card_to_modify = st.button(label="Submit")
    if submit_card_to_modify:
        st.session_state[PAGE_KEY] = PK_CHOOSE_OPERATION
        st.session_state[VK_DUE_TO_MODIFY] = dues_index[card_to_modify]
        st.rerun()

if st.session_state[PAGE_KEY] == PK_CHOOSE_OPERATION:
    label = (
        "Choose what you want to do to "
        f"___{st.session_state.get(VK_DUE_TO_MODIFY)['financial_commitment__name']}___"
    )
    operations = ["Delete due"]
    st.selectbox(label=label, options=operations)
