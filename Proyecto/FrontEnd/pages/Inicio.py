import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from dash import html

register_page(__name__, path="/")

layout=  dbc.Container(
    [   html.Div(children=[dbc.Row(dbc.Col(html.H5("SELECCIONE EL LINK DE INTERES"), style={'textAlign': 'center'},width={"size": 6, "offset": 3}))]),
    
        dbc.Row([dbc.NavItem(dbc.NavLink("Antecedentes", href="/antecedentes"),className= "card2")
            
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Modelo", href="/modelo"),className= "card2")
            
        ]),
        dbc.Row([dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard"),className= "card2")
            
        ]),
        dbc.Row([  
            html.Img(src='/assets/Logo.jpg',className="img-fluid")
        ],  className = "card")
         
    ]
)  