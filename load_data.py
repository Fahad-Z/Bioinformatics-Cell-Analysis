import sqlite3
from pathlib import Path

import pandas as pd


csv_file = Path("cell-count.csv")
database_file = Path("cell_counts.db")

data = pd.read_csv(csv_file)

connection = sqlite3.connect(database_file)

data.to_sql(
    "samples",
    connection,
    if_exists="replace",
    index=False,
)

connection.close()

print(f"Loaded data")