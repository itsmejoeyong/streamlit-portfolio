import os

import duckdb
import pandas as pd
import streamlit as st

########## Initializing DUCKDB ##########
DUCKDB_DB = os.path.join("duckdb", "blood_donation_pipeline_v2.duckdb")
con = duckdb.connect(database=DUCKDB_DB, read_only=True)

########## DROPDOWN LOGIC ##########
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

########## METRICS BY STATE ##########
st.markdown("### Metrics")
with st.expander("__Donation Metrics By State__"):
    DONATIONS_STATE_QUERY = """
    SELECT
        date,
        state,
        daily,
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

    # NOTE: DONATIONS_STATE_DF shorthand is: dons_st_df
    DONATIONS_STATE_DF = con.execute(DONATIONS_STATE_QUERY).df()
    dons_st_df_aggregate = DONATIONS_STATE_DF.groupby(['state', pd.Grouper(key='date', freq='YE')]).agg({
        'daily': 'sum',
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

    # getting state list
    state_list = dons_st_df_aggregate['state'].unique().tolist()
    SELECTED_STATE_TEXT = "Select a state: "
    selected_state = st.selectbox(SELECTED_STATE_TEXT, state_list, index=3)

    # getting date range
    min_date = dons_st_df_aggregate['date'].min().to_pydatetime()
    max_date = dons_st_df_aggregate['date'].max().to_pydatetime()
    (slider_min, slider_max) = st.slider(
        "Date Range",
        min_value = min_date,
        max_value = max_date,
        value = (min_date, max_date),
        format = "YYYY/MM",
        key = "state date slider"
    )

    # Filtering dataframe based on selection above
    filtered_dons_st_df = dons_st_df_aggregate[
        (dons_st_df_aggregate['state'] == selected_state) &
        (dons_st_df_aggregate['date'] >= slider_min) &
        (dons_st_df_aggregate['date'] <= slider_max)
    ]

    # set index to 'date' for better plotting
    filtered_dons_st_df.set_index('date', inplace=True)
    daily_type_col = ['daily']
    blood_type_col = ['blood_a', 'blood_b', 'blood_o', 'blood_ab']
    social_type_col = ['social_civilian', 'social_student', 'social_policearmy']
    donation_type_col = ['donations_new', 'donations_regular', 'donations_irregular']
    df_daily = filtered_dons_st_df[daily_type_col]
    df_blood_type = filtered_dons_st_df[blood_type_col]
    df_social_type = filtered_dons_st_df[social_type_col]
    df_donation_frequency = filtered_dons_st_df[donation_type_col]

    st.write('Total Blood Donations')
    st.area_chart(df_daily, color=(244, 67, 54, 0.7))
    
    "---"
    
    # put chart into columns
    col_line_chart_1, col_line_chart_2, col_line_chart_3 = st.columns(3)
    
    with col_line_chart_1:
        st.write("Donations by blood type")
        st.line_chart(df_blood_type)

    with col_line_chart_2:
        st.write("Donations by social type")
        st.line_chart(df_social_type)

    with col_line_chart_3:
        st.write("Donations by frequency")
        st.line_chart(df_donation_frequency)
    
    "---"
    
    st.markdown("### New Donor Metrics")
    
    NEW_DONORS_STATE_QUERY = """
    SELECT
        *
    FROM newdonors_state;
    """
    
    # NOTE: NEW_DONORS_STATE_DF shorthand is: n_donors_st_df
    NEW_DONORS_STATE_DF = con.execute(NEW_DONORS_STATE_QUERY).df()
    filtered_n_donors_st_df = NEW_DONORS_STATE_DF[
        (NEW_DONORS_STATE_DF['state'] == selected_state) &
        (NEW_DONORS_STATE_DF['date'] >= slider_min) &
        (NEW_DONORS_STATE_DF['date'] <= slider_max)
    ]
    n_donors_st_df = filtered_n_donors_st_df.groupby(['state', pd.Grouper(key='date', freq='YE')]).agg({
        '17-24': 'sum',
        '25-29': 'sum',
        '30-34': 'sum',
        '40-44': 'sum',
        '45-49': 'sum',
        '50-54': 'sum',
        '55-59': 'sum',
        '60-64': 'sum'
    }).reset_index().set_index('date')
    n_donors_st_df_cols = ['17-24','25-29','30-34','40-44','45-49','50-54','55-59','60-64']
    selected_age_groups = st.multiselect(
        'Select age groups: ', 
        n_donors_st_df_cols, 
        default=n_donors_st_df_cols,
        key = 'state multiselect'
    )
    if selected_age_groups:
        n_donors_st_df = n_donors_st_df[selected_age_groups]
        st.write('New Donors By Age Group')
        st.bar_chart(n_donors_st_df)
    else:
        st.write('*Please select at least one age group to render the chart*')
    
    st.markdown("> For some reason in streamlit there's an issue with year groupings as you can see, therefore the buckets we see should be 1 year less")

######### METRICS BY HOSPITALS ##########
with st.expander("__Donation Metrics By Hospital__"):
    DONATIONS_HOSPITAL_QUERY = """
    SELECT
        date,
        hospital,
        daily,
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
    FROM donations_facility
    """

    # NOTE: DONATIONS_HOSPITAL_DF shorthand is: dons_st_df
    DONATIONS_HOSPITAL_DF = con.execute(DONATIONS_HOSPITAL_QUERY).df()
    dons_st_df_aggregate = DONATIONS_HOSPITAL_DF.groupby(['hospital', pd.Grouper(key='date', freq='YE')]).agg({
        'daily': 'sum',
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

    # getting hospital list
    hospital_list = dons_st_df_aggregate['hospital'].unique().tolist()
    SELECTED_HOSPITAL_TEXT = "Select a hospital: "
    selected_hospital = st.selectbox(SELECTED_HOSPITAL_TEXT, hospital_list, index=21)

    # getting date range
    min_date = dons_st_df_aggregate['date'].min().to_pydatetime()
    max_date = dons_st_df_aggregate['date'].max().to_pydatetime()
    (slider_min, slider_max) = st.slider(
        "Date Range",
        min_value = min_date,
        max_value = max_date,
        value = (min_date, max_date),
        format = "YYYY/MM",
        key = 'hospital date slider'
    )

    # Filtering dataframe based on selection above
    filtered_dons_st_df = dons_st_df_aggregate[
        (dons_st_df_aggregate['hospital'] == selected_hospital) &
        (dons_st_df_aggregate['date'] >= slider_min) &
        (dons_st_df_aggregate['date'] <= slider_max)
    ]

    # set index to 'date' for better plotting
    filtered_dons_st_df.set_index('date', inplace=True)
    daily_type_col = ['daily']
    blood_type_col = ['blood_a', 'blood_b', 'blood_o', 'blood_ab']
    social_type_col = ['social_civilian', 'social_student', 'social_policearmy']
    donation_type_col = ['donations_new', 'donations_regular', 'donations_irregular']
    df_daily = filtered_dons_st_df[daily_type_col]
    df_blood_type = filtered_dons_st_df[blood_type_col]
    df_social_type = filtered_dons_st_df[social_type_col]
    df_donation_frequency = filtered_dons_st_df[donation_type_col]
    
    st.write('Total Blood Donations')
    st.area_chart(df_daily, color=(244, 67, 54, 0.7))
    
    "---"

    # put chart into columns
    col_line_chart_1, col_line_chart_2, col_line_chart_3 = st.columns(3)

    with col_line_chart_1:
        st.write("Donations by blood type")
        st.line_chart(df_blood_type)

    with col_line_chart_2:
        st.write("Donations by social type")
        st.line_chart(df_social_type)

    with col_line_chart_3:
        st.write("Donations by frequency")
        st.line_chart(df_donation_frequency)
    
    st.markdown("### New Donor Metrics")
    
    NEW_DONORS_HOSPITAL_QUERY = """
    SELECT
        *
    FROM newdonors_facility;
    """
    
    # NOTE: NEW_DONORS_HOSPITAL_DF shorthand is: n_donors_st_df
    NEW_DONORS_HOSPITAL_DF = con.execute(NEW_DONORS_HOSPITAL_QUERY).df()
    filtered_n_donors_st_df = NEW_DONORS_HOSPITAL_DF[
        (NEW_DONORS_HOSPITAL_DF['hospital'] == selected_hospital) &
        (NEW_DONORS_HOSPITAL_DF['date'] >= slider_min) &
        (NEW_DONORS_HOSPITAL_DF['date'] <= slider_max)
    ]
    n_donors_st_df = filtered_n_donors_st_df.groupby(['hospital', pd.Grouper(key='date', freq='YE')]).agg({
        '17-24': 'sum',
        '25-29': 'sum',
        '30-34': 'sum',
        '40-44': 'sum',
        '45-49': 'sum',
        '50-54': 'sum',
        '55-59': 'sum',
        '60-64': 'sum'
    }).reset_index().set_index('date')
    n_donors_st_df_cols = ['17-24','25-29','30-34','40-44','45-49','50-54','55-59','60-64']
    selected_age_groups = st.multiselect(
        'Select age groups: ', 
        n_donors_st_df_cols, 
        default=n_donors_st_df_cols,
        key = 'hospital multiselect'
    )
    if selected_age_groups:
        n_donors_st_df = n_donors_st_df[selected_age_groups]
        st.write('New Donors By Age Group')
        st.bar_chart(n_donors_st_df)
    else:
        st.write('*Please select at least one age group to render the chart*')
    
    st.markdown("> For some reason in streamlit there's an issue with year groupings as you can see, therefore the buckets we see should be 1 year less")
  