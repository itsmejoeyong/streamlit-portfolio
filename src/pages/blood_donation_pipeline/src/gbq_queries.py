granular_average_months_between_donations_query = """
WITH next_visit AS (
    SELECT
        birth_date,
        DATE(visit_date) AS visit_date,
        LEAD(DATE(visit_date)) OVER(PARTITION BY donor_id ORDER BY visit_date) AS next_visit_date
    FROM
        blood_donation_pipeline_v2.ds_data_granular
),

age_and_days AS (
    SELECT
        DATE_DIFF(visit_date, next_visit_date, DAY) AS days_between_visit,
        EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
    FROM    
        next_visit
),

age_groups AS (
    SELECT
        *,
        CASE
            WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
            WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
            WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
            WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
            WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
            WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
            WHEN age_on_visit >= 80 THEN '80+'
        END AS age_group,
        CASE
            WHEN age_on_visit < 20 THEN 1
            WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
            WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
            WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
            WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
            WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
            WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
            WHEN age_on_visit >= 80 THEN 8
        END AS age_group_order
    FROM
        age_and_days
    WHERE
        CASE
            WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
            WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
            WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
            WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
            WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
            WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
            WHEN age_on_visit >= 80 THEN '80+'
        END IS NOT NULL
)


SELECT
    age_group,
    ABS(FLOOR(AVG(days_between_visit) / 30)) AS average_months_between_visits
FROM
    age_groups
WHERE
    age_group IS NOT NULL
GROUP BY
    age_group,
    age_group_order
ORDER BY
    age_group_order;
"""


granular_average_months_before_churn_query_v2 = """
WITH next_visit AS (
    SELECT
        donor_id,
        birth_date,
        DATE(visit_date) AS visit_date,
        LEAD(DATE(visit_date)) OVER(PARTITION BY donor_id ORDER BY visit_date) AS next_visit_date
    FROM
        blood_donation_pipeline_v2.ds_data_granular
),

age_and_days AS (
    SELECT
        donor_id,
        visit_date,
        next_visit_date,
        ABS(DATE_DIFF(visit_date, next_visit_date, DAY)) AS days_between_visit,
        EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
    FROM    
        next_visit
),

age_groups AS (
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
        age_and_days
    WHERE
        CASE
            WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
            WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
            WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
            WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
            WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
            WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
            WHEN age_on_visit > 80 THEN '80+'
        END IS NOT NULL
),

rolling_sum_of_total_visits AS (
    SELECT
        *,
        SUM(days_between_visit) OVER(PARTITION BY donor_id ORDER BY visit_date) AS rolling_total_days_between_visit
    FROM
        age_groups
),

days_before_churn AS (
    SELECT
        *,
        DATE_DIFF(DATE(CONCAT(EXTRACT(YEAR FROM visit_date) + 2, '-12-31')), visit_date, DAY) AS days_before_next_churn
    FROM
        rolling_sum_of_total_visits
),

churns AS (
    SELECT
        *,
        IF(days_between_visit > days_before_next_churn, 1, 0) AS is_churn
    FROM
        days_before_churn
    WHERE
        IF(days_between_visit > days_before_next_churn, 1, 0) = 1
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
    age_group_order;
"""

granular_average_donations_by_age_group_query = """
WITH age AS (
    SELECT
        donor_id,
        visit_date,
        EXTRACT(YEAR FROM visit_date) - birth_date AS age_on_visit
    FROM
        blood_donation_pipeline_v2.ds_data_granular
),

age_groups AS (
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
        age
    WHERE
        age_on_visit >= 20 AND age_on_visit <= 80
),

n_donations_by_age_group_and_donor AS (
    SELECT
        donor_id,
        age_group,
        age_group_order,
        COUNT(*) AS n_donations
    FROM
        age_groups
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
    age_group_order;
"""
granular_cohorts_query = """
WITH first_year_donation AS (
    SELECT
        donor_id,
        EXTRACT(YEAR FROM MIN(visit_date)) AS first_donation_year,
        EXTRACT(YEAR FROM MIN(visit_date)) - birth_date AS age_on_first_donation
    FROM
        blood_donation_pipeline_v2.ds_data_granular
    GROUP BY
        donor_id,
        birth_date
),
age_group_assignment AS (
    SELECT
        donor_id,
        first_donation_year,
        CASE
            WHEN age_on_first_donation < 20 THEN '<20'
            WHEN age_on_first_donation BETWEEN 20 AND 29 THEN '20-29'
            WHEN age_on_first_donation BETWEEN 30 AND 39 THEN '30-39'
            WHEN age_on_first_donation BETWEEN 40 AND 49 THEN '40-49'
            WHEN age_on_first_donation BETWEEN 50 AND 59 THEN '50-59'
            WHEN age_on_first_donation BETWEEN 60 AND 69 THEN '60-69'
            WHEN age_on_first_donation BETWEEN 70 AND 79 THEN '70-79'
            WHEN age_on_first_donation >= 80 THEN '80+'
        END AS age_group
    FROM
        first_year_donation
),
yearly_donations AS (
    SELECT
        aga.donor_id,
        aga.first_donation_year,
        aga.age_group,
        EXTRACT(YEAR FROM ds.visit_date) AS donation_year
    FROM
        blood_donation_pipeline_v2.ds_data_granular ds
    JOIN
        age_group_assignment aga ON ds.donor_id = aga.donor_id
),
cohorts AS (
    SELECT
        first_donation_year,
        donation_year,
        age_group,
        COUNT(DISTINCT donor_id) AS n_donors
    FROM
        yearly_donations
    GROUP BY
        first_donation_year,
        donation_year,
        age_group
),
initial_cohort_size AS (
    SELECT
        first_donation_year,
        age_group,
        COUNT(DISTINCT donor_id) AS initial_donors
    FROM
        age_group_assignment
    GROUP BY
        first_donation_year,
        age_group
),
cohort_retention AS (
    SELECT
        c.first_donation_year,
        c.donation_year,
        c.age_group,
        c.n_donors,
        ic.initial_donors,
        ROUND((c.n_donors / CAST(ic.initial_donors AS FLOAT64)) * 100, 2) AS retention_rate
    FROM
        cohorts c
    JOIN
        initial_cohort_size ic ON c.first_donation_year = ic.first_donation_year AND c.age_group = ic.age_group
    WHERE
        c.donation_year >= c.first_donation_year
),
retention_by_nth_year AS (
    SELECT
        age_group,
        donation_year - first_donation_year + 1 AS nth_year,
        ROUND(AVG(retention_rate), 2) AS average_retention_rate
    FROM
        cohort_retention
    WHERE
        donation_year - first_donation_year + 1 <= 10
    GROUP BY
        age_group,
        nth_year
    ORDER BY
        age_group,
        nth_year
)
SELECT
    age_group,
    nth_year,
    average_retention_rate
FROM
    retention_by_nth_year
"""
# granular_cohorts_query = """
# WITH first_year_donation AS (
#     SELECT
#         donor_id,
#         EXTRACT(YEAR FROM MIN(visit_date)) - birth_date AS age_on_visit,
#         EXTRACT(YEAR FROM MIN(visit_date)) AS first_donation_year
#     FROM
#         blood_donation_pipeline_v2.ds_data_granular
#     GROUP BY
#         donor_id,
#         birth_date
# ),

