# Basics Requirements
import pathlib
import os
from dash import Dash, callback, html, dcc, dash_table, Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go
import plotly.express as px

# Dash Bootstrap Components
import dash_bootstrap_components as dbc

# Data
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

# Recall app
from app import app

###########################################################
#
#           APP LAYOUT:
#
###########################################################


# LOAD THE DIFFERENT FILES
from lib import title, sidebar, us_map, stats, selector



#components
#dropdownsex=dcc.Dropdown(id="sexo",value=["Hombre", "Mujer"], multi=False),




# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    [
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H1("MODELO PREDICTOR DE PRODUCTIVIDAD CON BASE EN CARACTERISTICAS SOCIODEMOGRAFICAS"),style={'textAlign': 'center', 'color': '#7FDBFF'}, width={"size": 10, "offset": 1}))]),
        html.Hr(),
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H5("Seleccione de las listas desplegables las caracteristicas de la persona seleccionada"), style={'textAlign': 'center'},width={"size": 6, "offset": 3}))]),
        html.Hr(),
        html.Br(),
        html.Br(),
        html.H5("Sexo"),
        html.Div([dcc.Dropdown(['Hombre', 'Mujer'], 'Sexo', id='sexdropdown'),    html.Div(id='sex-output-container')]),
        html.H5("Numero Hijos"),
        html.Div([dcc.Dropdown(['1', '2','3', '4','>5'], 'N.Hijos', id='hijosdropdown'),    html.Div(id='hijos-output-container')]),
        html.H5("Municipio Residencia"),
        html.Div([dcc.Dropdown(['Montería', 'Tierraalta'], 'Municipio', id='muni-dropdown'),    html.Div(id='muni-output-container')]),
        html.H5("Personas a cargo"),
        html.Div([dcc.Dropdown(['1', '2','3', '4','>5'], 'Personas a cargo', id='per-dropdown'),    html.Div(id='per-output-container')]),
        html.H5("Estado Civil"),
        html.Div([dcc.Dropdown(['Soltero', 'Casado', 'Unión Libre'], 'Estado', id='est-dropdown'),    html.Div(id='est-output-container')]),
        html.H5("Nivel Estudios"),
        html.Div([dcc.Dropdown(['Bachiller', 'Pregrado', 'Posgrado'], 'Nivel Estudios', id='niv-dropdown'),    html.Div(id='niv-output-container')]),
        html.H5("Programa Academico"),
        html.Div([dcc.Dropdown(['Medico', 'Auxiliar', 'Asistente'], 'Programa Academico', id='pro-dropdown'),    html.Div(id='pro-output-container')]),
        html.Br(),
        html.Div([dbc.Label("Ingrese la meta establecida por mes"),dbc.Input(id="meta", type="number", value="Escriba solo un numero enteros"),]),
        html.Br(),
        
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Button("Calcular", id="btncalcular", n_clicks=0,style={"horizontalAlign": "middle",'textAlign': 'center'}),     
        html.Hr(),
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H5("Resultados Obtenidos"), style={'textAlign': 'center'},width={"size": 6, "offset": 3}))]),
        html.Hr(),
        html.Br(),
        
        
        
        dbc.Container([dbc.Input(id="salida", placeholder="Waiting", type="text", value="Aquí aparece su resultado"),]),

        
        
        html.Br(),
        html.Br(),
        dbc.Button("INGRESAR AL DASHBOARD", id="btndashboard", n_clicks=0,style={"horizontalAlign": "middle",'textAlign': 'center'}),   
        html.Br(),
        html.Br(),
        html.Div(children=[html.Img(src=app.get_asset_url("Logo.jpg"),id="Logo",style={ 'width':'100%','position':'absolute', 'display': 'flex','flex': 1,'textAlign': 'center', 'color': '#7FDBFF'},)],),
        
    ],
)














'''
# PLACE THE COMPONENTS IN THE LAYOUT
app.layout = html.Div(
    [
        us_map.map,
        stats.stats,
        title.title,
        sidebar.sidebar,
    ],
)

###############################################
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
# Load and modify the data that will be used in the app.
#################################################################
DATA_DIR = "data"
superstore_path = os.path.join(DATA_DIR, "superstore.csv")
us_path = os.path.join(DATA_DIR, "us.json")
states_path = os.path.join(DATA_DIR, "states.json")
df = pd.read_csv(superstore_path, parse_dates=["Order Date", "Ship Date"])

with open(us_path) as geo:
    geojson = json.loads(geo.read())

with open(states_path) as f:
    states_dict = json.loads(f.read())

df["State_abbr"] = df["State"].map(states_dict)
df["Order_Month"] = pd.to_datetime(df["Order Date"].dt.to_period("M").astype(str))


#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@app.callback(
    [
        Output("Line", "figure"),
        Output("Scatter", "figure"),
        Output("Treemap", "figure"),
    ],
    [
        Input("state_dropdown", "value"),
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date"),
    ],
)
def make_line_plot(state_dropdown, start_date, end_date):
    df = us_map.df
    df['Order_Month'] = pd.to_datetime(df['Order Date'].dt.to_period('M').astype(str))
    ddf = df[df["State_abbr"].isin(state_dropdown)]
    ddf = ddf[(ddf["Order Date"] >= start_date) & (ddf["Order Date"] < end_date)]

    ddf1 = ddf.groupby(["Order_Month", "State"]).sum()
    ddf1 = ddf1.reset_index()

    Line_fig = px.line(ddf1, x="Order_Month", y="Sales", color="State")
    Line_fig.update_layout(
        title="Montly Sales in selected states", paper_bgcolor="#F8F9F9"
    )

    Scatter_fig = px.scatter(
        ddf,
        x="Sales",
        y="Profit",
        color="Category",
        hover_data=["State_abbr", "Sub-Category", "Order ID", "Product Name"],
    )
    Scatter_fig.update_layout(
        title="Sales vs. Profit in selected states", paper_bgcolor="#F8F9F9"
    )

    Treemap_fig = px.treemap(
        ddf,
        path=["Category", "Sub-Category", "State"],
        values="Sales",
        color_discrete_sequence=px.colors.qualitative.Dark24,
    )

    return [Line_fig, Scatter_fig, Treemap_fig]


#############################################################
# TREEMAP PLOT : Add sidebar interaction here
#############################################################


#############################################################
# MAP : Add interactions here
#############################################################

# MAP date interaction
@app.callback(
    Output("US_map", "figure"),
    [Input("date_picker", "start_date"), Input("date_picker", "end_date")],
)
def update_map(start_date, end_date):
    dff = df[
        (df["Order Date"] >= start_date) & (df["Order Date"] < end_date)
    ]  # We filter our dataset for the daterange
    dff = dff.groupby("State_abbr").sum().reset_index()
    fig_map2 = px.choropleth_mapbox(
        dff,
        locations="State_abbr",
        color="Sales",
        geojson=geojson,
        zoom=3,
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},
        color_continuous_scale="Viridis",
        opacity=0.5,
        title="US Sales",
    )
    fig_map2.update_layout(
        title="US State Sales",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="#F8F9F9",
        plot_bgcolor="#F8F9F9",
    )
    return fig_map2


# MAP click interaction


@app.callback(
    Output("state_dropdown", "value"),
    [Input("US_map", "clickData")],
    [State("state_dropdown", "value")],
)
def click_saver(clickData, state):
    if clickData is None:
        raise PreventUpdate

    # print(clickData)

    state.append(clickData["points"][0]["location"])

    return state
'''

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port="8050", debug=True)
