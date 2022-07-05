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
import re
from dateutil.relativedelta import relativedelta
import pingouin
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
import scipy
from scipy.stats import chi2_contingency
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.formula.api as smf
from pycaret.classification import *
from os import *

register_page(__name__, path="/modelo")

os.chdir(r"C:\Users\relat\Documents\GitHub\Team_224\Proyecto\Frontend")
all_data_final_model=load_model('model_selected_pipeline')

load_model('model_selected_pipeline')

ruta_madre="C:/Users/relat/Documents/GitHub/Team_224/Proyecto/Frontend/data"
ruta_data_preproc=os.path.join(ruta_madre,'data_master_ready_to_model.xlsx')
datos_to_model=pd.read_excel(ruta_data_preproc,index_col=0)

layout = html.Div(
    [
        html.Div(children=[dbc.Row(dbc.Col(html.H2("MODELO PREDICTOR DE PRODUCTIVIDAD CON BASE EN CARACTERISTICAS SOCIODEMOGRAFICAS"),style={'textAlign': 'center', 'color': '#0380C4'}, width={"size": 10, "offset": 1}))]),
        html.Hr(),
        html.Div(children=[dbc.Row(dbc.Col(html.H5("Seleccione de las listas desplegables las características de la persona seleccionada"), style={'textAlign': 'center'},width={"size": 8, "offset": 2}))]),
        html.Hr(),
        html.Div(children=[dbc.Row(dbc.Col(html.H5("Edad"),width={"size": 8, "offset": 2}))]),
        html.Div([dcc.Dropdown([18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65], 'EDAD', id='edad-dropdown'),]),
        html.H5("Genero"),
        html.Div([dcc.Dropdown(['MALE', 'FEMALE','OTHER'], 'GENERO', id='genero-dropdown'), ]),
        html.H5("Población especial"),
        html.Div([dcc.Dropdown(['NO APLICA', 'MADRE CABEZA DE FAMILIA','DESPLAZADO','VICTIVA CONFLICTO ARMADO', 'MUJER GESTANTE'], 'Población Especial', id='poblacion-dropdown')]),
        html.H5("Alguna discapacidad"),
        html.Div([dcc.Dropdown(['NO', 'no_reported'], 'Alguna Discapacidad', id='dis-dropdown'),    html.Div(id='dis-output-container')]),
        html.H5("Municipio de residencia"),
        html.Div([dcc.Dropdown(['monteria', 'sahagun', 'montelibano', 'planeta_rica', 'san_pelayo','cienaga_de_oro', 'cerete', 'murindo', 'NO_REPORTADO'], 'Municipio Residecnia', id='mun-dropdown'),]),
        html.H5("Tipo de casa"),
        html.Div([dcc.Dropdown(['ARRENDADA', 'FAMILIAR', 'PROPIA', 'OTHER'], 'Tipo de Casa', id='casa-dropdown'),]),
        html.H5("Nivel académico"),
        html.Div([dcc.Dropdown(['PROFESIONAL', 'TECNICO', 'TECNOLOGO', 'OTHER'], 'Nivel Academico', id='nivel-dropdown'),]),
        html.H5("Profesión"),
        html.Div([dcc.Dropdown(['admin_empresas', 'admin_servicios_salud', 'secretariado','asistente_administrativo', 'auxiliar_enfermeria', 'OTHER','agente_call_center', 'auxiliar administrativa','tecnico auxiliar en auxiliar contable sistematizado  -- tecnico agente de contac center','secretariado y asisten administrativo',
        'tecnico asistencia en organizacion de archivos'], 'Profesión', id='pro-dropdown'),]),
        html.H5("Estado civil"),
        html.Div([dcc.Dropdown(['SINGLE', 'MARRIED', 'CONSENSUAL UNION', 'DIVORCED', 'OTHER'], 'Estado Civil', id='estciv-dropdown'),]),
        html.H5("Dependientes"),
        html.Div([dcc.Dropdown(['2.0', '1.0', '3.0', '0.0', '7.0', '4.0', '8.0', 'nan'], 'Dependientes', id='dep-dropdown'),]),
        html.H5("Estrato social"),
        html.Div([dcc.Dropdown(['3.0', '1.0', '2.0', 'nan'],'Estrato Social',id='estrato-dropdown',),]),
        html.H5("Años en el rol"),
        html.Div([dcc.Dropdown([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], 'Años rol', id='yearsrol-dropdown')]),
        html.Br(),
        dbc.Button("Calcular", id="btncalcular", n_clicks=0),     
        html.Hr(),
        html.Div(children=[dbc.Row(dbc.Col(html.H5("Resultados Obtenidos"),width={"size": 6, "offset": 3}))]),
        html.Hr(),
        html.Br(),
        dbc.Container([dbc.Input(id="salida", placeholder=""),]),  
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
def update_sal(edad,genero, poblacion, dis, mun, casa, nivel, pro, estadociv, dep,estrato,yearsrol, nclicks):
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
            if prediction2>=float(25) :
                a= ' Excelente perfil. contrátalo'
            elif (prediction2<float(25) and prediction2 >=float(17)):
                a= ' Es un perfil sobresaliente. contrátalo'
            elif (prediction2<float(17) and prediction2 >= float(11) ):
                a= ' Es un perfil estandar. podrías con periodo de prueba'
            else:
                a=  ' No es tan productivo. ten cuidado'
            return str(prediction2) , a