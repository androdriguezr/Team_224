#libraries
from dash import html , dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page

#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import os

register_page(__name__, path="/Dashboard")

# specific layout for this page
layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                        html.Div([
            html.Div([
                html.H1('Seguimiento al personal operativo', style={'margin-bottom': '100px', 'color': 'Blue'}),

                html.H2('DS4A COLOMBIA / TEAM 224', style={'margin-bottom': '10px', 'color': 'Blue'})
            ])

        ], className='one-half column', id = 'title'),

            ], lg=15), 
           
        ]),
        ]
)