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
    st.write("")
    st.write(EXPANDER_TEXT)
    
    st.divider()
    
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
    st.write("")
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
    
    st.divider()
    
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
    
    st.divider()
    
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
    st.write("")
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
    
    st.divider()

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

st.divider()

age_group_to_age_query = {
    '20-29': 'BETWEEN 20 AND 29',
    '30-39': 'BETWEEN 30 AND 39',
    '40-49': 'BETWEEN 40 AND 49',
    '50-59': 'BETWEEN 50 AND 59',
    '60-69': 'BETWEEN 60 AND 69',
    '70-79': 'BETWEEN 70 AND 79',
    '80+': '>= 80'
}
selected_age_group = st.selectbox("select age group", ['20-29','30-39','40-49','50-59','60-69','70-79', '80+'])
age_filter_query = age_group_to_age_query.get(selected_age_group)

st.header("")

granular_average_months_between_donations_query = f"""
WITH next_visit AS(
SELECT
    birth_date,
    visit_date::DATE as visit_date,
    LEAD(visit_date::DATE) OVER(PARTITION BY donor_id ORDER BY visit_date) AS next_visit_date
FROM
    ds_data_granular
),

age_on_visit AS(
SELECT
    ABS(visit_date - next_visit_date) AS days_between_visit,
    EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
FROM    
    next_visit
WHERE
    age_on_visit {age_filter_query}
),

age_group AS(
    SELECT
    *,
    CASE
        WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
        WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
        WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
        WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
        WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
        WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
        WHEN age_on_visit > 80 THEN '80+'
        END AS age_group,
    CASE
        WHEN age_on_visit < 20 THEN 1
        WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
        WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
        WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
        WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
        WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
        WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
        WHEN age_on_visit > 80 THEN 8
        END AS age_group_order
FROM
    age_on_visit
WHERE
    age_group IS NOT NULL
)

SELECT
    age_group,
    FLOOR(AVG(days_between_visit) / 30) AS average_months_between_visits
FROM
    age_group
WHERE
    age_group IS NOT NULL
GROUP BY
    age_group,
    age_group_order
ORDER BY
    age_group_order
"""
granular_average_months_between_visits_table = con.execute(granular_average_months_between_donations_query).df()

# NOTE: churn definition: users who never donate blood once every 2 years
granular_average_months_before_churn_query_v2 = f"""
WITH next_visit AS(
SELECT
    donor_id,
    birth_date,
    visit_date::DATE as visit_date,
    LEAD(visit_date::DATE) OVER(PARTITION BY donor_id ORDER BY visit_date) AS next_visit_date
FROM
    ds_data_granular
),

age_on_visit AS(
SELECT
    donor_id,
    visit_date,
    next_visit_date,
    ABS(visit_date - next_visit_date) AS days_between_visit,
    EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
FROM    
    next_visit 
WHERE
    age_on_visit {age_filter_query}
),

age_group AS(
    SELECT
    *,
    CASE
        WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
        WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
        WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
        WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
        WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
        WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
        WHEN age_on_visit > 80 THEN '80+'
        END AS age_group,
    CASE
        WHEN age_on_visit < 20 THEN 1
        WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
        WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
        WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
        WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
        WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
        WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
        WHEN age_on_visit > 80 THEN 8
        END AS age_group_order
FROM
    age_on_visit
WHERE
    age_group IS NOT NULL
),

rolling_sum_of_total_visits AS(
SELECT
    *,
    SUM(days_between_visit) OVER(PARTITION BY donor_id ORDER BY visit_date) AS rolling_total_days_between_visit,
FROM
    age_group
),

days_before_churn AS(
SELECT
    *,
    CONCAT(EXTRACT(YEAR FROM visit_date) + 2, '-12-31')::DATE - visit_date AS days_before_next_churn
FROM
    rolling_sum_of_total_visits
),

churns AS(
SELECT
    *,
    IF(days_between_visit > days_before_next_churn, 1, 0) AS is_churn
FROM
    days_before_churn
WHERE
    is_churn = 1
)

SELECT
    age_group,
    FLOOR(AVG(rolling_total_days_between_visit / 30)) AS average_months_to_churn
FROM
    churns
GROUP BY
    age_group,
    age_group_order
ORDER BY
    age_group_order
"""
granular_average_months_before_churn_table_v2 = con.execute(granular_average_months_before_churn_query_v2).df()

