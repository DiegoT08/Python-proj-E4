import pandas as pd
from sqlalchemy import create_engine

# --- Paramètres ---
CSV_PATH = "data/cleaned/pred-mai-mef-dhup_clean.csv"
DB_URL = "postgresql+psycopg2://mateo:projetdata@localhost:5432/loyers_db"

# --- Charger le CSV dans un DataFrame ---
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

# --- Créer l'engine SQLAlchemy ---
engine = create_engine(DB_URL)

# --- Insérer les données dans la table 'loyers' ---
# if_exists='replace' supprime les anciennes lignes, 'append' ajoute
df.to_sql('loyers', engine, if_exists='replace', index=False)

print("✅ Données importées dans la table 'loyers'")