import os
import folium
import pandas as pd
from dash import html
from sqlalchemy import create_engine
import requests

# -------------------------------
# 🔹 Connexion à la base de données (SQLite)
# -------------------------------
DB_URL = "sqlite:///loyers.db"   # <-- SQLite

engine = create_engine(DB_URL)

# -------------------------------
# 🔹 Charger les données depuis la base de données
# -------------------------------
def load_data_from_db():
    """Récupère les données depuis loyers.db"""
    query = 'SELECT "DEP", "loypredm2", "latitude", "longitude" FROM loyers WHERE "loypredm2" IS NOT NULL'
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

df = load_data_from_db()

# Vérif colonnes indispensables
LOYER_COL = "loypredm2"
LAT_COL, LON_COL = "latitude", "longitude"

# -------------------------------
# 🔹 Moyenne des loyers par département
# -------------------------------
df_dep = df.groupby("DEP", as_index=False)["loypredm2"].mean()

# -------------------------------
# 🔹 Télécharger les frontières géographiques (GeoJSON)
# -------------------------------
geo_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
response = requests.get(geo_url)

if response.status_code != 200:
    raise Exception(f"Erreur lors du téléchargement du GeoJSON ({response.status_code})")

geo_json = response.json()

# -------------------------------
# 🔹 Créer la carte Folium
# -------------------------------
def generate_map():
    m = folium.Map(location=[46.6, 2.5], zoom_start=6, tiles="OpenStreetMap")
    
    # Choroplèthe
    folium.Choropleth(
        geo_data=geo_json,
        name="Loyers moyens",
        data=df_dep,
        columns=["DEP", "loypredm2"],
        key_on="feature.properties.code",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Loyer moyen au m² (€)",
        highlight=True
    ).add_to(m)
    
    # Tooltip simple
    folium.GeoJson(
        geo_json,
        name="Départements",
        style_function=lambda x: {"fillColor": "transparent", "color": "transparent", "weight": 0},
        tooltip=folium.GeoJsonTooltip(
            fields=["nom"],
            aliases=["Département :"],
            labels=True,
            sticky=True
        )
    ).add_to(m)

    # Ajouter loyer moyen dans le GeoJSON
    for _, row in df_dep.iterrows():
        dep_code = row['DEP']
        value = round(row['loypredm2'], 2)

        for feature in geo_json["features"]:
            if feature["properties"]["code"] == dep_code:
                feature["properties"]["loypredm2"] = f"{value} €/m²"

    # Tooltip avancé
    folium.GeoJson(
        geo_json,
        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "transparent",
            "weight": 0,
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["nom", "loypredm2"],
            aliases=["Département :", "Loyer moyen :"],
            localize=True,
            sticky=True,
            labels=True
        )
    ).add_to(m)

    # Sauvegarde carte
    stamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    map_path = os.path.join("assets", f"map_loyers_par_dep_{stamp}.html")
    m.save(map_path)

    return map_path

# -------------------------------
# 🔹 Layout de la page carte
# -------------------------------
layout = html.Div([
    html.H1("Carte des loyers par département", style={"textAlign": "center"}),

    html.Iframe(
        src=f"/assets/{generate_map().split('/')[-1]}",
        style={"width": "100%", "height": "600px", "border": "none"}
    ),
])
