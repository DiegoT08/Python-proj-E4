import os
import pandas as pd

# Répertoires
RAW_DIR = "data/raw"
CLEAN_DIR = "data/cleaned"
os.makedirs(CLEAN_DIR, exist_ok=True)

# Fichiers
RAW_FILE = os.path.join(RAW_DIR, "pred-mai-mef-dhup.csv")
CLEAN_FILE = os.path.join(CLEAN_DIR, "pred-mai-mef-dhup_clean.csv")


def clean_data(raw_path=RAW_FILE, clean_path=CLEAN_FILE):
    """Nettoie les données brutes et les enregistre dans data/cleaned/"""
    print(f"Lecture du fichier brut : {raw_path}")

    # Lecture du CSV (séparateur ; et décimales avec ,)
    df = pd.read_csv(raw_path, sep=";", decimal=",", encoding="latin-1")

    print(f"Nombre de lignes avant nettoyage : {len(df)}")

    # Nettoyage des colonnes (ex : suppression d'espaces, renommage cohérent)
    df.columns = (
        df.columns.str.strip()
        .str.replace(" ", "_")
        .str.replace(".", "_")
        .str.replace("�", "é")  # gestion des caractères mal encodés
    )

    # Supprimer les doublons
    df = df.drop_duplicates()

    # Supprimer les lignes vides
    df = df.dropna(how="all")

    # Conversion des colonnes numériques (par sécurité)
    numeric_cols = [
        "loypredm2", "lwr_IPm2", "upr_IPm2", "nbobs_com", "nbobs_mail", "R2_adj"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", ".")
                .astype(float)
            )

    # Remplacement des caractères erronés dans les noms de villes
    df["LIBGEO"] = df["LIBGEO"].str.replace("�", "é")

    print(f"Nombre de lignes après nettoyage : {len(df)}")

    # Sauvegarde du fichier nettoyé
    df.to_csv(clean_path, index=False, sep=";", encoding="utf-8")
    print(f"Données nettoyées enregistrées dans : {clean_path}")

    return df


if __name__ == "__main__":
    clean_data()