import os

import duckdb
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
    table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
    table_names_df = con.execute(table_names_query).df()
    table_names = table_names_df['table_name'].tolist()
    
    # Create dropdown
    selected_table = st.selectbox('Select a table to preview the data: ', table_names)
    
    if selected_table:
        preview_data_query = f"SELECT * FROM {selected_table} LIMIT 5;"
        df = con.execute(preview_data_query).df()
        
        st.dataframe(df)
