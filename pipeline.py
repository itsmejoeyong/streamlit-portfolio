"""main entrypoint to run the pipeline"""

from datetime import datetime
import logging
import os

from src.dataframe_cleaner import DataFrameCleaner
from src.dataframe_manager import DataFrameManager

import duckdb

##### LOGGING #####
DATE_NOW = datetime.now().strftime("%Y/%m/%d")
LOG_NAME = "blood-donation-pipeline.log"
LOG_DIR = os.path.join("logs", DATE_NOW)
LOG_FILEPATH = os.path.join(LOG_DIR, LOG_NAME)
os.makedirs(LOG_DIR, exist_ok=True)
logger = logging.getLogger(os.path.basename(__file__))
logging.basicConfig(
    filename=LOG_FILEPATH,
    level=logging.INFO,
    format="%(asctime)s : %(name)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


FILE_URLS = [
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_facility.csv",
    "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_state.csv",
    "https://dub.sh/ds-data-granular",
]

DATES = ["date", "visit_date"]

LOAD_FOLDER = "load"
DUCKDB_FOLDER = "duckdb"
if not os.path.exists(LOAD_FOLDER):
    os.makedirs(LOAD_FOLDER)
if not os.path.exists(DUCKDB_FOLDER):
    os.makedirs(DUCKDB_FOLDER)

DUCKDB_CONN = duckdb.connect(database="duckdb/blood_donation_pipeline_v2.duckdb")


def main() -> None:
    logger.info("beginning of log: running pipeline.py")
    for url in FILE_URLS:
        df_cleaner = DataFrameCleaner()
        df_manager = DataFrameManager(url)
        df_name = df_manager.name
        df = df_manager.df

        # duckdb will select from this variable
        cleaned_df = df_cleaner.clean_dataframe(df, DATES)

        query = f"CREATE OR REPLACE TABLE {df_name} AS SELECT * FROM cleaned_df;"
        DUCKDB_CONN.execute(query)
    logger.info("end of log: pipeline.py completed successfully")


if __name__ == "__main__":
    main()
