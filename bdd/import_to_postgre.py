import pandas as pd
from sqlalchemy import create_engine
import os

DB_FILE = "loyers.db"
DB_URL = f"sqlite:///{DB_FILE}"

CSV_PATH = "data/cleaned/pred-mai-mef-dhup_clean_coords.csv"

# Charger CSV
df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

# Engine SQLite
engine = create_engine(DB_URL)

# Remplacer les données
df.to_sql("loyers", engine, if_exists="replace", index=False)

print("✅ Données importées dans loyers.db (SQLite)")