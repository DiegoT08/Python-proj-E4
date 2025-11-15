import os
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

# DATABASE = fichier local SQLite
DB_FILE = "loyers.db"
DB_URL = f"sqlite:///{DB_FILE}"

# Engine SQLite
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

# Structure de la table
class Loyers(Base):
    __tablename__ = "loyers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    LIBGEO = Column(String)
    loypredm2 = Column(Float)
    latitude = Column(Float)
    longitude = Column(Float)
    DEP = Column(String)

# Créer la base + table
def create_database_and_table():
    Base.metadata.create_all(engine)
    print("✅ Base SQLite 'loyers.db' créée avec la table 'loyers'.")

if __name__ == "__main__":
    create_database_and_table()