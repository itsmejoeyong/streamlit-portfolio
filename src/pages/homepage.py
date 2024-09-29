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
Data Engineer at Borong, a leading platform empowering businesses with efficient digital wholesale solutions in Malaysia!
"""
CATCH_PHRASE: str = "I don't just build pipelines, I build value!"
SOCIAL_MEDIA: dict = {
    "LinkedIn": "https://www.linkedin.com/in/itsmejoeyong/",
    "GitHub": "https://github.com/itsmejoeyong",
}
COMPANY_WEBSITES: dict = {
    "pandai": "https://my.pandai.org/",
    "borong": "https://www.borong.com/my",
    "rinse": "https://www.instagram.com/rinse_kl/",
}
MARKDOWN_LINKEDIN_LINK: str = f"[LinkedIn]({SOCIAL_MEDIA["LinkedIn"]})"
MARKDOWN_GITHUB_LINK: str = f"[GitHub]({SOCIAL_MEDIA["GitHub"]})"
EMAIL: str = "joeanselmyz@gmail.com"
HTML_EMAIL_LINK: str = f'<a href="mailto:{EMAIL}">Email</a>'
PHONE_NO: int = 60182307282
WHATSAPP_LINK: str = f"[Whatsapp](https://web.whatsapp.com/send?phone={PHONE_NO})"
COMPANIES: dict = {
    "borong": [
        {
            "name": "Borong",
            "latest title": [{"name": "Data Engineer", "tenure": "2024 Oct - Present"}],
        }
    ],
    "pandai": [
        {
            "name": "Pandai Education Sdn Bhd",
            "part time title": [
                {"name": "Data Engineer (part time)", "tenure": "2024 Sept - Present"}
            ],
            "latest title": [
                {
                    "name": "Data Engineer",
                    "tenure": "2023 Oct - 2024 Sept",
                }
            ],
            "second latest title": [
                {
                    "name": "Data Analyst",
                    "tenure": "2022 Oct - 2023 Oct",
                }
            ],
        }
    ],
    "rinse": [
        {
            "name": "Rinse KL",
            "latest title": [
                {"name": "Barista cum Cafe Manger", "tenure": "After SPM - 2022 Mar"}
            ],
        }
    ],
}


def homepage():
    # ----- HEADER & BIO -----

    center_header("Joe Yong")
    center_paragraph(DESCRIPTION)
    center_paragraph(CATCH_PHRASE)
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
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.write("")

    with col2:
        st.write(MARKDOWN_LINKEDIN_LINK)

    with col3:
        st.markdown(MARKDOWN_GITHUB_LINK)

    with col4:
        st.markdown(HTML_EMAIL_LINK, unsafe_allow_html=True)

    with col5:
        st.markdown(WHATSAPP_LINK)

    with col6:
        st.markdown("")

    st.divider()

    # ----- WORK EXPERIENCE -----
    create_two_columns_with_ratio(
        f"### [{COMPANIES['borong'][0]['name']}]({COMPANY_WEBSITES['borong']})",
        80,
        f"",
        20,
    )
    create_two_columns_with_ratio(
        f"##### {COMPANIES['borong'][0]['latest title'][0]['name']}",
        80,
        f"{COMPANIES['borong'][0]['latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Yet to document!
    """)
    st.title("")

    create_two_columns_with_ratio(
        f"### [{COMPANIES['pandai'][0]['name']}]({COMPANY_WEBSITES['pandai']})",
        80,
        "",
        20,
    )
    create_two_columns_with_ratio(
        f"##### {COMPANIES['pandai'][0]['part time title'][0]['name']}",
        80,
        f"{COMPANIES['pandai'][0]['part time title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Revamped ELT pipeline, replacing Azure Data Factory w Databricks & Airflow, reducing operational costs by 90%
    - Initiated machine learning pipeline integration with production app to predict high-potential subscribers with the Product & B2C teams.
    - Established playbooks, documentation, architectual, network & logic diagrams for Data Team & administrative &/ diagnostics operations.
    """)
    st.title("")

    create_two_columns_with_ratio(
        f"##### {COMPANIES['pandai'][0]['latest title'][0]['name']}",
        80,
        f"{COMPANIES['pandai'][0]['latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Developed pipelines to support AI department’s LLM development using OpenAI models, LangChain, PgVector & AzureAI.
    - Developed, modeled, optimized database & assisted in feature development for LLM application, resulting in 50% reduced costs & 100% increase in throughput/performance.
    - Replaced former ELT Analytics Pipeline with BigQuery, Azure Data Factory & BQ Transfer Jobs, improving analysis speeds by more than 1000% & reducing processing time by 60%.
    - Revamped Analytics & Dashboarding using BigQuery, DBT & LookerStudio improving workflow efficiency by more than 100%.
    - Constructed ETL pipeline using Azure Form Recognizer to boost workflow speed and efficiency, resulting in processing over 500% more documents.
    - Engineered ETL pipeline using GPT for document classification & labeling, reducing manual intervention, and saving 100’s of hours a week.
    - Established Airflow instance with Docker, orchestrating dozens of DAGS, unifying most data-related development into a single repository.
    - Replaced Segment with self-hosted Rudderstack deployment for CDP analytics, reducing costs by 75%.
    - Crafted Batch ETL pipeline (GUI + code) for event-based/clickstream data using AWS services, enhancing data frequency from weekly to daily intervals.
    - Engineering Team Representative for ISMS ISO 27001:2022 certification, managing engineering-related ISMS documents, and ensuring compliance.
    - Deployed self-hosted Wireguard VPN server to comply with ISO 27001:2022 standard, resulting in 75% cost reduction compared to PaaS VPN.
    """)
    st.title("")

    create_two_columns_with_ratio(
        f"##### {COMPANIES['pandai'][0]['second latest title'][0]['name']}",
        80,
        f"{COMPANIES['pandai'][0]['second latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - 75% reduction in database operational costs & reduced query times from hours to seconds by optimizing queries & applying strategic indexes.
    - 500% increased efficiency in improved data cleansing processes allowing respective departments to set higher goals.
    - Implemented & captured Type 2 Slowly Changing Dimensions data warehousing practices in analytics database to analyze historical data accurately.
    - Handled Migration of BI services on linux virtual machines, databases & data migration from MariaDB to MySQL during migration project.
    - Reduced Production MariaDB & MySQL server load by 60% (100% peak load > 40% peak load) which addressed web app freezing issues & saving RM 60,000 annually on DB upgrades annually.
    - Set up automated self-service dashboards/reports on LookerStudio which allowed us to take on multiple projects with business partners with less ad-hoc querying/reporting, saving dozens of hours a week.
    - Improved Analytics DB performance which sped up reporting & query operations from 2 hours down to seconds/minutes.
    - Established & managing data mart practices in analytics database for easier data governance, observability & troubleshooting, made up of over 50 components (stored procedures & events).
    - PIC for infrastructure migration project w/ business partner from AWS to Azure, handling migration of BI service on linux VM, Database & data migration from MariaDB to MySQL, management of Terraform script.
    - Increased reporting speeds from weekly to daily updates for clickstream data by implementing an ETL pipeline (GUI + code) using AWS services to pull data & load it into our analytics database.
    - Set up Database replication on AWS & automatic DB replication error logging & skipping ensuring 100% replica uptime
    """)
    # create some space
    st.title("")
    create_two_columns_with_ratio(
        f"### [{COMPANIES['rinse'][0]['name']}]({COMPANY_WEBSITES['rinse']})",
        80,
        "",
        20,
    )
    create_two_columns_with_ratio(
        f"##### {COMPANIES['rinse'][0]['latest title'][0]['name']}",
        80,
        f"{COMPANIES['rinse'][0]['latest title'][0]['tenure']}",
        20,
    )
    st.markdown("""
    - Managed FOH/BOH (Front/Back of House) resources (staff timetables, stocks, audit, opening/closing etc.)
    - Prepared, personalized & supervised team onboarding & training SOP's for junior & Senior Service Crews, Baristas & Shift Managers.
    - Calibrated & QC'd hand brew & espresso based beverages.
    - Managed over half a dozen brands & platforms for delivery services, handling well over 100's of orders per day.
    - Created social media content (pictures & copywriting) for company's Instagram.
    """)

    st.divider()

    # ----- Skills -----
    create_two_columns_with_ratio(
        "### Production Skills",
        80,
        "",
        20,
    )
    st.markdown("""
    - Development & deployment experience with AWS, Azure & GCP.
    - Production experience with SQL, Bigquery, DBT, Python, Airflow, Data Pipelines, Query & Database Optimizations, Data Modeling & OpenAI models/LLM’s.
    - Fluent in English, able to converse in Malay informally.
    """)

    st.divider()

    # ----- Projects -----
    st.markdown("### Projects")
    st.info("""
    Expand the sidebar on the top left and select the projects you want to view!
    Or head to my github page :)
    """)

    st.divider()

    # ----- Certifications -----
    create_two_columns_with_ratio(
        "### Certifications",
        80,
        "",
        20,
    )

    create_two_columns_with_ratio(
        "- [DBT Fundamentals](itsmejoeyong.com)",
        80,
        "2024-04 - 2026-04",
        20,
    )

    create_two_columns_with_ratio(
        "- [AWS Certified Solutions Architect – Associate](https://www.credly.com/badges/c101ada5-369e-486a-8fc6-6444411726ce)",
        80,
        "2023-06 - 2026-06",
        20,
    )

    create_two_columns_with_ratio(
        "- [Datacamp Data Engineer](https://www.datacamp.com/completed/statement-of-accomplishment/track/7073af6f1dd3fb64befc5cae4d6ac8757e3eab9c)",
        80,
        "2023-02 ~",
        20,
    )

    create_two_columns_with_ratio(
        "- [Google Data Analytics](https://www.coursera.org/account/accomplishments/specialization/certificate/AZ2P6LM2RWA5)",
        80,
        "2022-05 ~",
        20,
    )
