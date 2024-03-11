from src.pages.homepage import homepage

import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

page_names_to_funcs = {"homepage": homepage}
page_selector = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[page_selector]()
