import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# === Paramètres ===
DB_URL = "sqlite:///loyers.db"   # <-- SQLite au lieu de PostgreSQL
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# === Connexion à la base de données ===
def load_data_from_db():
    """Récupère les données depuis loyers.db"""
    query = "SELECT * FROM loyers"
    engine = create_engine(DB_URL)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df = load_data_from_db()

# === Nettoyage de la colonne des loyers ===
df = df[df["loypredm2"].notna()]
df = df[df["loypredm2"] > 0]
df = df[df["loypredm2"] < 60]  # coupe les extrêmes (valeurs aberrantes)

# === Tracé de l'histogramme ===
plt.figure(figsize=(10, 6))
sns.histplot(df["loypredm2"], bins=40, kde=True, color="#3182bd")

plt.title("Distribution des loyers moyens au m² en France", fontsize=16, fontweight='bold')
plt.xlabel("Loyer moyen au m² (€)", fontsize=13)
plt.ylabel("Nombre de communes", fontsize=13)
plt.grid(True, alpha=0.3)
plt.xlim(0, 25)

# === Sauvegarde ===
output_path = os.path.join(OUT_DIR, "histogramme_loyer_moyen.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ Histogramme enregistré dans {output_path}")