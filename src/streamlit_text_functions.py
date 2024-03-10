import streamlit as st


def center_header(text: str, header_level: int = 1):
    if header_level not in range(1, 7):
        raise ValueError("Header level must be between 1 & 6")
    st.markdown(
        f"<h{header_level} style='text-align: center;'>{text}</h{header_level}>",
        unsafe_allow_html=True,
    )


def center_paragraph(text):
    st.markdown(f"<p style='text-align: center;'>{text}</p>", unsafe_allow_html=True)


def create_two_columns_with_ratio(a, ratio_a, b, ratio_b):
    col1, col2 = st.columns([ratio_a, ratio_b])
    with col1:
        st.markdown(a)
    with col2:
        st.markdown(b)
