import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# --- Paramètres ---
CSV_PATH = "data/cleaned/pred-mai-mef-dhup_clean_coords.csv"  # Remplacez par le chemin de votre fichier CSV
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
DB_NAME = os.getenv('DB_NAME')

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