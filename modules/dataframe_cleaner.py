"""module for dataframe operations"""
from datetime import datetime
import re
import pandas as pd


class DataFrameCleaner:
    def clean_dataframe(
        self, df: pd.DataFrame, date_column: list[str] = None
    ) -> pd.DataFrame:
        """
        cleans the dataframe using various functions

        Args:
            df (pd.DataFrame): pandas dataframe
            date_column (str): date column to be validated

        Returns:
            pd.DataFrame: pandas dataframe
        """
        self.date_columns: list[str] = date_column

        cleaning_methods = [
            self._format_columns,
            self._filter_negative_int,
            self._validate_date,
            self._drop_dupes,
        ]

        for method in cleaning_methods:
            df = method(df)

        return df

    def _format_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        converts CamelCase into snake_case using regex

        Args:
            column (str): column to be passed

        Output:
            returns the cleaned column name

        Example:
            - vendorID > vendor_id
            - TypeApheresisPlatelet > type_apheresis_platelet
        """
        df.columns = [
            re.sub(r"(?<!^)([A-Z]+)", r"_\1", col).lower().strip() for col in df.columns
        ]
        return df

    def _filter_negative_int(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        filters any negative int

        Args:
            df (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: pandas dataframe
        """
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                df[col] = df[col].mask(df[col] < 0)
        return df

    def _validate_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        converts the column to datetime else NaT

        Args:
            df (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: pandas dataframe
        """
        for date in self.date_columns:
            if date in df.columns:
                df[date] = pd.to_datetime(df[date], errors="coerce")
                df = df[df[date] <= datetime.now()]
        return df

    def _drop_dupes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drops duplicate rows from a dataframe

        Args:
            df (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: _description_
        """
        return df.drop_duplicates()
