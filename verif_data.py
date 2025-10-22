# --- Installation (décommenter si nécessaire dans un terminal) ---
# pip install pandas matplotlib geopandas folium

# --- Import & chargement ---
import pandas as pd
import os

# Déterminer le chemin absolu vers le dossier data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned", "pred-mai-mef-dhup_clean.csv")

# Charger le CSV
df = pd.read_csv(DATA_PATH, sep=';')  # charge d'abord tout en str pour contrôle
print("Fichier chargé : {} lignes, {} colonnes".format(len(df), df.shape[1]))

# Afficher un aperçu (convertir l'affichage pour voir les vraies valeurs)
pd.set_option('display.max_columns', None)
print(df.head(10))

# --- Conversion des colonnes numériques attendues ---
num_cols = ["loypredm2", "lwr_IPm2", "upr_IPm2", "nbobs_com", "nbobs_mail", "R2_adj"]

for c in num_cols:
    if c in df.columns:
        # Si la colonne est déjà numérique → on laisse comme ça
        if pd.api.types.is_numeric_dtype(df[c]):
            continue
        # Sinon on convertit en numérique après avoir remplacé la virgule par un point
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '.'), errors='coerce')

# Vérification finale
print("\n✅ Conversion des colonnes numériques effectuée.")
print(df[num_cols].dtypes)

# Vérifier le type et descripteurs rapides
print("\nInfos générales :")
print(df.info())

print("\nStatistiques descriptives (colonnes numériques détectées) :")
print(df[num_cols].describe())

# --- Vérifications utiles ---
# 1) Nombre d'observations effectives
n_obs = len(df)
print(f"\nNombre total d'observations : {n_obs}")

# 2) Combien de valeurs manquantes dans les colonnes numériques
print("\nValeurs manquantes par colonne numérique :")
print(df[num_cols].isna().sum())

# 3) Vérifier format des codes INSEE (s'il existe) : convertir en chaîne 5 caractères (zfill)
if "INSEE_C" in df.columns:
    # nettoyer espaces et transformer en string
    df["INSEE_C"] = df["INSEE_C"].astype(str).str.strip()
    # afficher quelques valeurs uniques / exemples
    print("\nExemples de INSEE_C :")
    print(df["INSEE_C"].unique()[:10])
    # compter les doublons éventuels
    n_unique_insee = df["INSEE_C"].nunique()
    print(f"Nombre de INSEE_C uniques : {n_unique_insee}")
    if n_unique_insee < n_obs:
        print("Attention : il y a des doublons sur INSEE_C (plusieurs lignes pour une même commune).")

# 4) Vérifier la colonne TYPPRED
if "TYPPRED" in df.columns:
    print("\nValeurs distinctes dans TYPPRED :")
    print(df["TYPPRED"].value_counts())

# Sauvegarde d'un fichier nettoyé (utile pour l'étape carte)
df.to_csv("ton_fichier_nettoye.csv", index=False, sep=';')
print("\nFichier nettoyé sauvé sous 'ton_fichier_nettoye.csv' (formats normalisés).")