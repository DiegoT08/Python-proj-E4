import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
import psycopg2

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Configuration de la connexion PostgreSQL en utilisant les variables d'environnement
DB_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
DB_NAME = os.getenv('DB_NAME')
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
            dbname="postgres", user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'), port=os.getenv('DB_PORT')
        )
        connection.autocommit = True
        cursor = connection.cursor()

        # Créer la base de données si elle n'existe pas
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print(f"Base de données '{DB_NAME}' créée avec succès.")
        else:
            print(f"La base de données '{DB_NAME}' existe déjà.")

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Erreur lors de la création de la base de données : {e}")

# Fonction pour créer la table 'loyers' si elle n'existe pas
def create_table():
    try:
        # Connexion à la base de données loyers_db
        engine_db = create_engine(DB_URL)
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