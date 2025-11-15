import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
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

# === Liste locale des départements littoraux ===
DEPARTEMENTS_LITTORAUX = [
    "06","13","14","17","22","29","30","33","34","35","40",
    "44","50","56","59","62","64","66","76","83","85"
]

# === Séparation des groupes ===
df_littoral = df[df["DEP"].astype(str).isin(DEPARTEMENTS_LITTORAUX)]
df_non_littoral = df[~df["DEP"].astype(str).isin(DEPARTEMENTS_LITTORAUX)]

# === Moyennes ===
mean_littoral = df_littoral["loypredm2"].mean()
mean_non_littoral = df_non_littoral["loypredm2"].mean()

# === STYLE GRAPHIQUE CLAIR ===
mpl.rcdefaults()               # Réinitialise toutes les configurations globales Matplotlib
plt.style.use("default")       # Supprime tout style global (comme dark_background)
sns.reset_orig()               # Réinitialise Seaborn à son état d'origine
sns.set_theme(style="whitegrid")

# Crée la figure avec fond blanc explicite
fig, ax = plt.subplots(figsize=(10, 6), facecolor="white")
ax.set_facecolor("white")

# === Histogrammes superposés ===
sns.histplot(
    df_littoral["loypredm2"],
    bins=35,
    color="#3182bd",
    label="Départements littoraux",
    alpha=0.5,
    kde=True,
    ax=ax
)
sns.histplot(
    df_non_littoral["loypredm2"],
    bins=35,
    color="#e6550d",
    label="Autres départements",
    alpha=0.4,
    kde=True,
    ax=ax
)

# === Lignes de moyenne ===
ax.axvline(mean_littoral, color="#3182bd", linestyle="--", linewidth=2)
ax.axvline(mean_non_littoral, color="#e6550d", linestyle="--", linewidth=2)

# === Annotations ===
ax.text(mean_littoral + 0.2, ax.get_ylim()[1]*0.8, f"μ Littoral = {mean_littoral:.2f} €",
        color="#3182bd", fontsize=10)
ax.text(mean_non_littoral + 0.2, ax.get_ylim()[1]*0.7, f"μ Autres = {mean_non_littoral:.2f} €",
        color="#e6550d", fontsize=10)

# === Titres et axes ===
ax.set_title("Distribution des loyers moyens au m²\nLittoral vs Non-Littoral (France 2023)",
             fontsize=14, fontweight="bold")
ax.set_xlabel("Loyer moyen au m² (€)", fontsize=12)
ax.set_ylabel("Nombre de communes", fontsize=12)
ax.legend(frameon=True)
plt.tight_layout()

# === Sauvegarde ===
output_path = os.path.join(OUT_DIR, "hist_littoral_vs_nonlittoral.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight", facecolor="white")  # <-- fond blanc forcé
print(f"✅ Histogramme littoral/non-littoral enregistré dans : {output_path}")