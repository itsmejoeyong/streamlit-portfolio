from src.pages.blood_donation_pipeline.app import display_blood_donation_pipeline

import streamlit as st

##### CONFIG #####
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

##### CONSTS #####
PAGE_NAMES_TO_FUNCS: dict = {"Blood Donation Pipeline": display_blood_donation_pipeline}
GITHUB_REPOS = {
    "Blood Donation Pipeline": {
        "repository": "https://github.com/itsmejoeyong/blood-donation-pipeline-v2",
        "branch": "https://github.com/itsmejoeyong/streamlit-portfolio/tree/blood-donation-pipeline-v2",
    },
}

##### SIDEBAR SELECTBOX #####
page_selected = st.sidebar.selectbox("Select a page", PAGE_NAMES_TO_FUNCS.keys())
st.sidebar.divider()
st.sidebar.markdown(f"""
{page_selected}:

- [dedicated repository]({GITHUB_REPOS[page_selected]['repository']})

- [main application branch]({GITHUB_REPOS[page_selected]['branch']})
""")
##### MAIN PAGE #####
PAGE_NAMES_TO_FUNCS[page_selected]()
