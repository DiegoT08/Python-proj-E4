from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from pages import home, carte, histogrammes, classement  # ← AJOUT ICI

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# Liste des liens
nav_links = [
    {"label": "Accueil", "href": "/"},
    {"label": "Carte", "href": "/carte"},
    {"label": "Histogrammes", "href": "/histogrammes"},
    {"label": "Classement", "href": "/classement"}  # ← AJOUT ICI
]

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Navigation horizontale
    html.Div(id='topnav', className="topnav"),

    # Contenu principal
    html.Div(id='page-content', className="main-content")
])

# Callback pour générer la navigation avec lien actif
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

# Callback pour afficher la page
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/carte':
        return carte.layout
    elif pathname == '/histogrammes':
        return histogrammes.layout
    elif pathname == '/classement':  # ← AJOUT ICI
        return classement.layout
    else:
        return home.layout

if __name__ == "__main__":
    app.run(debug=True)