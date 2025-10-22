import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Définir le chemin du fichier nettoyé ---
cleaned_path = "ton_fichier_nettoye.csv"

# --- Vérification de l'existence du fichier ---
if not os.path.exists(cleaned_path):
    raise FileNotFoundError(f"❌ Fichier non trouvé : {cleaned_path}. Lance d'abord verif_data.py pour le créer.")

# --- Chargement du fichier nettoyé ---
df = pd.read_csv(cleaned_path, sep=';')
print(f"Fichier chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print("Colonnes :", df.columns.tolist())

# --- Créer un dossier de sortie pour les graphiques ---
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# --- Histogramme du loyer prédictif ---
plt.figure(figsize=(8, 5))
plt.hist(df["loypredm2"], bins=50, edgecolor='black')
plt.title("Distribution des loyers prédictifs au m²")
plt.xlabel("Loyer prédit (€/m²)")
plt.ylabel("Nombre de communes")
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "hist_loypredm2.png"))
plt.close()

# --- Boxplot selon le type de prédiction ---
plt.figure(figsize=(8, 5))
df.boxplot(column="loypredm2", by="TYPPRED", grid=False)
plt.title("Loyer prédictif (€/m²) selon le type de maille")
plt.suptitle("")
plt.xlabel("Type de prédiction")
plt.ylabel("Loyer prédit (€/m²)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "boxplot_typpred.png"))
plt.close()

print(f"Graphiques sauvegardés dans le dossier : {output_dir}")