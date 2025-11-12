import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests  # <-- nouveau pour le téléchargement

# Répertoires et constantes
RAW_DIR = "data/raw"
OUT_DIR = "outputs"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# URL publique des données (à adapter selon ton jeu de données)
DATA_URL = "https://www.data.gouv.fr/fr/datasets/r/34434cef-2f85-43b9-a601-c625ee426cb7"  # exemple Air Quality
DATA_PATH = os.path.join(RAW_DIR, "pred-mai-mef-dhup.csv")


def download_data(url=DATA_URL, dest_path=DATA_PATH):
    """Télécharge les données depuis une ressource publique et les stocke dans data/raw."""
    if os.path.exists(dest_path):
        print(f"Fichier déjà présent : {dest_path}")
        return dest_path

    print(f"Téléchargement des données depuis {url} ...")
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        raise Exception(f"Erreur HTTP {response.status_code} lors du téléchargement.")
    
    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"Données téléchargées et sauvegardées dans : {dest_path}")
    return dest_path

def main():
    download_data()

if __name__ == "__main__":
    main()