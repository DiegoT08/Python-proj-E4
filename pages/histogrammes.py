from dash import html
import os

# Chemin vers les images
assets_path = "assets"
images = [f for f in os.listdir(assets_path) if f.lower().endswith(".png")]

# Fonction pour tronquer les noms trop longs
def truncate_name(name, max_len=20):
    if len(name) > max_len:
        return name[:max_len-3] + "..."  # ajoute "..."
    return name

# Layout de la page
layout = html.Div([
    html.H1("Histogrammes et visuels"),

    html.Div(
        children=[
            html.Div(
                className="card",
                children=[
                    html.Img(src=f"/assets/{img}"),
                    html.H4(truncate_name(img.split(".")[0]))
                ]
            )
            for img in images
        ],
        className="image-grid"
    )
])