# yearly_donations AS (
#     SELECT
#         fd.donor_id,
#         fd.first_donation_year,
#         EXTRACT(YEAR FROM ds.visit_date) AS donation_year,
#         EXTRACT(YEAR FROM ds.visit_date) - ds.birth_date AS age_on_visit
#     FROM
#         blood_donation_pipeline_v2.ds_data_granular ds
#     JOIN
#         first_year_donation fd
#         ON fd.donor_id = ds.donor_id
# ),

# cohorts AS (
#     SELECT
#         first_donation_year,
#         donation_year,
#         CASE
#             WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
#             WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
#             WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
#             WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
#             WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
#             WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
#             WHEN age_on_visit > 80 THEN '80+'
#         END AS age_group,
#         CASE
#             WHEN age_on_visit < 20 THEN 1
#             WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
#             WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
#             WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
#             WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
#             WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
#             WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
#             WHEN age_on_visit > 80 THEN 8
#         END AS age_group_order,
#         COUNT(DISTINCT donor_id) AS n_donors
#     FROM
#         yearly_donations
#     GROUP BY
#         first_donation_year,
#         donation_year,
#         age_group,
#         age_group_order
# ),

# initial_cohort_size AS (
#         SELECT
#             first_donation_year,
#             CASE
#                 WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
#                 WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
#                 WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
#                 WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
#                 WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
#                 WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
#                 WHEN age_on_visit > 80 THEN '80+'
#                 END AS age_group,
#             CASE
#                 WHEN age_on_visit < 20 THEN 1
#                 WHEN age_on_visit BETWEEN 20 AND 29 THEN 2
#                 WHEN age_on_visit BETWEEN 30 AND 39 THEN 3
#                 WHEN age_on_visit BETWEEN 40 AND 49 THEN 4
#                 WHEN age_on_visit BETWEEN 50 AND 59 THEN 5
#                 WHEN age_on_visit BETWEEN 60 AND 69 THEN 6
#                 WHEN age_on_visit BETWEEN 70 AND 79 THEN 7
#                 WHEN age_on_visit > 80 THEN 8
#                 END AS age_group_order,
#             COUNT(DISTINCT donor_id) AS initial_donors
#         FROM
#             first_year_donation
#         WHERE
#             CASE
#                 WHEN age_on_visit BETWEEN 20 AND 29 THEN '20-29'
#                 WHEN age_on_visit BETWEEN 30 AND 39 THEN '30-39'
#                 WHEN age_on_visit BETWEEN 40 AND 49 THEN '40-49'
#                 WHEN age_on_visit BETWEEN 50 AND 59 THEN '50-59'
#                 WHEN age_on_visit BETWEEN 60 AND 69 THEN '60-69'
#                 WHEN age_on_visit BETWEEN 70 AND 79 THEN '70-79'
#                 WHEN age_on_visit > 80 THEN '80+'
#                 END IS NOT NULL
#         GROUP BY
#             first_donation_year,
#             age_group,
#             age_group_order
# ),

# cohort_retention AS (
#     SELECT
#         c.first_donation_year,
#         c.donation_year,
#         c.age_group,
#         c.age_group_order,
#         c.n_donors,
#         ic.initial_donors,
#         ROUND((c.n_donors / ic.initial_donors) * 100, 2) AS retention_rate
#     FROM
#         cohorts c
#     JOIN
#         initial_cohort_size ic
#         ON c.first_donation_year = ic.first_donation_year AND c.age_group = ic.age_group
#     WHERE
#         c.donation_year >= c.first_donation_year
# ),

# retention_by_nth_year AS (
#     SELECT
#         age_group,
#         age_group_order,
#         donation_year - first_donation_year + 1 AS nth_year,
#         ROUND(AVG(retention_rate), 2) AS average_retention_rate
#     FROM
#         cohort_retention
#     WHERE
#         donation_year - first_donation_year + 1 <= 10
#     GROUP BY
#         age_group,
#         age_group_order,
#         nth_year
#     ORDER BY
#         age_group_order,
#         nth_year
# )

# SELECT
#     age_group,
#     nth_year,
#     average_retention_rate
# FROM
#     retention_by_nth_year
# """