granular_average_donations_by_age_group_query = f"""
WITH age_on_visit AS(
    SELECT
    donor_id,
    visit_date,
    EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
FROM
    ds_data_granular
WHERE
    age_on_visit {age_filter_query}
),

age_group AS(
SELECT
    *,
    CASE
        WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
        WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
        WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
        WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
        WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
        WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
        WHEN age_on_visit > 80 THEN '80+'
        END AS age_group,
    CASE
        WHEN age_on_visit < 20 THEN 1
        WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
        WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
        WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
        WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
        WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
        WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
        WHEN age_on_visit > 80 THEN 8
        END AS age_group_order
FROM
    age_on_visit
WHERE
    age_group IS NOT NULL
),

n_donations_by_age_group_and_donor AS(
SELECT
    donor_id,
    age_group,
    age_group_order,
    COUNT(*) AS n_donations
FROM
    age_group
WHERE
    age_group IS NOT NULL
GROUP BY
    donor_id,
    age_group,
    age_group_order
)

SELECT
    age_group,
    ROUND(AVG(n_donations), 2) AS avg_donations
FROM
    n_donations_by_age_group_and_donor
GROUP BY
    age_group,
    age_group_order
ORDER BY
    age_group_order
"""
granular_average_donations_by_age_group_table = con.execute(granular_average_donations_by_age_group_query).df()

granular_cohorts_query = f"""
WITH first_year_donation AS(
SELECT
    donor_id,
    EXTRACT(YEAR FROM MIN(visit_date)) - birth_date AS age_on_visit,
    EXTRACT(YEAR FROM MIN(visit_date)) AS first_donation_year
FROM
    ds_data_granular
GROUP BY
    donor_id,
    birth_date
HAVING
    age_on_visit {age_filter_query}
),

yearly_donations AS(
SELECT
    fd.donor_id,
    fd.first_donation_year,
    EXTRACT(YEAR FROM visit_date) AS donation_year,
    EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
FROM
    ds_data_granular AS ds
JOIN
    first_year_donation AS fd
    USING(donor_id)
WHERE
    age_on_visit {age_filter_query}
),

cohorts AS(
SELECT
    first_donation_year,
    donation_year,
    CASE
        WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
        WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
        WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
        WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
        WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
        WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
        WHEN age_on_visit > 80 THEN '80+'
        END AS age_group,
    CASE
        WHEN age_on_visit < 20 THEN 1
        WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
        WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
        WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
        WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
        WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
        WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
        WHEN age_on_visit > 80 THEN 8
        END AS age_group_order,
    COUNT(DISTINCT donor_id) AS n_donors
FROM
    yearly_donations AS yd
WHERE
    age_group IS NOT NULL
GROUP BY
    first_donation_year,
    donation_year,
    age_group,
    age_group_order
),

initial_cohort_size AS(
SELECT
    first_donation_year,
    CASE
        WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
        WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
        WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
        WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
        WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
        WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
        WHEN age_on_visit > 80 THEN '80+'
        END AS age_group,
    CASE
        WHEN age_on_visit < 20 THEN 1
        WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
        WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
        WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
        WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
        WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
        WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
        WHEN age_on_visit > 80 THEN 8
        END AS age_group_order,
    COUNT(DISTINCT donor_id) AS initial_donors
FROM
    first_year_donation
WHERE
    age_group IS NOT NULL
GROUP BY
    first_donation_year,
    age_group,
    age_group_order
),

cohort_retention AS (
SELECT
    c.first_donation_year,
    c.donation_year,
    c.age_group,
    c.age_group_order,
    c.n_donors,
    ic.initial_donors,
    ROUND((c.n_donors / ic.initial_donors) * 100, 2) AS retention_rate
FROM
    cohorts AS c
JOIN
    initial_cohort_size AS ic
    USING(first_donation_year, age_group)
WHERE
    c.donation_year >= c.first_donation_year
),

retention_by_nth_year AS (
SELECT
    age_group,
    age_group_order,
    donation_year - first_donation_year + 1 AS nth_year,
    ROUND(AVG(retention_rate), 2) AS average_retention_rate
FROM
    cohort_retention
WHERE
    nth_year <= 10
GROUP BY
    age_group,
    age_group_order,
    nth_year
ORDER BY
    age_group_order,
    nth_year
)

SELECT
    age_group,
    nth_year,
    average_retention_rate
FROM
    retention_by_nth_year
"""

granular_cohorts_table = con.execute(granular_cohorts_query).df()

# eating dinner
metric1, metric2, metric3 = st.columns(3)
with metric1:
    st.metric("Average months between visits", granular_average_months_between_visits_table['average_months_between_visits'])
with metric2:
    st.metric("Average months to churn", granular_average_months_before_churn_table_v2['average_months_to_churn'])
with metric3:
    st.metric("Average donations within age group", granular_average_donations_by_age_group_table['avg_donations'])
    

st.dataframe(granular_cohorts_table)