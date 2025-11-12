# histogrammes.py
from dash import html
import os

# Chemin vers le dossier des images
assets_path = "assets"
# On définit un ordre précis pour les images
images_order = [
    "histogramme_loyer_moyen.png",
    "loyer_paris_arrondissements.png",
]

# Légendes explicatives pour chaque image
legendes = {
    "histogramme_loyer_moyen.png": "Histogramme : Distribution des loyers prédits par commune. Montre comment les loyers sont répartis sur toutes les communes.",
    "loyer_paris_arrondissements.png": "Boxplot : Variation des loyers selon le type de maille. Permet de comparer les loyers entre différents types de prédictions.",
}

# Layout de la page
layout = html.Div([
    html.H1("Visualisation des histogrammes et graphiques"),

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
            for img in images_order if os.path.exists(os.path.join(assets_path, img))
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