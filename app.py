import os
import subprocess
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from pages import home, carte, histogrammes, classement  # ← assure-toi que toutes les pages sont importées

# --- Fonction pour exécuter les scripts ---
def run_script(script_name):
    """Exécute un script Python donné."""
    try:
        subprocess.run(['python3', script_name], check=True)
        print(f"✅ {script_name} exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de {script_name}: {e}")

# --- Dossier de sortie pour les fichiers générés ---
OUT_DIR = "assets"
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    print("🎯 Lancement des étapes de traitement...")

    # 1. Récupérer les données et nettoyer
    run_script('data/use/get_data.py')  # Récupérer le CSV
    run_script('data/use/clean_data.py')  # Nettoyer les données
    run_script('data/use/add_coordinate.py')  # Ajouter les coordonnées géographiques

    # 2. Créer la base de données et insérer les données
    run_script('bdd/db.py')  # Créer la base de données
    run_script('bdd/import_to_postgre.py')  # Importer les données dans PostgreSQL

    # 3. Générer les histogrammes
    run_script('Histo/hist_littoral_vs_nonlittoral.py')  # Histogramme Littoral vs Non-Littoral
    run_script('Histo/hist_ratio_loyer_dep.py')  # Histogramme Ratio Loyer Département
    run_script('Histo/histo_loyer_moyen.py')  # Histogramme Loyer Moyen
    run_script('Histo/histo_loyer_region.py')  # Histogramme Loyer Moyen par Région
    run_script('Histo/Histo_paris.py')  # Histogramme Loyer Paris

    # 4. Générer la carte Folium
    run_script('carte/carte.py')  # Créer la carte Folium

    # 5. Lancer le dashboard
    print("🔘 Lancement du dashboard...")
    app = Dash(__name__)
    app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='topnav', className="topnav"),
        html.Div(id='page-content', className="main-content")
    ])

    # Navigation et affichage des pages Dash
    nav_links = [
        {"label": "Accueil", "href": "/"},
        {"label": "Carte", "href": "/carte"},
        {"label": "Histogrammes", "href": "/histogrammes"},
        {"label": "Classement", "href": "/classement"}
    ]

    @app.callback(
        Output('topnav', 'children'),
        Input('url', 'pathname')
    )
    def update_nav(pathname):
        links = [html.H2("Dashboard Loyers", style={"margin":"0", "display":"inline-block", "marginRight":"50px"})]
        for link in nav_links:
            class_name = "topnav-link"
            if pathname == link["href"]:
                class_name += " active"  # ajoute la classe active
            links.append(dcc.Link(link["label"], href=link["href"], className=class_name))
        return links

    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == '/carte':
            return carte.layout
        elif pathname == '/histogrammes':
            return histogrammes.layout
        elif pathname == '/classement':
            return classement.layout
        else:
            return home.layout

    app.run(debug=True)

if __name__ == "__main__":
    main()