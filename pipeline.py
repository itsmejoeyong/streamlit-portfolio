"""main entrypoint to run the pipeline"""
import os

from modules.dataframe_cleaner import DataFrameCleaner
from modules.dataframe_manager import DataFrameManager

import duckdb

FILE_URLS = [
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_facility.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_state.csv",
    "https://dub.sh/ds-data-granular",
]

DATES = ["date", "visit_date"]

LOAD_FOLDER = "load"
if not os.path.exists(LOAD_FOLDER):
    os.makedirs(LOAD_FOLDER)

DUCKDB_CONN = duckdb.connect(database='duckdb/blood_donation_pipeline_v2.duckdb')

def main() -> None:
    for url in FILE_URLS:
        df_cleaner = DataFrameCleaner()
        df_manager = DataFrameManager(url)
        df_name = df_manager.name
        load_folder = os.path.join(LOAD_FOLDER, f"{df_name}.parquet")

        df = df_manager.df
        cleaned_df = df_cleaner.clean_dataframe(df, DATES)
        
        query = f"CREATE OR REPLACE TABLE {df_name} AS SELECT * FROM cleaned_df;"
        DUCKDB_CONN.execute(query)


if __name__ == "__main__":
    main()
