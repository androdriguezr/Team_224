import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from dash import html

register_page(__name__, path="/")

layout=  dbc.Container([
       dbc.Row([
            dbc.Row([
                dbc.Col(html.H2("Seleccione el link de interes:"), style={'textAlign': 'center', 'color':'#0380C4'})
                    ]),
            dbc.Row([
                dbc.Col([html.Div(),], className = 'p-3'),
                ]),
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Antecedentes", href="/antecedentes"),className= "card2")
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Modelo", href="/modelo"),className= "card2")
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Dashboard", href="/Dashboard"),className= "card2")
        ]),

    
        dbc.Row([
            dbc.Col([html.Div(),], className = 'p-5'),
                ]),
         dbc.Row([
            dbc.Col([html.Div(),], className = 'p-5'),
                ]),

])  

