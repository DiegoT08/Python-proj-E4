# pages/classement.py


from dash import html, dcc, dash_table
import pandas as pd
import os
import folium

# -------------------------------
# 🔹 Chargement des données
# -------------------------------
data_path = os.path.join("data", "cleaned", "pred-mai-mef-dhup_clean_coords.csv")
df = pd.read_csv(data_path, sep=";")

# 🔹 Vérifie le bon nom de la colonne du loyer
LOYER_COL = "loypredm2"  # à adapter si besoin

# 🔹 Vérifie que lat/lon existent dans ton CSV
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

# Ajoute les points du Top 10
for _, row in top10.iterrows():
    if pd.notna(row[LAT_COL]) and pd.notna(row[LON_COL]):
        folium.Marker(
            location=[row[LAT_COL], row[LON_COL]],
            popup=f"{row['LIBGEO']} - {row[LOYER_COL]} €/m²",
            icon=folium.Icon(color="red")
        ).add_to(m)

# Sauvegarde la carte dans /assets
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
    html.H2("Carte des villes du Top 10", style={"textAlign": "center"}),
    html.Iframe(
        src="/assets/map_classement.html",
        style={"width": "100%", "height": "600px", "border": "none"}
    )
])