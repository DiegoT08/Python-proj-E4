from dash import html, dash_table
import pandas as pd
import folium
from datetime import datetime

# Charger les données
DATA_PATH = "data/cleaned/pred-mai-mef-dhup_clean_coords.csv"
df = pd.read_csv(DATA_PATH, sep=';')

LOYER_COL = "loypredm2"

# Top 10 et Bottom 10
top10 = df.nlargest(10, LOYER_COL)[["LIBGEO", LOYER_COL, "latitude", "longitude"]]
bottom10 = df.nsmallest(10, LOYER_COL)[["LIBGEO", LOYER_COL, "latitude", "longitude"]]

# Combiner pour carte
top_bottom = pd.concat([top10, bottom10], ignore_index=True)

# Créer la carte Folium
m = folium.Map(location=[46.6, 2.5], zoom_start=6, tiles="OpenStreetMap")
for _, row in top_bottom.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"{row['LIBGEO']}<br>{LOYER_COL}: {row[LOYER_COL]:.2f} €/m²",
        tooltip=row['LIBGEO']
    ).add_to(m)

# Layout Dash
layout = html.Div([
    html.H1("Classement des villes par loyers", style={"textAlign": "center"}),

    # Conteneur des deux tableaux côte à côte
    html.Div([
        html.Div([
            html.H2("Top 10 - Loyers les plus élevés", style={"textAlign": "center"}),
            dash_table.DataTable(
                id="table-top10",
                data=top10.to_dict("records"),
                columns=[{"name": "Ville", "id": "LIBGEO"}, {"name": "Loyer (€/m²)", "id": LOYER_COL}],
                style_table={"width": "100%"},
                style_cell={"textAlign": "center", "padding": "8px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f2f2f2"}
            )
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H2("Top 10 - Loyers les plus faibles", style={"textAlign": "center"}),
            dash_table.DataTable(
                id="table-bottom10",
                data=bottom10.to_dict("records"),
                columns=[{"name": "Ville", "id": "LIBGEO"}, {"name": "Loyer (€/m²)", "id": LOYER_COL}],
                style_table={"width": "100%"},
                style_cell={"textAlign": "center", "padding": "8px"},
                style_header={"fontWeight": "bold", "backgroundColor": "#f2f2f2"}
            )
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "marginLeft": "4%"})
    ], style={"width": "90%", "margin": "0 auto"}),

    html.Br(),

    # Carte Folium
    html.Iframe(
        srcDoc=m.get_root().render(),
        width="80%",
        height="500",
        style={"margin": "0 auto", "display": "block"}
    )
])