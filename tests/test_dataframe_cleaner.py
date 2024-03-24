import numpy as np
import pandas as pd
import pytest
from modules.dataframe_cleaner import DataFrameCleaner


@pytest.fixture
def sample_dataframe():
    data = {
        "VendorID": [1, 2, 3, -1, -2],
        "SomeDateColumn": [
            "2021-01-01",
            "not a date",
            "2021-03-01",
            "2021-04-01",
            "2021-05-01",
        ],
        "DuplicateColumn": [1, 1, 2, 3, 3],
    }
    df = pd.DataFrame(data)
    return df


DATE_COL = ["some_date_column"]


def test_clean_dataframe_format_columns(sample_dataframe):
    cleaner = DataFrameCleaner()
    cleaned_df = cleaner.clean_dataframe(sample_dataframe, DATE_COL)

    expected_columns = ["vendor_id", "some_date_column", "duplicate_column"]
    assert (
        list(cleaned_df.columns) == expected_columns
    ), "columns names were not formatted correctly"


def test_clean_dataframe_filter_negative_int(sample_dataframe):
    cleaner = DataFrameCleaner()
    cleaned_df = cleaner.clean_dataframe(sample_dataframe, DATE_COL)

    assert cleaned_df["vendor_id"].min() >= 0, "there are negative int values"


def test_clean_dataframe_validate_date(sample_dataframe):
    cleaner = DataFrameCleaner()
    cleaned_df = cleaner.clean_dataframe(sample_dataframe, DATE_COL)

    print(cleaned_df.head())
    assert pd.isnull(
        # .at is similar to accessing an index of a list (in this case the index of a row)
        cleaned_df.at[1, "some_date_column"]
    ), "Invalid date was not coerced to NaT."


def test_clean_dataframe_drop_dupes(sample_dataframe):
    cleaner = DataFrameCleaner()
    # Manually adding duplicate row for testing using pd.concat instead of append
    duplicated_df = pd.concat(
        [sample_dataframe, sample_dataframe.iloc[[0]]], ignore_index=True
    )
    cleaned_df = cleaner.clean_dataframe(duplicated_df, DATE_COL)

    assert (
        cleaned_df.shape[0] == sample_dataframe.shape[0]
    ), "Duplicate rows were not properly dropped."
