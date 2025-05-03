import streamlit as st

# Configure the page
st.set_page_config(
    page_title="My Portfolio",
    page_icon="🎯",
    layout="wide"
)

# Initialize session state for page navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Create the navigation header
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1>My Portfolio</h1>
</div>
""", unsafe_allow_html=True)

# Create two columns for navigation buttons
col1, col2 = st.columns(2)

# Navigation buttons with proper state management
with col1:
    home_clicked = st.button(
        "🏠 Home",
        key="home_btn",
        use_container_width=True,
        type="primary" if st.session_state.current_page == 'home' else "secondary"
    )
    if home_clicked:
        st.session_state.current_page = 'home'
        st.rerun()

with col2:
    works_clicked = st.button(
        "💼 Works",
        key="works_btn",
        use_container_width=True,
        type="primary" if st.session_state.current_page == 'works' else "secondary"
    )
    if works_clicked:
        st.session_state.current_page = 'works'
        st.rerun()

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Run the appropriate page based on session state
if st.session_state.current_page == 'home':
    with open('src/pages/home.py', 'r') as f:
        exec(f.read())
else:
    with open('src/pages/works.py', 'r') as f:
        exec(f.read())