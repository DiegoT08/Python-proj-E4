import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import re

# === Paramètres ===
DB_URL = "sqlite:///loyers.db"   # <-- SQLite remplace PostgreSQL
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
df = df[df["loypredm2"] < 60]  # coupe les extrêmes

# === Filtrer uniquement les arrondissements de Paris ===
df_paris = df[df["LIBGEO"].str.contains("PARIS", case=False, na=False)].copy()

# === Extraire le numéro d’arrondissement ===
df_paris["Arrondissement"] = df_paris["LIBGEO"].apply(
    lambda x: re.findall(r"\d+", x)[0] if re.findall(r"\d+", x) else None
)
df_paris = df_paris.dropna(subset=["Arrondissement"])
df_paris["Arrondissement"] = df_paris["Arrondissement"].astype(int)

# === Calcul du loyer moyen par arrondissement ===
df_paris_moy = df_paris.groupby("Arrondissement")["loypredm2"].mean().reset_index()

# === Tracé du graphique ===
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_paris_moy.sort_values("Arrondissement"),
    x="Arrondissement",
    y="loypredm2",
    palette="coolwarm"
)

plt.title("Loyer moyen au m² par arrondissement à Paris", fontsize=15, fontweight="bold")
plt.xlabel("Arrondissement", fontsize=12)
plt.ylabel("Loyer moyen au m² (€)", fontsize=12)
plt.grid(True, axis="y", alpha=0.3)

# === Sauvegarde ===
output_path = os.path.join(OUT_DIR, "loyer_paris_arrondissements.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ Graphique enregistré dans : {output_path}")
