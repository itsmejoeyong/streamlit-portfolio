import streamlit as st

st.title("My Works")
st.write("Here are some of my notable projects and contributions:")

# Example project cards
def create_project_card(title, description, technologies, link=None):
    with st.container():
        st.subheader(title)
        st.write(description)
        st.write("**Technologies:** " + ", ".join(technologies))
        if link:
            st.markdown(f"[View Project]({link})")
        st.divider()

# Project 1
create_project_card(
    "Project 1",
    "A web application that helps users manage their daily tasks efficiently.",
    ["Python", "Streamlit", "SQLite"],
    "https://github.com/yourusername/project1"
)

# Project 2
create_project_card(
    "Project 2",
    "A data analysis tool for visualizing and understanding complex datasets.",
    ["Python", "Pandas", "Plotly"],
    "https://github.com/yourusername/project2"
)

# Project 3
create_project_card(
    "Project 3",
    "An API service for handling user authentication and authorization.",
    ["Python", "FastAPI", "JWT"],
    "https://github.com/yourusername/project3"
) 