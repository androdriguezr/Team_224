import dash_bootstrap_components as dbc
from dash import html
from dash_labs.plugins.pages import register_page


register_page(__name__, path="/nosotros")

layout = dbc.Row([
    dbc.Col([
        dbc.Row(["DS4A Project - Team 224"], className= "flex-fill ")
    ], className = "d-flex display-4 align-self-center flex-column align-items-center"),
        dbc.Row([
        html.Img(src='/assets/nosotros.PNG',className="img-fluid")
    ],  className = "d-flex align-items-center display-6 justify-content-start")

])
