import os
from sqlalchemy import create_engine, Table, Column, Integer, Float, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import psycopg2

# Configuration de la connexion PostgreSQL
DB_URL = "postgresql+psycopg2://postgres:projetdata@localhost:5432/loyers_db"
DB_NAME = "loyers_db"
engine = create_engine(DB_URL)
Base = declarative_base()

# Définir la structure de la table
class Loyers(Base):
    __tablename__ = 'loyers'

    id = Column(Integer, primary_key=True)
    LIBGEO = Column(String)
    loypredm2 = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    DEP = Column(String)

# Fonction pour créer la base de données si elle n'existe pas
def create_database():
    try:
        # Connexion à PostgreSQL pour créer la base de données
        connection = psycopg2.connect(
            dbname="postgres", user="postgres", password="projetdata", host="localhost", port="5432"
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Créer la base de données si elle n'existe pas
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'loyers_db'")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('CREATE DATABASE loyers_db')
            print("Base de données 'loyers_db' créée avec succès.")
        else:
            print("La base de données 'loyers_db' existe déjà.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {e}")

# Fonction pour créer la table 'loyers' si elle n'existe pas
def create_table():
    try:
        # Connexion à la base de données loyers_db
        engine_db = create_engine(f"postgresql+psycopg2://postgres:projetdata@localhost:5432/{DB_NAME}")
        Base.metadata.create_all(engine_db)
        print("Table 'loyers' créée avec succès.")
    except OperationalError as e:
        print(f"Erreur lors de la création de la table : {e}")

# Fonction pour vérifier et créer la base de données et la table
def check_and_create_db():
    create_database()  # Créer la base de données si nécessaire
    create_table()     # Créer la table 'loyers' si nécessaire

# Appel de la fonction pour vérifier et créer la base de données et la table
if __name__ == "__main__":
    check_and_create_db()