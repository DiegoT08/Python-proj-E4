from dash import html, dcc, dash_table
import pandas as pd
import os
import folium
from sqlalchemy import create_engine

# -------------------------------
# 🔹 Connexion à la base de données (SQLite)
# -------------------------------
DB_URL = "sqlite:///loyers.db"   # <-- SQLite remplace PostgreSQL
engine = create_engine(DB_URL)

# -------------------------------
# 🔹 Chargement des données
# -------------------------------
def load_data_from_db():
    """Récupère les données depuis loyers.db"""
    query = 'SELECT "LIBGEO", "loypredm2", "latitude", "longitude" FROM loyers'
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df = load_data_from_db()

# 🔹 Vérifie le bon nom de la colonne du loyer
LOYER_COL = "loypredm2"

# 🔹 Vérifie les colonnes lat/lon
LAT_COL, LON_COL = "latitude", "longitude"

# -------------------------------
# 🔹 Création des classements
# -------------------------------
top10 = df.nlargest(10, LOYER_COL)[["LIBGEO", LOYER_COL, LAT_COL, LON_COL]]
bottom10 = df.nsmallest(10, LOYER_COL)[["LIBGEO", LOYER_COL, LAT_COL, LON_COL]]

# -------------------------------
# 🔹 Création de la carte Folium
# -------------------------------
m = folium.Map(location=[46.6, 2.2], zoom_start=6)

# 🔹 Points du Top 10 (rouge)
for _, row in top10.iterrows():
    if pd.notna(row[LAT_COL]) and pd.notna(row[LON_COL]):
        folium.Marker(
            location=[row[LAT_COL], row[LON_COL]],
            popup=f"{row['LIBGEO']} - {row[LOYER_COL]} €/m²",
            icon=folium.Icon(color="red")
        ).add_to(m)

# 🔹 Points du Bottom 10 (bleu)
for _, row in bottom10.iterrows():
    if pd.notna(row[LAT_COL]) and pd.notna(row[LON_COL]):
        folium.Marker(
            location=[row[LAT_COL], row[LON_COL]],
            popup=f"{row['LIBGEO']} - {row[LOYER_COL]} €/m²",
            icon=folium.Icon(color="blue")
        ).add_to(m)

# -------------------------------
# 🔹 Sauvegarder la carte
# -------------------------------
map_path = os.path.join("assets", "map_classement.html")
m.save(map_path)

# -------------------------------
# 🔹 Layout Dash
# -------------------------------
layout = html.Div([
    html.H1("Classement des loyers en France", style={"textAlign": "center"}),

    html.H2("Top 10 - Loyers les plus élevés", style={"textAlign": "center"}),
    dash_table.DataTable(
        data=top10[["LIBGEO", LOYER_COL]].to_dict("records"),
        columns=[{"name": col, "id": col} for col in ["LIBGEO", LOYER_COL]],
        style_table={"width": "60%", "margin": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#f2f2f2"}
    ),

    html.Br(),

    html.H2("Top 10 - Loyers les plus faibles", style={"textAlign": "center"}),
    dash_table.DataTable(
        data=bottom10[["LIBGEO", LOYER_COL]].to_dict("records"),
        columns=[{"name": col, "id": col} for col in ["LIBGEO", LOYER_COL]],
        style_table={"width": "60%", "margin": "auto"},
        style_cell={"textAlign": "center", "padding": "8px"},
        style_header={"fontWeight": "bold", "backgroundColor": "#f2f2f2"}
    ),

    html.Br(),
    html.H2("Carte des villes du Top 10 et Bottom 10", style={"textAlign": "center"}),

    html.Iframe(
        src="/assets/map_classement.html",
        style={"width": "100%", "height": "600px", "border": "none"}
    )
])
