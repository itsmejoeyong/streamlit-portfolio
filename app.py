from src.pages.homepage import homepage

import streamlit as st

# ----- CONFIG -----
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ----- CONSTS -----
PAGE_NAMES_TO_FUNCS: dict = {"Homepage": homepage}
GITHUB_REPOS = {
    "Homepage": "https://github.com/itsmejoeyong/streamlit-portfolio/tree/homepage"
}

# ----- SIDEBAR SELECTBOX -----
page_selected = st.sidebar.selectbox("Select a page", PAGE_NAMES_TO_FUNCS.keys())
st.sidebar.divider()
PAGE_NAMES_TO_FUNCS[page_selected]()
st.sidebar.markdown(f"""
Github Repo for {page_selected}:
[here]({GITHUB_REPOS.get(page_selected)})
""")
