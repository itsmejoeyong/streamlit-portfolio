from src.streamlit_text_functions import (
    center_header,
    center_paragraph,
    create_two_columns_with_ratio,
)

import streamlit as st

# ----- CONSTANTS -----
PAGE_TITLE: str = "DIGITAL Portfolio | Joe Yong"
NAME: str = "Joe Yong"
DESCRIPTION: str = """
Data Engineer in Pandai, an Edtech startup helping students getting better grades in Malaysia!
"""
SOCIAL_MEDIA: dict = {
    "LinkedIn": "https://www.linkedin.com/in/itsmejoeyong/",
    "GitHub": "https://github.com/itsmejoeyong",
}
MARKDOWN_LINKEDIN_LINK: str = f"[LinkedIn]({SOCIAL_MEDIA["LinkedIn"]})"
MARKDOWN_GITHUB_LINK: str = f"[GitHub]({SOCIAL_MEDIA["GitHub"]})"
EMAIL: str = "joeanselmyz@gmail.com"
HTML_EMAIL_LINK: str = f'<a href="mailto:{EMAIL}">Email</a>'
PHONE_NO: int = 60182307282
WHATSAPP_LINK: str = f"[Whatsapp](https://web.whatsapp.com/send?phone={PHONE_NO})"
COMPANIES: dict = {
    "pandai": [
        {
            "name": "Pandai Education Sdn Bhd",
            "latest title": [
                {
                    "name": "data engineer",
                    "tenure": "2023 Oct - Present",
                }
            ],
            "second latest title": [
                {
                    "name": "data analyst",
                    "tenure": "2022 Oct - 2023 Oct",
                }
            ],
        }
    ]
}


def homepage():
    # ----- HEADER & BIO -----

    center_header("Joe Yong")
    center_paragraph(DESCRIPTION)
    st.info("""
    I keep my meetings, presentations, summaries, a̵n̵d̵ ̵m̵y̵ ̵w̵o̵r̵k̵ ̵h̵o̵u̵r̵s̵ short.

    I left my first job after a week, I don't have a degree, SPM results kinda sucked, and made many mistakes along the way, 
    but that didn't stop me from becoming a Barista, a Cafe Manager, a Data Analyst, & recently a Data Engineer!

    Currently in a startup, i wear many many hats; 
    used to do a little community management, data work here and there, managing & training data interns, 
    some infrastructure, dev ops, non data/coding project management (isms iso engineering representative) etc.

    am currently interested in the software-engineering aspects & methodologies (SOLID),
    trying to implement what I'm learning into my data products (basically my code) & projects!

    Curious as to what I do? Head on down to my work experience! 
    It's slightly more detailed if you're curious about the nitty-gritty!
    """)

    st.write("######")

    # ----- CONTACTS -----
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write(MARKDOWN_LINKEDIN_LINK)

    with col2:
        st.write(MARKDOWN_GITHUB_LINK)

    with col3:
        st.markdown(HTML_EMAIL_LINK, unsafe_allow_html=True)

    with col4:
        st.markdown(WHATSAPP_LINK)

    st.divider()

    # ----- WORK EXPERIENCE -----
    create_two_columns_with_ratio(f"### {COMPANIES['pandai'][0]['name']}", 80, "", 20)
    create_two_columns_with_ratio(
        f"##### {COMPANIES['pandai'][0]['latest title'][0]['name']}",
        80,
        f"{COMPANIES['pandai'][0]['latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Constructured ETL pipeline using Azure services, leveraging AI technology to boost workflow speed and efficiency, resulting in processing over 500% more documents.
    - Engineered ETL pipeline using GPT for document classification, improving process &reducing manual intervention, saving 100’s of hours a week of manual reviewing.
    - Crafted Batch ETL pipeline (GUI + code) for event-based/clickstream data using AWS services, enhancing data frequency from weekly to daily intervals.
    - Developed Idempotent Pipelines to extract & load data from PostgreSQL to MySQL (& vice-versa) for downstream analysis & or feature development.
    - Established Airflow instance with Docker, orchestrating dozens of DAGS, unifying most data-related development into a single repository.
    - Enforced ISMS ISO 27001:2022 practices across engineering teams, managing engineering-related ISMS documents, and ensuring compliance.
    """)
    create_two_columns_with_ratio(
        f"##### {COMPANIES['pandai'][0]['second latest title'][0]['name']}",
        80,
        f"{COMPANIES['pandai'][0]['second latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Optimized queries, data models & applied strategic indexes on main application, saving RM 100,000 anually in database operational costs & reducing query times from hours to seconds.
    - Improved internal data cleansing processes & improved efficiency by more than 500%, allowing respective departments to set higher goals.
    - Set up automated self-service dashboards & reports on LookerStudio & Redash, internally & with business partners, significantly reducing the amount of ad-hoc querying & reporting.
    - Implemented & captured Type 2 Slowly Changing Dimensions data warehousing practices in analytics database to analyze historical data accurately.
    - Handled Migration of BI services on linux virtual machines, databases & data migration from MariaDB to MySQL during migration project.
    """)

    st.divider()

    # ----- Projects -----
    st.markdown("### Projects")
    st.info("""
    Expand the sidebar on the top left and select the projects you want to view!
    """)
