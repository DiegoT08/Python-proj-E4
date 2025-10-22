import pandas as pd
import folium
import json
import requests

# === 1️⃣ Charger les données nettoyées ===
DATA_PATH = "data/cleaned/pred-mai-mef-dhup_clean.csv"
df = pd.read_csv(DATA_PATH, sep=';')
print("Données chargées :", df.shape)

# === 2️⃣ Préparer les données ===
# On garde uniquement les colonnes utiles
df = df[['DEP', 'loypredm2']].dropna()
df['loypredm2'] = df['loypredm2'].astype(float)

# Calcul du loyer moyen par département
df_dep = df.groupby('DEP', as_index=False)['loypredm2'].mean()
print("Nombre de départements :", len(df_dep))

# === 3️⃣ Charger les frontières géographiques des départements (GeoJSON) ===
geo_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
response = requests.get(geo_url)
if response.status_code != 200:
    raise Exception(f"Erreur de téléchargement du GeoJSON ({response.status_code})")
geo_json = response.json()
print("Fichier GeoJSON chargé avec succès.")

# === 4️⃣ Créer la carte Folium ===
m = folium.Map(location=[46.6, 2.5], zoom_start=6, tiles='OpenStreetMap')

# === 5️⃣ Ajouter la couche choroplèthe (carte colorée) ===
folium.Choropleth(
    geo_data=geo_json,
    name="choropleth",
    data=df_dep,
    columns=["DEP", "loypredm2"],
    key_on="feature.properties.code",
    fill_color="YlOrRd",         # palette jaune → rouge
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name="Loyer moyen au m² (€)",
    highlight=True
).add_to(m)

# === 6️⃣ Ajouter des popups dynamiques avec les valeurs ===
for _, row in df_dep.iterrows():
    dep_code = row['DEP']
    value = round(row['loypredm2'], 2)
    folium.Marker(
        location=[46.6, 2.5],  # position par défaut remplacée plus bas
        popup=f"Département {dep_code} : {value} €/m²"
    )

# === 7️⃣ Sauvegarder la carte ===
OUTPUT_PATH = "outputs/carte_loyers_dep.html"
m.save(OUTPUT_PATH)
print(f"✅ Carte enregistrée : {OUTPUT_PATH}")
print("Ouvrez le fichier HTML dans votre navigateur pour visualiser la carte.")
