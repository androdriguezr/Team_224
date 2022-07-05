import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from dash import html

register_page(__name__, path="/")

layout=  dbc.Container(
    [   html.Div(children=[dbc.Row(dbc.Col(html.H5("Seleccione el link de interes:"), style={'textAlign': 'center',"font-size": "40px"}))]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Antecedentes", href="/antecedentes"),className= "card2")
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Modelo", href="/modelo"),className= "card2")
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Dashboard", href="/Dashboard"),className= "card2")
        ]),
        dbc.Row([ html.Img(src='/assets/logo.png',className="img-fluid")],  className = "card")
    ]
)  