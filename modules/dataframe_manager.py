"""module for managing dataframes"""
from pathlib import Path

import pandas as pd

class DataFrameManager():
    def __init__(self, path_to_df: str):
        self.file_path = path_to_df
        self.path = Path(path_to_df)
        self.name = self.path.name
        self.df = self._initialize_df()
    
    def _initialize_df(self) -> pd.DataFrame:
        """
        reads a csv/parquet via URL/file

        Returns:
            pd.DataFrame: pandas dataframe
        
        Raises:
            ValueError: If the file format is not supported
        """
        last_exception = None
        readers = [
            self.read_csv,
            self.read_parquet
        ]
        
        for reader in readers:
            try:
                return reader(self.file_path)
            except Exception as e:
                last_exception = e
            
            raise ValueError(f"Failed to read the file as any supported format. Last error: {last_exception}")
    
    @staticmethod
    def read_csv(path: Path) -> pd.DataFrame:
        return pd.read_csv(path)
    
    @staticmethod
    def read_parquet(path: Path) -> pd.DataFrame:
        return pd.read_parquet(path)
    
    
    def write_df_to_file(self, output_path: str = None, file_type: str = 'csv', index: bool = False, compress: bool = False) -> None:
        if output_path is None:
            output_path = self.file_path.rsplit('.', 1)[0] + f"_modified.{file_type}"
        
        writer = {
            'csv': self._write_csv,
            'xlsx': self._write_xlsx,
            'parquet': self._write_parquet
        }
        
        if file_type in writer:
            writer[file_type](output_path, index, compress)
        else:
            raise ValueError("Supported types are csv, xlsx/excel & parquet")
    
    def _write_csv(self, output, index, compress):
        compression = 'gzip' if compress else None
        self.df.to_csv(output, index=index, compression=compression)

    def _write_xlsx(self, output, index, compress):
        # NOTE: no compression option for excel
        self.df.to_excel(output, index=index)

    def _write_parquet(self, output, index, compress):
        compression = 'gzip' if compress else None
        self.df.to_parquet(output, index=index, compression=compression)
