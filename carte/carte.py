import pandas as pd
import folium
import requests
import json
from datetime import datetime
from sqlalchemy import create_engine

# === 1️⃣ Connexion à la base de données ===
DB_URL = "postgresql+psycopg2://mateo:projetdata@localhost:5432/loyers_db"
engine = create_engine(DB_URL)

# === 2️⃣ Charger les données depuis la base de données ===
query = "SELECT DEP, loypredm2 FROM loyers WHERE loypredm2 IS NOT NULL"
df = pd.read_sql(query, engine)
print("Données chargées :", df.shape)

# === 3️⃣ Préparer les données ===
df['loypredm2'] = df['loypredm2'].astype(float)
df_dep = df.groupby('DEP', as_index=False)['loypredm2'].mean()
print("Nombre de départements :", len(df_dep))

# === 4️⃣ Télécharger les frontières géographiques (GeoJSON) ===
geo_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
response = requests.get(geo_url)
if response.status_code != 200:
    raise Exception(f"Erreur lors du téléchargement du GeoJSON ({response.status_code})")
geo_json = response.json()
print("Fichier GeoJSON chargé avec succès.")

# === 5️⃣ Créer la carte Folium ===
# (carte standard avec labels et fond clair)
m = folium.Map(
    location=[46.6, 2.5],
    zoom_start=6,
    tiles="OpenStreetMap"
)

# === 6️⃣ Ajouter la couche choroplèthe ===
folium.Choropleth(
    geo_data=geo_json,
    name="Loyers moyens",
    data=df_dep,
    columns=["DEP", "loypredm2"],
    key_on="feature.properties.code",
    fill_color="YlOrRd",   # jaune → rouge
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Loyer moyen au m² (€)",
    highlight=True
).add_to(m)

# === 7️⃣ Ajouter un tooltip (infobulle au survol) ===
# On relie chaque polygone à ses infos (nom + valeur)
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

# On ajoute aussi le loyer moyen depuis notre DataFrame
for _, row in df_dep.iterrows():
    dep_code = row['DEP']
    value = round(row['loypredm2'], 2)

    # On cherche la géométrie correspondante
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

# === 8️⃣ Ajouter la couche de labels des villes par-dessus ===
folium.TileLayer(
    tiles='https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png',
    attr='©OpenStreetMap, ©CartoDB',
    name='Labels des villes',
    control=False
).add_to(m)

# === 9️⃣ Sauvegarder la carte avec un nom unique ===
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_PATH = f"outputs/carte_loyers_dep_{stamp}.html"
m.save(OUTPUT_PATH)
print(f"✅ Carte enregistrée : {OUTPUT_PATH}")
print(f"Ouvrez ensuite : /{OUTPUT_PATH}")