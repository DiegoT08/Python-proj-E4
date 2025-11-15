import pandas as pd
from sqlalchemy import create_engine, text  # Importer 'text' de SQLAlchemy

# --- Paramètres ---
CSV_PATH = "data/cleaned/pred-mai-mef-dhup_clean_coords.csv"
DB_URL = "postgresql+psycopg2://postgres:projetdata@localhost:5432/loyers_db"
DB_NAME = "loyers_db"

# --- Charger le CSV dans un DataFrame ---
df = pd.read_csv(CSV_PATH, sep=';', encoding='utf-8')

# --- Créer l'engine SQLAlchemy ---
engine = create_engine(DB_URL)

# --- Supprimer les anciennes données dans la table 'loyers' ---
with engine.connect() as connection:
    # Utilisation de 'text' pour envoyer la requête SQL
    connection.execute(text("TRUNCATE TABLE loyers RESTART IDENTITY CASCADE;"))
    print("✅ Anciennes données supprimées de la table 'loyers'.")

# --- Insérer les nouvelles données dans la table 'loyers' ---
df.to_sql('loyers', engine, if_exists='replace', index=False)

print("✅ Données importées dans la table 'loyers'")