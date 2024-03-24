"""module for dataframe operations"""

from datetime import datetime
import logging
import os
import re

import pandas as pd


class DataFrameCleaner:
    def __init__(self):
        self.logger = logging.getLogger(os.path.basename(__file__))

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
        self.logger.info("Starting dataframe cleaning process")
        self.date_columns: list[str] = date_column

        cleaning_methods = [
            self._format_columns,
            self._validate_int,
            self._validate_date,
            self._drop_dupes,
        ]

        for method in cleaning_methods:
            self.logger.debug(f"applying cleaning method: {method}")
            df = method(df)

        self.logger.info("Dataframe cleaning process completed")
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
        self.logger.info("formatting columns to use snake_case case type")
        df.columns = [
            re.sub(r"(?<!^)([A-Z]+)", r"_\1", col).lower().strip() for col in df.columns
        ]
        return df

    def _validate_int(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        replaces any negative int values with NaN

        Args:
            df (pd.DataFrame): pandas dataframe

        Returns:
            pd.DataFrame: pandas dataframe
        """
        self.logger.info("validating integer columns")
        for col in df.columns:
            if pd.api.types.is_integer_dtype(df[col]):
                self.logger.debug(f"validating column: {col}")
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
        self.logger.info("validating date columns")
        for date in self.date_columns:
            if date in df.columns:
                self.logger.debug(f"converting column: {date} to datetime data type")
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
        self.logger.info("dropping duplicates")
        return df.drop_duplicates()
