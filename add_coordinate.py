import pandas as pd
import geopandas as gpd

# Charger ton dataset
df = pd.read_csv("data/cleaned/pred-mai-mef-dhup_clean.csv", sep=";")

# Charger GeoJSON des communes françaises
communes = gpd.read_file("https://france-geojson.gregoiredavid.fr/repo/communes.geojson")

# Fusionner via code INSEE
df = df.merge(communes[['code', 'geometry']], left_on='INSEE_C', right_on='code', how='left')

# Transformer en GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry='geometry')

# Extraire centroides
gdf['latitude'] = gdf.geometry.centroid.y
gdf['longitude'] = gdf.geometry.centroid.x

# Sauvegarder
gdf.to_csv("data/cleaned/pred-mai-mef-dhup_clean_coords.csv", sep=";", index=False)
print("CSV avec coordonnées généré !")