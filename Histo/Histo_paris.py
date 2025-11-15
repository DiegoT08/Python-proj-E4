import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import re

# === Paramètres ===
DB_URL = "postgresql+psycopg2://mateo:projetdata@localhost:5432/loyers_db"
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# === Connexion à la base de données ===
def load_data_from_db():
    """Récupère les données de la table 'loyers' depuis la base de données"""
    query = "SELECT * FROM loyers"
    engine = create_engine(DB_URL)
    df = pd.read_sql(query, engine)
    return df

df = load_data_from_db()

# === Nettoyage de la colonne des loyers ===
# On retire les valeurs manquantes et aberrantes (loyers trop élevés ou négatifs)
df = df[df["loypredm2"].notna()]
df = df[df["loypredm2"] > 0]
df = df[df["loypredm2"] < 60]  # 60 €/m² : coupe les extrêmes (valeurs aberrantes)

# === Filtrer uniquement les arrondissements de Paris ===
df_paris = df[df["LIBGEO"].str.contains("PARIS", case=False, na=False)].copy()

# === Extraire le numéro d'arrondissement ===
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

# === Sauvegarde et affichage ===
output_path = os.path.join(OUT_DIR, "loyer_paris_arrondissements.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Graphique enregistré dans : {output_path}")