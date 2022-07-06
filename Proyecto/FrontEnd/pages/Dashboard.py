#libraries
from tkinter import font
from dash import html , dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash_labs.plugins.pages import register_page
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import os

register_page(__name__, path="/Dashboard")

from components.df.df_dashboard import df, df2, df3

# specific layout for this page
layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.H2('Informe de productividad gestores de salud año 2022',  className='text-center text-primary, mb-4', style={'color':'#0380C4'}),
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
                html.P(" ")
            ])


        ]),

        dbc.Row([
             dbc.Col([
                html.P("Seleccione el mes de interés: "),
                dcc.Checklist(id='my-checklist',  value=['1', '2', '3'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df['MES'].unique())],
                          labelClassName='mr-4'),
                dcc.Graph(id='my-hist', figure={})], 
                          width={'size':5, 'offset':1})
                          #xs=12, sm=12, md=12, lg=5, xl=5),
                


                ],align='center', justify='center'),


# Esto es para generar espacio entre el logo y el Dashboard 
    dbc.Row([
        dbc.Col([html.Div(),], className = 'p-5'),
        ]),
    dbc.Row([
        dbc.Col([html.Div(),], className = 'p-5'),
        ]),


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



# Pie chart - multiple
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
