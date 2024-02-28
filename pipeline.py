"""main entrypoint to run the pipeline"""
import os

from modules.dataframe_cleaner import DataFrameCleaner
from modules.dataframe_manager import DataFrameManager

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


def main() -> None:
    for url in FILE_URLS:
        df_cleaner = DataFrameCleaner()
        df_manager = DataFrameManager(url)

        df_to_clean = df_manager.df
        cleaned_dataframe = df_cleaner.clean_dataframe(df_to_clean, DATES)

        load_folder = os.path.join(LOAD_FOLDER, f"{df_manager.name}.parquet")

        cleaned_dataframe.to_parquet(load_folder, index=False)


if __name__ == "__main__":
    main()
