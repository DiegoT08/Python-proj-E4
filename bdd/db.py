# db.py
from sqlalchemy import create_engine
import pandas as pd

# Configuration de la connexion PostgreSQL
DB_URL = "postgresql+psycopg2://mateo:projetdata@localhost:5432/loyers_db"

# Création de l'engine SQLAlchemy
engine = create_engine(DB_URL)

def get_data():
    """Récupère toutes les données de la table 'loyers'"""
    query = "SELECT * FROM loyers"
    return pd.read_sql(query, engine)