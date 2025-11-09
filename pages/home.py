from dash import html

layout = html.Div([
    html.H1("Bienvenue sur le Dashboard des Loyers en France"),
    
    html.P("""
    Ce dashboard interactif a été conçu pour analyser et visualiser les loyers pratiqués dans différentes communes françaises. 
    Les données utilisées proviennent de sources publiques et comprennent des informations détaillées sur les communes, 
    leurs codes INSEE, départements et différentes métriques liées aux loyers.
    """),

    html.P("""
    Chaque ligne de données correspond à une unité géographique (commune ou maille) et contient :
    """),

    html.Ul([
        html.Li("Le code INSEE et le nom de la commune."),
        html.Li("Le département et les codes associés."),
        html.Li("Des métriques géographiques et statistiques liées aux loyers, telles que le loyer moyen, la densité, etc."),
        html.Li("Des informations sur la maille géographique utilisée."),
    ]),

    html.P("""
    L'objectif de ce dashboard est de fournir une vue d'ensemble claire et interactive des loyers, 
    permettant de naviguer entre différentes visualisations :
    """),

    html.Ul([
        html.Li("Une carte interactive des loyers par département, pour identifier les zones avec des loyers élevés ou faibles."),
        html.Li("Une galerie d'histogrammes et de graphiques pour visualiser les distributions des loyers."),
        html.Li("Un classement des dix villes les plus chères et des dix villes les moins chères accompagnés d'une carte interactive présentant ces différentes villes."),
    ]),

    html.P("""
    Ce projet est particulièrement utile pour les chercheurs, urbanistes, agents immobiliers ou toute personne 
    intéressée par l'analyse territoriale des loyers en France. 
    Grâce à ce dashboard, il est possible de détecter rapidement les tendances locales et de comparer différentes communes.
    """),
])