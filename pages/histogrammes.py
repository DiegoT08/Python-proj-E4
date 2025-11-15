from dash import html
import os

# Chemin vers le dossier des images
assets_path = "assets"

# On définit un ordre précis pour les images (tous les fichiers d'histogrammes)
images_order = [
    "hist_littoral_vs_nonlittoral.png",
    "hist_ratio_loyer_dep.png",
    "histogramme_loyer_moyen.png",
    "loyer_moyen_par_region.png",
    "loyer_paris_arrondissements.png"
]

# Légendes explicatives pour chaque image
legendes = {
    "hist_littoral_vs_nonlittoral.png": "Histogramme : Loyer moyen dans les départements littoraux et non littoraux.",
    "hist_ratio_loyer_dep.png": "Histogramme : Distribution du ratio communal / moyenne départementale des loyers.",
    "histogramme_loyer_moyen.png": "Histogramme : Distribution des loyers moyens au m² en France.",
    "loyer_moyen_par_region.png": "Graphique : Loyer moyen par région en France.",
    "loyer_paris_arrondissements.png": "Graphique : Loyer moyen par arrondissement à Paris."
}

# Layout de la page
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
            for img in images_order if os.path.exists(os.path.join(assets_path, img))  # Vérifie si l'image existe dans le dossier assets
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