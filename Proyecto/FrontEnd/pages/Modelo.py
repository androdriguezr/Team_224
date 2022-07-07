import dash
import os
import pycaret
import scipy
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from dash import html , dcc, callback, Input, Output, State
import os
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
import seaborn as sns
from datetime import datetime
import math
import unicodedata
from unicodedata import normalize
from dateutil.relativedelta import relativedelta
import pingouin
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
import scipy
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
from pycaret.classification import *


register_page(__name__, path="/modelo")


all_data_final_model=load_model('model_selected_pipeline')

load_model('model_selected_pipeline')

ruta_madre="./data"
ruta_data_preproc=os.path.join(ruta_madre,'data_master_ready_to_model.xlsx')
datos_to_model=pd.read_excel(ruta_data_preproc,index_col=0)

layout = html.Div(
    [
        html.Div(children=[dbc.Row(dbc.Col(html.H2("Modelo predictor de productividad con base en características sociodemográficas"),style={'textAlign': 'center', 'color': '#0380C4'}, width={"offset": 1}))]),
        html.Hr(),

        html.Div(children=[dbc.Row(dbc.Col(html.H4("Seleccione de las listas desplegables las características de la persona seleccionada"), style={'textAlign': 'center'},width={"size": 8, "offset": 2}))]),
        html.Hr(),

        html.Div(children=[dbc.Row(dbc.Col(html.H5("Todos los campos deben ser diligenciados"), style={'textAlign': 'center', 'color':'#8b0000'},width={"size": 8, "offset": 2}))]),
        html.Hr(),
        html.Hr(),
        
        #html.Div(children=[dbc.Row(dbc.Col(html.H5("Edad (en años)"),width={"size": 8, "offset": 2}))]),
        html.H5("Edad (en años)"),
        html.Div([dcc.Dropdown([18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65], id='edad-dropdown'),]),
        
        html.H5("Género"),
        html.Div([dcc.Dropdown(options=[{'label':'Masculino', 'value':'MALE'}, 
                                        {'label':'Femenino', 'value':'FEMALE'},
                                        {'label':'No registra', 'value':'OTHER'}], id='genero-dropdown'), ]),
        html.H5("Población especial"),
        html.Div([dcc.Dropdown(options=[{'label':'No aplica', 'value':'NO APLICA'},
                                        {'label':'Madre cabeza de familia', 'value':'MADRE CABEZA DE FAMILIA'},
                                        {'label':'Desplazado', 'value':'DESPLAZADO'},
                                        {'label':'Víctima del conflicto armado', 'value':'VICTIVA CONFLICTO ARMADO'},
                                        {'label':'Mujer gestante', 'value':'MUJER GESTANTE'}], id='poblacion-dropdown')]),

        html.H5("Alguna discapacidad"),
        html.Div([dcc.Dropdown(options=[{'label':'No', 'value':'NO'},
                                      {'label':'No reporta', 'value':'no_reported'}], id='dis-dropdown')]),  
        
       
        html.H5("Municipio de residencia"),
        html.Div([dcc.Dropdown(options=[{'label':'Montería', 'value':'monteria'},
                                {'label':'Sahagún', 'value':'sahagun'},
                                {'label':'Montelíbano', 'value':'montelibano'},
                                {'label':'Planeta Rica', 'value':'planeta_rica'},
                                {'label':'San Pelayo', 'value':'san_pelayo'},
                                {'label':'Ciénaga de Oro', 'value':'cienaga_de_oro'},
                                {'label':'Cereté', 'value':'cerete'},
                                {'label':'Murindó', 'value':'murindo'},
                                {'label':'No reporta', 'value':'NO_REPORTADO'}], id='mun-dropdown')]),
       
        html.H5("Tipo de vivienda"),
        html.Div([dcc.Dropdown(options=[{'label':'Arrendada', 'value':'ARRENDADA'},
                                {'label':'Familiar ', 'value':'FAMILIAR'},
                                {'label':'Propia', 'value':'PROPIA'},
                                {'label':'Otra', 'value':'OTHER'}], id='casa-dropdown')]),
        
        html.H5("Nivel académico"),
        html.Div([dcc.Dropdown(options=[{'label':'Profesional', 'value':'PROFESIONAL'},
                                        {'label':'Técnico', 'value':'TECNICO'},
                                        {'label':'Tecnólogo', 'value':'TECNOLOGO'},
                                        {'label':'Otro', 'value':'OTHER'}], id='nivel-dropdown')]),
        
        html.H5("Profesión"),
        html.Div([dcc.Dropdown(options=[{'label':'Administrador de empresas', 'value':'admin_empresas'},
                                        {'label':'Administrador en servicios de salud', 'value':'admin_servicios_salud'},
                                        {'label':'Secretariado', 'value':'secretariado'},
                                        {'label':'Asistente administrativo', 'value':'asistente_administrativo'},
                                        {'label':'Auxiliar de enfermería', 'value':'auxiliar_enfermeria'},
                                        {'label':'Agente Call Center', 'value':'agente_call_center'},
                                        {'label':'Auxiliar administrativo', 'value':'auxiliar administrativa'},
                                        {'label':'Técnico auxiliar contable', 'value':'tecnico auxiliar en auxiliar contable sistematizado  -- tecnico agente de contac center'},                                      
                                        {'label':'Técnico asistente en administración de archivos', 'value':'tecnico asistencia en organizacion de archivos'},
                                        {'label':'Otra', 'value':'OTHER'}], id='pro-dropdown')]),
        
        html.H5("Estado civil"),
        html.Div([dcc.Dropdown(options=[{'label':'Soltero/a', 'value':'SINGLE'},
                                        {'label':'Casado/a', 'value':'MARRIED'},
                                        {'label':'Unión libre', 'value':'CONSENSUAL UNION'},
                                        {'label':'Divorsiado/a', 'value':'DIVORCED'},
                                        {'label':'No registra', 'value':'OTHER'}], id='estciv-dropdown')]),
        
        html.H5("Dependientes"),
        html.Div([dcc.Dropdown(options=[{'label':'Ninguno', 'value':'0.0'},
                                        {'label':'1', 'value':'1.0'},
                                        {'label':'2', 'value':'2.0'},
                                        {'label':'3', 'value':'3.0'},
                                        {'label':'4', 'value':'4.0'},
                                        {'label':'Más de 4', 'value':'7.0'},
                                        {'label':'No registra', 'value':'nan'}], id='dep-dropdown')]),
        
        html.H5("Estrato social"),
        html.Div([dcc.Dropdown(options=[{'label':'1', 'value':'1.0'},
                                        {'label':'2', 'value':'2.0'},
                                        {'label':'3', 'value':'3.0'},
                                        {'label':'No registra', 'value':'nan'}],id='estrato-dropdown')]),
        
        html.H5("Tiempo en el rol (en años)"),
        html.Div([dcc.Dropdown([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], id='yearsrol-dropdown')]),
        
        html.Br(),
        dbc.Button("Calcular", id="btncalcular", n_clicks=0),     
        html.Hr(),
        html.Div(children=[dbc.Row(dbc.Col(html.H5("Resultados Obtenidos"),width={"size": 6, "offset": 3}))]),
        html.Hr(),
        html.Br(),
        dbc.Container([dbc.Input(id="salida", placeholder="",style={'textAlign': 'center'}),]),  
        html.Br(),
        dbc.Button("Ingresar Dashboard", id="btndashboard",href="/Dashboard", n_clicks=0,),   
        html.Br(),
    ],style={'textAlign': 'center' , "margin-left": "15%", "margin-right": "15%", "margin-bottom": "5%"}
)

