import os
import pandas as pd
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

# === Dictionnaire code → nom de région ===
regions = {
    11: "Île-de-France",
    24: "Centre-Val de Loire",
    27: "Bourgogne-Franche-Comté",
    28: "Normandie",
    32: "Hauts-de-France",
    44: "Grand Est",
    52: "Pays de la Loire",
    53: "Bretagne",
    75: "Nouvelle-Aquitaine",
    76: "Occitanie",
    84: "Auvergne-Rhône-Alpes",
    93: "Provence-Alpes-Côte d’Azur",
    94: "Corse"
}

# === Nettoyage et préparation ===
df = df[df["loypredm2"].notna()]
df = df[df["REG"].notna()]
df["REG"] = df["REG"].astype(int)
df["REGION_NOM"] = df["REG"].map(regions)

df = df[df["REGION_NOM"].notna()]  # Sécurité

# === Calcul du loyer moyen régional ===
df_region = (
    df.groupby("REGION_NOM")["loypredm2"]
    .mean()
    .reset_index()
    .sort_values("loypredm2", ascending=False)
)

# === Graphique ===
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    data=df_region,
    x="loypredm2",
    y="REGION_NOM",
    hue="REGION_NOM",   # oblige seaborn à distinguer chaque barre
    dodge=False,
    palette="Blues_r"
)

# Supprimer la légende inutile
legend = ax.get_legend()
if legend is not None:
    legend.remove()

plt.title("Loyer moyen au m² par région en France (2023)", fontsize=16, fontweight='bold')
plt.xlabel("Loyer moyen au m² (€)", fontsize=13)
plt.ylabel("Région", fontsize=13)
plt.grid(axis='x', alpha=0.3)

# === Sauvegarde ===
output_path = os.path.join(OUT_DIR, "loyer_moyen_par_region.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"✅ Graphique enregistré dans {output_path}")
