#libraries
from dash import html
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page


# dash-labs plugin call, menu name and route
register_page(__name__, path="/dashboard")

# specific layout for this page
layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                 
            ], ), 
           
        ]),
        ]
)