import os

import duckdb
import pandas as pd
import streamlit as st

### Initializing DUCKDB ###
DUCKDB_DB = os.path.join("duckdb", "blood_donation_pipeline_v2.duckdb")
con = duckdb.connect(database=DUCKDB_DB, read_only=True)

### Initializing streamlit ###
st.set_page_config(layout="wide")
st.title('Blood donation pipeline v2')

EXPANDER_TEXT = """
The second version of our Blood Donation Pipeline, a major refactor, code & tech wise, that led to a new repository. 

The data is regarding blood donations that's made available through Ministry of Health (MOH).
"""
with st.expander("About the project & data"):
    st.write(EXPANDER_TEXT)
    
    "---"
    
    st.subheader("Preview the data")
    # Query db information schema to get table list
    TABLE_NAMES_QUERY = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
    table_names_df = con.execute(TABLE_NAMES_QUERY).df()
    table_names = table_names_df['table_name'].tolist()
    
    # Create dropdown
    SELECT_TEXT = "Select a table to preview the data: "
    selected_table = st.selectbox(SELECT_TEXT, table_names)
    
    if selected_table:
        PREVIEW_DATA_QUERY = f"SELECT * FROM {selected_table} LIMIT 5;"
        df = con.execute(PREVIEW_DATA_QUERY).df()
        
        st.dataframe(df)


st.subheader("Charts")
DONATIONS_STATE_QUERY = """
SELECT
    date,
    state,
    blood_a,
    blood_b,
    blood_o,
    blood_ab,
    social_civilian,
    social_student,
    social_policearmy,
    donations_new,
    donations_regular,
    donations_irregular
FROM donations_state
"""

DONATIONS_FACILITY_DF = con.execute(DONATIONS_STATE_QUERY).df()
monthly_aggregate_df = DONATIONS_FACILITY_DF.groupby(['state', pd.Grouper(key='date', freq='Y')]).agg({
    'blood_a': 'sum',
    'blood_b': 'sum',
    'blood_o': 'sum',
    'blood_ab': 'sum',
    'social_civilian': 'sum',
    'social_student': 'sum',
    'social_policearmy': 'sum',
    'donations_new': 'sum',
    'donations_regular': 'sum',
    'donations_irregular': 'sum'
}).reset_index()
monthly_aggregate_df['year_month'] = monthly_aggregate_df['date'].dt.strftime('%Y')

# getting state list
hospital_list = monthly_aggregate_df['state'].unique().tolist()
SELECTED_STATE_TEXT = "Select a state: "
selected_hospital = st.selectbox(SELECTED_STATE_TEXT, hospital_list, index=3)

# getting date range
min_date = monthly_aggregate_df['date'].min()
max_date = monthly_aggregate_df['date'].max()
SELECTED_DATE_RANGE_TEXT = "Select date range: "
selected_date_range = st.date_input(SELECTED_DATE_RANGE_TEXT, value=(min_date, max_date))

# Filtering dataframe based on selection above
filtered_df = monthly_aggregate_df[
    (monthly_aggregate_df['state'] == selected_hospital) &
    (monthly_aggregate_df['date'] >= pd.to_datetime(selected_date_range[0])) &
    (monthly_aggregate_df['date'] <= pd.to_datetime(selected_date_range[1]))
]

# set index to 'date' for better plotting
filtered_df.set_index('date', inplace=True)
blood_type_col = ['blood_a', 'blood_b', 'blood_o', 'blood_ab']
social_type_col = ['social_civilian', 'social_student', 'social_policearmy']
donation_type_col = ['donations_new', 'donations_regular', 'donations_irregular']
df_blood_type = filtered_df[blood_type_col]
df_social_type = filtered_df[social_type_col]
df_donation_frequency = filtered_df[donation_type_col]

# put chart into columns
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Donations by blood type")
    st.line_chart(df_blood_type)

with col2:
    st.write("Donations by social type")
    st.line_chart(df_social_type)

with col3:
    st.write("Donations by donation frequency")
    st.line_chart(df_donation_frequency)