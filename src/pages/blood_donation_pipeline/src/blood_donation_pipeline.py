"""module to abstract blood donation pipeline streamlit logic"""

import duckdb
import pandas as pd
import streamlit as st


class BloodDonationPipeline:
    def __init__(self, duckdb_conn):
        self.conn = duckdb_conn

    def display_about_section(self):
        with st.expander("About the project & data"):
            st.write("")
            st.write("""
            The second version of our Blood Donation Pipeline, a major refactor, code & tech wise, that led to a new repository. 

            The data is regarding blood donations that's made available through Ministry of Health (MOH).
            """)

            st.divider()

            st.subheader("Preview the data")
            # Query db information schema to get table list
            table_names_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            table_names_df = self.conn.execute(table_names_query).df()
            table_names = table_names_df["table_name"].tolist()

            # Create dropdown
            SELECT_TEXT = "Select a table to preview the data: "
            selected_table = st.selectbox(SELECT_TEXT, table_names)

            if selected_table:
                PREVIEW_DATA_QUERY = f"SELECT * FROM {selected_table} LIMIT 5;"
                df = self.conn.execute(PREVIEW_DATA_QUERY).df()

                st.dataframe(df)

    def display_donation_metrics_by_state(self):
        with st.expander("__Donation Metrics By State__"):
            st.write("")
            donations_state_query = """
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
            donations_state_Df = self.conn.execute(donations_state_query).df()
            dons_st_df_aggregate = (
                donations_state_Df.groupby(["state", pd.Grouper(key="date", freq="YE")])
                .agg(
                    {
                        "daily": "sum",
                        "blood_a": "sum",
                        "blood_b": "sum",
                        "blood_o": "sum",
                        "blood_ab": "sum",
                        "social_civilian": "sum",
                        "social_student": "sum",
                        "social_policearmy": "sum",
                        "donations_new": "sum",
                        "donations_regular": "sum",
                        "donations_irregular": "sum",
                    }
                )
                .reset_index()
            )

            # getting state list
            state_list = dons_st_df_aggregate["state"].unique().tolist()
            selected_state = "Select a state: "
            selected_state = st.selectbox(selected_state, state_list, index=3)

            # getting date range
            min_date = dons_st_df_aggregate["date"].min().to_pydatetime()
            max_date = dons_st_df_aggregate["date"].max().to_pydatetime()
            (slider_min, slider_max) = st.slider(
                "Date Range",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY/MM",
                key="state date slider",
            )

            # Filtering dataframe based on selection above
            filtered_dons_st_df = dons_st_df_aggregate[
                (dons_st_df_aggregate["state"] == selected_state)
                & (dons_st_df_aggregate["date"] >= slider_min)
                & (dons_st_df_aggregate["date"] <= slider_max)
            ]

            # set index to 'date' for better plotting
            filtered_dons_st_df.set_index("date", inplace=True)
            daily_type_col = ["daily"]
            blood_type_col = ["blood_a", "blood_b", "blood_o", "blood_ab"]
            social_type_col = ["social_civilian", "social_student", "social_policearmy"]
            donation_type_col = [
                "donations_new",
                "donations_regular",
                "donations_irregular",
            ]
            df_daily = filtered_dons_st_df[daily_type_col]
            df_blood_type = filtered_dons_st_df[blood_type_col]
            df_social_type = filtered_dons_st_df[social_type_col]
            df_donation_frequency = filtered_dons_st_df[donation_type_col]

            st.write("Total Blood Donations")
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

            new_donors_state_query = """
            SELECT
                *
            FROM newdonors_state;
            """

            # NOTE: NEW_DONORS_STATE_DF shorthand is: n_donors_st_df
            new_donors_state_df = self.conn.execute(new_donors_state_query).df()
            filtered_n_donors_st_df = new_donors_state_df[
                (new_donors_state_df["state"] == selected_state)
                & (new_donors_state_df["date"] >= slider_min)
                & (new_donors_state_df["date"] <= slider_max)
            ]
            n_donors_st_df = (
                filtered_n_donors_st_df.groupby(
                    ["state", pd.Grouper(key="date", freq="YE")]
                )
                .agg(
                    {
                        "17-24": "sum",
                        "25-29": "sum",
                        "30-34": "sum",
                        "40-44": "sum",
                        "45-49": "sum",
                        "50-54": "sum",
                        "55-59": "sum",
                        "60-64": "sum",
                    }
                )
                .reset_index()
                .set_index("date")
            )
            n_donors_st_df_cols = [
                "17-24",
                "25-29",
                "30-34",
                "40-44",
                "45-49",
                "50-54",
                "55-59",
                "60-64",
            ]
            selected_age_groups = st.multiselect(
                "Select age groups: ",
                n_donors_st_df_cols,
                default=n_donors_st_df_cols,
                key="state multiselect",
            )
            if selected_age_groups:
                n_donors_st_df = n_donors_st_df[selected_age_groups]
                st.write("New Donors By Age Group")
                st.bar_chart(n_donors_st_df)
            else:
                st.write("*Please select at least one age group to render the chart*")

            st.markdown(
                "> For some reason in streamlit there's an issue with year groupings as you can see, therefore the buckets we see should be 1 year less"
            )

    def display_donation_metrics_by_hospital(self):
        with st.expander("__Donation Metrics By Hospital__"):
            st.write("")
            donations_hospital_query = """
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
            donations_hospital_df = self.conn.execute(donations_hospital_query).df()
            dons_st_df_aggregate = (
                donations_hospital_df.groupby(
                    ["hospital", pd.Grouper(key="date", freq="YE")]
                )
                .agg(
                    {
                        "daily": "sum",
                        "blood_a": "sum",
                        "blood_b": "sum",
                        "blood_o": "sum",
                        "blood_ab": "sum",
                        "social_civilian": "sum",
                        "social_student": "sum",
                        "social_policearmy": "sum",
                        "donations_new": "sum",
                        "donations_regular": "sum",
                        "donations_irregular": "sum",
                    }
                )
                .reset_index()
            )

            # getting hospital list
            hospital_list = dons_st_df_aggregate["hospital"].unique().tolist()
            selected_hospital = "Select a hospital: "
            selected_hospital = st.selectbox(selected_hospital, hospital_list, index=21)

            # getting date range
            min_date = dons_st_df_aggregate["date"].min().to_pydatetime()
            max_date = dons_st_df_aggregate["date"].max().to_pydatetime()
            (slider_min, slider_max) = st.slider(
                "Date Range",
                min_value=min_date,
                max_value=max_date,
                value=(min_date, max_date),
                format="YYYY/MM",
                key="hospital date slider",
            )

            # Filtering dataframe based on selection above
            filtered_dons_st_df = dons_st_df_aggregate[
                (dons_st_df_aggregate["hospital"] == selected_hospital)
                & (dons_st_df_aggregate["date"] >= slider_min)
                & (dons_st_df_aggregate["date"] <= slider_max)
            ]

            # set index to 'date' for better plotting
            filtered_dons_st_df.set_index("date", inplace=True)
            daily_type_col = ["daily"]
            blood_type_col = ["blood_a", "blood_b", "blood_o", "blood_ab"]
            social_type_col = ["social_civilian", "social_student", "social_policearmy"]
            donation_type_col = [
                "donations_new",
                "donations_regular",
                "donations_irregular",
            ]
            df_daily = filtered_dons_st_df[daily_type_col]
            df_blood_type = filtered_dons_st_df[blood_type_col]
            df_social_type = filtered_dons_st_df[social_type_col]
            df_donation_frequency = filtered_dons_st_df[donation_type_col]

            st.write("Total Blood Donations")
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

            new_donors_hospital = """
            SELECT
                *
            FROM newdonors_facility;
            """

            # NOTE: NEW_DONORS_HOSPITAL_DF shorthand is: n_donors_st_df
            new_donors_hospital_df = self.conn.execute(new_donors_hospital).df()
            filtered_n_donors_st_df = new_donors_hospital_df[
                (new_donors_hospital_df["hospital"] == selected_hospital)
                & (new_donors_hospital_df["date"] >= slider_min)
                & (new_donors_hospital_df["date"] <= slider_max)
            ]
            n_donors_st_df = (
                filtered_n_donors_st_df.groupby(
                    ["hospital", pd.Grouper(key="date", freq="YE")]
                )
                .agg(
                    {
                        "17-24": "sum",
                        "25-29": "sum",
                        "30-34": "sum",
                        "40-44": "sum",
                        "45-49": "sum",
                        "50-54": "sum",
                        "55-59": "sum",
                        "60-64": "sum",
                    }
                )
                .reset_index()
                .set_index("date")
            )
            n_donors_st_df_cols = [
                "17-24",
                "25-29",
                "30-34",
                "40-44",
                "45-49",
                "50-54",
                "55-59",
                "60-64",
            ]
            selected_age_groups = st.multiselect(
                "Select age groups: ",
                n_donors_st_df_cols,
                default=n_donors_st_df_cols,
                key="hospital multiselect",
            )
            if selected_age_groups:
                n_donors_st_df = n_donors_st_df[selected_age_groups]
                st.write("New Donors By Age Group")
                st.bar_chart(n_donors_st_df)
            else:
                st.write("*Please select at least one age group to render the chart*")

            st.markdown(
                "> For some reason in streamlit there's an issue with year groupings as you can see, therefore the buckets we see should be 1 year less"
            )

    def display_granular_dataset_analysis(self):
        selected_age_group = st.selectbox(
            "select age group",
            ["20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"],
        )

        st.header("")

        granular_average_months_between_donations_result = f"""
        SELECT
            average_months_between_visits
        FROM
            granular_average_months_between_donations_query
        WHERE
            age_group = '{selected_age_group}';
        """
        granular_average_months_between_visits_table = self.conn.execute(
            granular_average_months_between_donations_result
        ).df()

        # NOTE: churn definition: users who never donate blood once every 2 years
        granular_average_months_before_churn_result_v2 = f"""
        SELECT
            average_months_to_churn
        FROM
            granular_average_months_before_churn_query_v2
        WHERE
            age_group = '{selected_age_group}';
        """
        granular_average_months_before_churn_table_v2 = self.conn.execute(
            granular_average_months_before_churn_result_v2
        ).df()
        avg_months_to_churn = (
            granular_average_months_before_churn_table_v2[
                "average_months_to_churn"
            ].iloc[0]
            if not granular_average_months_before_churn_table_v2.empty
            else "N/A"
        )

        granular_average_donations_by_age_group_result = f"""
        SELECT
            avg_donations
        FROM
            granular_average_donations_by_age_group_query
        WHERE
            age_group = '{selected_age_group}';
        """
        granular_average_donations_by_age_group_table = self.conn.execute(
            granular_average_donations_by_age_group_result
        ).df()
        avg_donations = (
            granular_average_donations_by_age_group_table["avg_donations"].iloc[0]
            if not granular_average_donations_by_age_group_table.empty
            else "N/A"
        )

        granular_cohorts_result = f"""
        SELECT
            nth_year,
            average_retention_rate
        FROM
            granular_cohorts_query
        WHERE
            age_group = '{selected_age_group}';
        """

        granular_cohorts_df = self.conn.execute(granular_cohorts_result).df()

        # eating dinner
        metric1, metric2, metric3 = st.columns(3)
        with metric1:
            st.metric(
                "Average months between visits",
                granular_average_months_between_visits_table[
                    "average_months_between_visits"
                ],
            )
        with metric2:
            st.metric("Average months to churn", avg_months_to_churn)
        with metric3:
            st.metric(
                "Average donations within age group",
                avg_donations,
            )

        granular_cohorts_df = granular_cohorts_df.set_index("nth_year")
        st.write("average % retention rate on nth year")
        st.bar_chart(granular_cohorts_df, color=(244, 67, 54, 0.7))
