import pandas as pd
from sqlalchemy import create_engine

# Charger le CSV
df = pd.read_csv("data/cleaned/pred-mai-mef-dhup_clean.csv", sep=";")

# Connexion à PostgreSQL
engine = create_engine("postgresql+psycopg2://mateo:projet_data@localhost:5432/loyers_db")

# Envoi du DataFrame dans la BDD
df.to_sql("loyers", engine, if_exists="replace", index=False)

print("✅ Données importées dans PostgreSQL avec succès.")