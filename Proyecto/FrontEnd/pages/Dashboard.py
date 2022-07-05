#libraries
from dash import html , dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_labs.plugins.pages import register_page
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import os

register_page(__name__, path="/Dashboard")

from components.df.df_dashboard import df, df2, df3


#df = px.data.medals_wide(indexed=True)

# specific layout for this page
layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H3('Informe de productividad gestores de salud año 2022',  className='text-center text-primary, mb-4'),
            width=12)
            ]),

        dbc.Row([
            dbc.Col([
                html.P("Seleccione un gestor de salud: "),
                dcc.Dropdown(id='my-dpdn', multi=False, value='LINA MARGARITA RICARDO MORENO',
                             options=[{'label':x, 'value':x}
                                  for x in sorted(df2['NOMBRE_USUARIO'].unique())]),
                 dcc.Graph(id='line-fig', figure={})], 
                            #width={'size':5, 'offset':1, 'order':1}),
                            xs=12, sm=12, md=12, lg=5, xl=5),
            dbc.Col([
                html.P("Seleccione un origen de solicitud: "),
                dcc.Dropdown(id='my-dpdn2', multi=True, value=['ASIGNACION DE CITAS', 'SOL. AUTORIZACION'],
                            options=[{'label':x, 'value':x}
                                  for x in sorted(df3['ORIGEN'].unique())],
                         ),
                dcc.Graph(id='line-fig2', figure={})],
                        # width={'size':5, 'offset':0, 'order':2}),
                        xs=12, sm=12, md=12, lg=5, xl=5),
                ], justify='center'),  # Horizontal:start,center,end,between,around

        dbc.Row([
             dbc.Col([
                html.P("Seleccione el mes de interés: "),
                dcc.Checklist(id='my-checklist',  value=['1', '2', '3'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df['MES'].unique())],
                          labelClassName='mr-4'),
                dcc.Graph(id='my-hist', figure={})], 
                         # width={'size':5, 'offset':1}
                          xs=12, sm=12, md=12, lg=5, xl=5),
                
                dbc.Col([
                     dbc.Card([
                    dbc.CardBody(
                        html.P("We're better together. Help each other out!", className="card-text")),
                    dbc.CardImg(src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif", bottom=True)],style={"width": "24rem"})

                        ], 
                        #width={'size':5, 'offset':1})
                        xs=12, sm=12, md=12, lg=5, xl=5),

                ],align='center', justify='center'),


], fluid=True)


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@callback(Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df2[df2['NOMBRE_USUARIO']==stock_slctd]
    dff.rename(columns={'MES':'Mes','Solicitud': 'Numero de solicitudes'}, inplace=True)
    figln = px.bar(dff, x='Mes', y='Numero de solicitudes')
    return figln



# Line chart - multiple
@callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df3.loc[df3['ORIGEN'].isin(stock_slctd)]
    dff.rename(columns={'MES':'Mes','Solicitud': 'Numero de solicitudes'}, inplace=True)
    #figln2 = px.bar(dff, x='Mes', y='Numero de solicitudes', color='ORIGEN',barmode="group")
    figln2 = px.pie(dff, values='Numero de solicitudes', names='ORIGEN')
    return figln2
