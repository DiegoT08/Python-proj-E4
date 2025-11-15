import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# === Paramètres ===
DB_URL = "postgresql+psycopg2://postgres:projetdata@localhost:5432/loyers_db"
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
df = df[df["loypredm2"].notna()]
df = df[df["loypredm2"] > 0]
df = df[df["loypredm2"] < 60]  # coupe les valeurs aberrantes

# === Vérification colonne DEP ===
if "DEP" not in df.columns:
    raise KeyError("Colonne 'DEP' manquante dans le dataset.")
df["DEP"] = df["DEP"].astype(str).str.zfill(2)  # uniformisation (ex: '6' -> '06')

# === Calcul de la moyenne départementale ===
dept_mean = df.groupby("DEP")["loypredm2"].transform("mean")

# === Calcul du ratio communal / moyenne départementale ===
df["ratio_dep"] = df["loypredm2"] / dept_mean

# === Nettoyage du ratio (suppression des divisions nulles / inf) ===
df = df.replace([np.inf, -np.inf], np.nan)
df = df[df["ratio_dep"].notna()]

# === Statistiques descriptives pour annotation ===
mean_ratio = df["ratio_dep"].mean()
median_ratio = df["ratio_dep"].median()
std_ratio = df["ratio_dep"].std()

# === Style graphique ===
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10,6))

# === Histogramme ===
sns.histplot(
    df["ratio_dep"],
    bins=50,
    color="#2c7fb8",
    kde=True,
    edgecolor=None,
    alpha=0.8
)

# === Lignes de repère ===
plt.axvline(1, color="red", linestyle="--", linewidth=2, label="Ratio = 1 (moyenne départementale)")
plt.axvline(mean_ratio, color="orange", linestyle="--", linewidth=1.5, label=f"Moyenne nationale ({mean_ratio:.2f})")
plt.axvline(median_ratio, color="green", linestyle=":", linewidth=1.5, label=f"Médiane ({median_ratio:.2f})")

# === Titres et légendes ===
plt.title("Distribution du ratio communal / moyenne départementale des loyers", fontsize=14, fontweight="bold")
plt.xlabel("Ratio (loyer communal / moyenne départementale)", fontsize=12)
plt.ylabel("Nombre de communes", fontsize=12)
plt.xlim(0.5, 1.8)
plt.legend()
plt.grid(True, alpha=0.3)

# === Sauvegarde ===
output_path = os.path.join(OUT_DIR, "hist_ratio_loyer_dep.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ Histogramme enregistré dans {output_path}")
print(f"Moyenne du ratio : {mean_ratio:.3f} | Médiane : {median_ratio:.3f} | Écart-type : {std_ratio:.3f}")
