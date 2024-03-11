from src.pages.homepage import homepage

import streamlit as st

# ----- CONFIG -----
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# ----- CONSTS -----
PAGE_NAMES_TO_FUNCS: dict = {"homepage": homepage}

# ----- SIDEBAR SELECTBOX -----
page_selector = st.sidebar.selectbox("Select a page", PAGE_NAMES_TO_FUNCS.keys())
PAGE_NAMES_TO_FUNCS[page_selector]()
