"""module for managing dataframes"""

import logging
import os
from pathlib import Path

import pandas as pd


class DataFrameManager:
    def __init__(self, path_to_df: str):
        self.logger = logging.getLogger(os.path.basename(__file__))
        self.file_path = path_to_df
        self.path = Path(path_to_df)
        self.name = self.path.name.split(".")[0].replace("-", "_")
        self.df = self._initialize_df()

    def _initialize_df(self) -> pd.DataFrame:
        """
        reads a csv/parquet via URL/file

        Returns:
            pd.DataFrame: pandas dataframe

        Raises:
            ValueError: If the file format is not supported
        """
        self.logger.info("starting process to initlaize a dataframe")
        last_exception = None
        readers = [self.read_csv, self.read_parquet]

        for reader in readers:
            try:
                df = reader(self.file_path)
                return df
            except Exception as e:
                self.logger.info(f"error reading dataframe: {e}, using next reader")
                last_exception = e
        self.logger.info(f"failed to read using readers provided: {last_exception}")
        raise ValueError(
            f"Failed to read the file as any supported format. Last error: {last_exception}"
        )

    @staticmethod
    def read_csv(path: Path) -> pd.DataFrame:
        return pd.read_csv(path)

    @staticmethod
    def read_parquet(path: Path) -> pd.DataFrame:
        return pd.read_parquet(path)

    def write_df_to_file(
        self,
        output_path: str = None,
        file_type: str = "csv",
        index: bool = False,
        compress: bool = False,
    ) -> None:
        self.logger.info("starting process to write dataframe to a file")
        if output_path is None:
            output_path = self.file_path.rsplit(".", 1)[0] + f"_modified.{file_type}"

        writer = {
            "csv": self._write_csv,
            "xlsx": self._write_xlsx,
            "parquet": self._write_parquet,
        }

        if file_type not in writer:
            self.logger.info(".extension format to write dataframe to not supported")
            raise ValueError("Supported types are csv, xlsx/excel & parquet")
        writer[file_type](output_path, index, compress)
        self.logger.info("Dataframe writing process completed")

    def _write_csv(self, output, index, compress):
        self.logger.info("writing dataframe to a csv file")
        compression = "gzip" if compress else None
        self.df.to_csv(output, index=index, compression=compression)

    def _write_xlsx(self, output, index, compress):
        self.logger.info("writing dataframe to an xlsx file")
        # NOTE: no compression option for excel
        self.df.to_excel(output, index=index)

    def _write_parquet(self, output, index, compress):
        self.logger.info("writing dataframe to a parquet file")
        compression = "gzip" if compress else None
        self.df.to_parquet(output, index=index, compression=compression)
