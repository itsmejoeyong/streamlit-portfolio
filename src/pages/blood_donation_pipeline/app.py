import os

from src.pages.blood_donation_pipeline.src.blood_donation_pipeline import (
    BloodDonationPipeline,
)

import duckdb
import streamlit as st


def display_blood_donation_pipeline():
    DUCKDB_DB_PATH = os.path.join(
        f"{os.getcwd()}", "duckdb", "blood_donation_pipeline_v2.duckdb"
    )
    DUCKDB_CONN = duckdb.connect(DUCKDB_DB_PATH, True)
    bdp = BloodDonationPipeline(DUCKDB_CONN)

    ########## CONFIG ##########
    # NOTE: This will be moved towards the main entrypoint
    # st.set_page_config(layout="wide")

    ########## TITLE & ABOUT ##########
    st.title("Blood donation pipeline v2")
    st.markdown("#####")
    bdp.display_about_section()
    st.divider()

    ########## METRICS ##########
    st.markdown("### Metrics")
    bdp.display_donation_metrics_by_state()
    bdp.display_donation_metrics_by_hospital()
    st.divider()

    ########## GRANULAR DATASET ANALYSIS ##########
    st.markdown("### Granular Dataset Analysis")
    bdp.display_granular_dataset_analysis()

    ########## INFO ##########
    st.info("""
    - churn definition: donor who hasn't made a donation within 2 years since last donation
    - average retention after nth year: the % of donor retention on the nth year from the 1st year (for example, only ~20% of donors in age group 20-29 from the first year made a donation in the 2nd year)
    > be patient! nearly 10 million rows on a 1 core 2 gig machine takes some time even with duckdb's columnar aggregations :)

    > the dataset being analyzed is ds_data_granular, you can open the "About the project & data" dropdown and inspect
    """)
