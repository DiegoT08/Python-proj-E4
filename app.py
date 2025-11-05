import os
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__, suppress_callback_exceptions=True)

# Chemin du dossier assets
assets_path = "assets"

# Liste tous les fichiers PNG dans assets/
images = [f for f in os.listdir(assets_path) if f.lower().endswith(".png")]

# Layout du dashboard
app.layout = html.Div(
    style={
        "fontFamily": "Helvetica, Arial, sans-serif",
        "backgroundColor": "#f5f6fa",
        "padding": "50px"
    },
    children=[
        html.H1(
            "Dashboard Professionnel des Histogrammes",
            style={
                "textAlign": "center",
                "color": "#2c3e50",
                "marginBottom": "50px",
                "fontWeight": "bold"
            }
        ),

        # Checklist pour sélectionner les images
        html.Div(
            dcc.Checklist(
                id="checklist-images",
                options=[{"label": img.split(".")[0], "value": img} for img in images],
                value=[images[0]] if images else [],
                labelStyle={"display": "inline-block", "marginRight": "20px", "fontSize": "16px"}
            ),
            style={"textAlign": "center", "marginBottom": "50px"}
        ),

        html.Div(
            id="images-container",
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))",
                "gap": "40px",
                "justifyItems": "center",
                "alignItems": "start",
                "maxHeight": "80vh",
                "overflowY": "auto",
                "padding": "10px"
            }
        )
    ]
)

# Callback pour afficher les images cochées
@app.callback(
    Output("images-container", "children"),
    Input("checklist-images", "value")
)
def update_images(selected_images):
    if not selected_images:
        return html.Div(
            "Aucune image sélectionnée",
            style={"color": "#7f8c8d", "fontStyle": "italic", "textAlign": "center", "fontSize": "18px"}
        )

    cards = []
    for img in selected_images:
        cards.append(
            html.Div(
                children=[
                    html.Img(
                        src=f"/assets/{img}",
                        title=img.split(".")[0],
                        style={
                            "width": "100%",
                            "borderRadius": "12px",
                            "boxShadow": "0 8px 16px rgba(0,0,0,0.2)",
                            "transition": "transform 0.3s, box-shadow 0.3s"
                        }
                    ),
                    html.H4(
                        img.split(".")[0],
                        style={"textAlign": "center", "marginTop": "10px", "color": "#34495e"}
                    )
                ],
                style={
                    "backgroundColor": "#fff",
                    "padding": "15px",
                    "borderRadius": "12px",
                    "width": "90%",
                    "textAlign": "center",
                    "cursor": "pointer",
                    "overflow": "hidden"
                },
                className="card"
            )
        )
    return cards

if __name__ == "__main__":
    app.run(debug=False)