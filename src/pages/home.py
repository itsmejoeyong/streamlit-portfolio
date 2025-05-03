import streamlit as st

st.title("Welcome to My Portfolio")
st.write("""
👋 Hi there! I'm excited to share my work and journey with you.

This is my personal portfolio where I showcase my projects, skills, and experiences.
Feel free to explore and get to know more about my work!
""")

# Add a nice divider
st.divider()

# Add some key highlights
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Years of Experience", "3+")
    
with col2:
    st.metric("Projects Completed", "10+")
    
with col3:
    st.metric("Technologies", "5+") 