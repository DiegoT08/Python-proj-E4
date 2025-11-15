import os
import folium
import pandas as pd
from dash import html
from sqlalchemy import create_engine
import requests

# -------------------------------
# 🔹 Connexion à la base de données
# -------------------------------
DB_URL = "postgresql+psycopg2://mateo:projetdata@localhost:5432/loyers_db"
engine = create_engine(DB_URL)

# -------------------------------
# 🔹 Charger les données depuis la base de données
# -------------------------------
def load_data_from_db():
    """Récupère les données de la table 'loyers' depuis la base de données"""
    query = 'SELECT "DEP", "loypredm2", "latitude", "longitude" FROM loyers WHERE "loypredm2" IS NOT NULL'
    df = pd.read_sql(query, engine)
    return df

df = load_data_from_db()

# 🔹 Vérifie que lat/lon existent dans ton CSV
LOYER_COL = "loypredm2"  # à adapter si besoin
LAT_COL, LON_COL = "latitude", "longitude"

# -------------------------------
# 🔹 Calcul de la moyenne des loyers par département
# -------------------------------
df_dep = df.groupby("DEP", as_index=False)["loypredm2"].mean()

# -------------------------------
# 🔹 Télécharger les frontières géographiques (GeoJSON) pour les départements
# -------------------------------
geo_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
response = requests.get(geo_url)
if response.status_code != 200:
    raise Exception(f"Erreur lors du téléchargement du GeoJSON ({response.status_code})")
geo_json = response.json()

# -------------------------------
# 🔹 Créer la carte Folium avec les départements et leurs loyers moyens
# -------------------------------
def generate_map():
    # Créer la carte
    m = folium.Map(location=[46.6, 2.5], zoom_start=6, tiles="OpenStreetMap")
    
    # Ajouter la couche choroplèthe avec la moyenne des loyers par département
    folium.Choropleth(
        geo_data=geo_json,
        name="Loyers moyens",
        data=df_dep,
        columns=["DEP", "loypredm2"],
        key_on="feature.properties.code",
        fill_color="YlOrRd",   # Jaune vers rouge
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name="Loyer moyen au m² (€)",
        highlight=True
    ).add_to(m)
    
    # Ajouter un tooltip pour chaque département avec son loyer moyen
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

    # On ajoute aussi le loyer moyen pour chaque département dans un autre tooltip
    for _, row in df_dep.iterrows():
        dep_code = row['DEP']
        value = round(row['loypredm2'], 2)
        
        # On cherche la géométrie correspondante dans le GeoJSON
        for feature in geo_json["features"]:
            if feature["properties"]["code"] == dep_code:
                feature["properties"]["loypredm2"] = f"{value} €/m²"

    # Tooltip avec nom + valeur
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
    
    # Sauvegarder la carte dans un fichier HTML
    stamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    map_path = os.path.join("assets", f"map_loyers_par_dep_{stamp}.html")
    m.save(map_path)

    return map_path

# -------------------------------
# 🔹 Layout de la page carte
# -------------------------------
layout = html.Div([
    html.H1("Carte des loyers par département", style={"textAlign": "center"}),

    # Affichage direct de la carte dans un Iframe
    html.Iframe(
        src=f"/assets/{generate_map().split('/')[-1]}",  # Génère la carte et récupère le nom du fichier
        style={"width": "100%", "height": "600px", "border": "none"}
    ),
])