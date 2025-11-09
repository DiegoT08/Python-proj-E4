from dash import html

layout = html.Div([
    html.H1("Carte des loyers", style={"color":"#000000"}),
    html.Iframe(src="/assets/carte_loyers.html",
                style={"width":"100%", "height":"600px", "border":"none", "borderRadius":"12px"})
])