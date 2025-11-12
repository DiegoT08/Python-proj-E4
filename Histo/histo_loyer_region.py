# ...existing code...
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Paramètres ===
DATA_PATH = "data/cleaned/pred-mai-mef-dhup_clean.csv"
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# === Chargement des données ===
def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} introuvable. Copiez le CSV dans le dossier data/")
    df = pd.read_csv(path, sep=';', encoding='utf-8', low_memory=False)
    return df

df = load_data(DATA_PATH)

# === Dictionnaire de correspondance code -> nom de région ===
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

# Supprime les lignes avec région non reconnue (au cas où)
df = df[df["REGION_NOM"].notna()]

# === Calcul du loyer moyen par région ===
df_region = df.groupby("REGION_NOM")["loypredm2"].mean().reset_index().sort_values("loypredm2", ascending=False)

# === Tracé du graphique ===
plt.figure(figsize=(12, 6))
ax = sns.barplot(
    data=df_region,
    x="loypredm2",
    y="REGION_NOM",
    hue="REGION_NOM",     # assigne y à hue pour éviter la dépréciation
    dodge=False,          # empile/overlay pour n'avoir qu'une barre par région
    palette="Blues_r"
)

# Supprime la légende (effet identique à l'ancien passage de palette sans hue)
if ax.get_legend() is not None:
    ax.get_legend().remove()

plt.title("Loyer moyen au m² par région en France (2023)", fontsize=16, fontweight='bold')
plt.xlabel("Loyer moyen au m² (€)", fontsize=13)
plt.ylabel("Région", fontsize=13)
plt.grid(axis='x', alpha=0.3)

# === Sauvegarde et affichage ===
output_path = os.path.join(OUT_DIR, "loyer_moyen_par_region.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"✅ Graphique enregistré dans {output_path}")
