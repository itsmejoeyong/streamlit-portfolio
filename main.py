"""main entrypoint to the the script"""
from modules.dataframe_cleaner import DataFrameCleaner
from modules.dataframe_manager import DataFrameManager

URL = "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv"

df_cleaner = DataFrameCleaner()
df_manager = DataFrameManager(URL)

df_to_clean = df_manager.df
cleaned_dataframe = df_cleaner.clean_dataframe(df_to_clean)
print(cleaned_dataframe.count())
