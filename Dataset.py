# dataset.py
import os
import pandas as pd
import numpy as np

DATA_PATH = "data/cleaned/pred-mai-mef-dhup_clean.csv"

def load_data(path=DATA_PATH):
    """Charge le dataset nettoyé et retourne un DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} introuvable. Vérifie que le CSV est présent dans data/cleaned/")
    df = pd.read_csv(path, sep=';', encoding='utf-8', low_memory=False)
    return df

def summary(df):
    """Affiche résumé du dataset et valeurs manquantes."""
    print("Shape:", df.shape)
    print("\nColonnes et types:\n", df.dtypes)
    print("\nAperçu:\n", df.head())
    print("\nStatistiques descriptives:\n", df.describe(include='all').T)
    missing = df.isna().sum()
    print("\nValeurs manquantes par colonne:\n", missing[missing>0])

def select_numeric(df):
    """Retourne uniquement les colonnes numériques utiles pour l'analyse."""
    cols = ["loypredm2", "nbobs_com", "nbobs_mail", "R2_adj"]
    numeric_cols = [c for c in cols if c in df.columns]
    return df[numeric_cols]

if __name__ == "__main__":
    df = load_data()
    summary(df)