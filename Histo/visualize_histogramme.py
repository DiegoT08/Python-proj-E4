import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dash import html

# Dossier de sortie pour les images
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

# === Connexion à la base de données ===
DB_URL = "postgresql+psycopg2://postgres:projetdata@localhost:5432/loyers_db"

def load_data_from_db():
    """Récupère les données de la table 'loyers' depuis la base de données"""
    query = "SELECT * FROM loyers"
    engine = create_engine(DB_URL)
    df = pd.read_sql(query, engine)
    return df

# === Fonction d'affichage de tous les histogrammes ===
def display_histograms():
    images_order = [
        "hist_littoral_vs_nonlittoral.png",
        "hist_ratio_loyer_dep.png",
        "histogramme_loyer_moyen.png",
        "loyer_moyen_par_region.png",
        "loyer_paris_arrondissements.png"
    ]

    legendes = {
        "hist_littoral_vs_nonlittoral.png": "Histogramme : Loyer moyen dans les départements littoraux et non littoraux.",
        "hist_ratio_loyer_dep.png": "Histogramme : Distribution du ratio communal / moyenne départementale des loyers.",
        "histogramme_loyer_moyen.png": "Histogramme : Distribution des loyers moyens au m² en France.",
        "loyer_moyen_par_region.png": "Graphique : Loyer moyen par région en France.",
        "loyer_paris_arrondissements.png": "Graphique : Loyer moyen par arrondissement à Paris."
    }

    layout = html.Div([
        html.H1("Visualisation des histogrammes et graphiques", style={"textAlign": "center"}),

        html.Div(
            children=[
                html.Div(
                    style={
                        "margin": "20px",
                        "textAlign": "center",
                        "width": "80%"
                    },
                    children=[
                        html.Img(
                            src=f"/assets/{img}",
                            style={"width": "100%", "height": "auto", "border": "1px solid #ccc", "border-radius": "5px"}
                        ),
                        html.P(
                            legendes.get(img, "Aucune description disponible."),
                            style={"marginTop": "10px", "fontStyle": "italic", "fontSize": "14px"}
                        )
                    ]
                )
                for img in images_order if os.path.exists(os.path.join(OUT_DIR, img))
            ],
            style={
                "height": "80vh",          # hauteur du conteneur
                "overflowY": "auto",       # défilement vertical
                "padding": "10px",
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center"
            }
        )
    ])

    return layout

# --- Main code ---
def main():
    df = load_data_from_db()  # Utilisation de la base de données au lieu du fichier CSV
    print(f"✅ Toutes les figures sauvegardées dans {OUT_DIR}")

if __name__ == "__main__":
    main()