@callback(
        Output("salida", 'value'), 
        [State("edad-dropdown", "value"), 
        State("genero-dropdown","value"),
        State("poblacion-dropdown","value"),
        State("dis-dropdown","value"),
        State("mun-dropdown","value"),
        State("casa-dropdown","value"),
        State("nivel-dropdown","value"),
        State("pro-dropdown","value"),
        State("estciv-dropdown","value"),
        State("dep-dropdown","value"),
        State("estrato-dropdown","value"),
        State("yearsrol-dropdown","value"),
        Input("btncalcular", "n_clicks"),
        ],prevent_initial_call=True
    )
def update_sal(edad,genero, poblacion,dis, mun, casa, nivel, pro, estadociv, dep,estrato,yearsrol, nclicks):
#def update_sal(edad,genero, poblacion, dis, mun, casa, nivel, pro, estadociv, dep,estrato,yearsrol, nclicks):
            new_data=datos_to_model.iloc[[0,]].copy()
            new_data=new_data.drop(columns='request_attend_per_day')
            new_data['age']=float(edad)
            new_data['age2']=float(edad)**2
            new_data['age3']=float(edad)**3
            new_data['age4']=float(edad)**4
            new_data['age5']=float(edad)**5
            new_data['gender']=genero
            new_data['is_special_population']=str(poblacion)
            new_data['municipio_living']=str(mun)
            new_data['home_type']=str(casa)
            new_data['education_level']=str(nivel)
            new_data['marital_status']=str(estadociv)
            new_data['total_dependants']=str(dep)
            new_data['ESTRATO_SOCIAL']=str(estrato)
            new_data['years_exp_current_role']=float(yearsrol)
            new_data['PROFESION']=str(pro)

            prediction=predict_model(all_data_final_model, data = new_data)
            
            prediction2=float(prediction.Label)

            a=0
            if prediction2>=float(33) :
                a= 'Excelente perfil. Se sugiere tener en cuenta este perfil'
            elif (prediction2<float(33) and prediction2 >=float(25)):
                a= 'Es un perfil sobresaliente. Se sugiere tener en cuenta este perfil'
            elif (prediction2<float(25) and prediction2 >= float(17)):
                a= 'Es un perfil estándar. Se sugiere tener en cuenta este perfil en periodo de prueba'
            else:
                a= 'Bajo criterios del modelamiento, no se recomienda tener en cuenta este perfil'
                
            return a