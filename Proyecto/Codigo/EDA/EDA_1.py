# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:38:33 2022

@author: USUARIO
"""
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
##### organizando rutas #########

ruta_madre="C:/Users/USUARIO/Documents/GitHub/Team_224/Proyecto"
ruta_insumos=os.path.join(ruta_madre, 'Insumos')
ruta_resultados=os.path.join(ruta_madre, 'Resultados')

##### importando ##########


### datos sueldos####
os.chdir(os.path.join(ruta_insumos,'Descripcion_empleados'))
sendero_sueldos=os.path.join(os.getcwd(),'Sueldos_nomina_consolidados.csv')
sueldos=pd.read_csv(sendero_sueldos,sep=";")
#sueldos['year']=sueldos['year'].astype('float64')
sueldos['Codigo']=sueldos['Codigo'].astype('int').astype('str')
sueldos.drop_duplicates(['year','Codigo','Nombres'],inplace=True)

## datos  demográficos ##########
os.chdir(os.path.join(ruta_insumos,"Encuesta_sociodem_empleados"))
sendero_feature=os.path.join(os.getcwd(),str(os.listdir()[0]))
feature_demo=pd.read_excel(sendero_feature)
#feature_demo.dropna(subset=["NOMBRE_CLAVE"],inplace=True)

#estadisticos_iniciales=consol_data.describe(include = ['O'])
## importando los datos de las actividades   #######

os.chdir(os.path.join(ruta_insumos,'Datos_eventos'))
sendero_eventos=os.path.join(os.getcwd(),str(os.listdir()[0]))
datos_eventos=pd.read_excel(sendero_eventos)
datos_eventos['cedula']=datos_eventos['cedula'].astype('str')
#datos_eventos.dropna(subset=["NOMBRE_CLAVE"],inplace=True)


'''descripcion variable. todo debe ser objeto porque ninguno se va a utilizar como float'''


##### limpieza de data#######

### creando variables utiles#####


feature_demo['NUMERO_DE_DOCUMENTO']=feature_demo.NUMERO_DE_DOCUMENTO.astype('int').astype('str').str.strip()
sueldos['Codigo']=sueldos['Codigo'].str.strip()


consol_data_con_features=datos_eventos.merge(feature_demo,how='left',right_on='NUMERO_DE_DOCUMENTO',left_on='cedula')

data_agregada=consol_data_con_features.merge(sueldos[['year','Codigo','Sueldo','Cargo']],how='left',left_on=['year','cedula'],right_on=['year','Codigo'])

## crear edad

##data_agregada['Wage_fixed']=np.where(data_agregada.Sueldo.isna(),data_agregada.SALARIO , data_agregada.Sueldo)

data_agregada['fecha_analisis']=[pd.to_datetime(datetime(data_agregada['year'][x],data_agregada['MES'][x],1)) for x in range(len(data_agregada['year']))]

years_born=data_agregada['fecha_analisis']-data_agregada['FECHA_DE_NACIMIENTO']

data_agregada['edad']=years_born.dt.days//360; del years_born
 
## crear años de experiencia#####

expertise=data_agregada['fecha_analisis']-data_agregada['FECHA_DE_INGRESO']
data_agregada['years_antiguedad']=expertise.dt.days/360 ; del expertise

data_agregada.drop(columns=['NOMBRES','APELLIDOS','Codigo','NUMERO_DE_DOCUMENTO'],inplace=True)

## arreglar genero( esta bien)

### arreglar poblacion especial


###arreglar municipio

data_agregada['MUNICIPIO_DE_RESIDENCIA']=data_agregada.MUNICIPIO_DE_RESIDENCIA.str.lower().str.strip().str.replace('[ ]+','_')

def normalizar(x):
    
    caracter_norm=re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
            normalize( "NFD", x
            ), 0, re.I
        )
    return caracter_norm

prueba=[]
for i in range(len(data_agregada['MUNICIPIO_DE_RESIDENCIA'])):
    
    try:
        prueba.append(normalizar(data_agregada['MUNICIPIO_DE_RESIDENCIA'][i]))
    except:
        
        prueba.append(np.nan)
    
    
data_agregada['MUNICIPIO_DE_RESIDENCIA']=prueba ## se le quita las tildes

### normalizar las solicitudes###

## que quede solicitudes, autorizaciones por dia

data_agregada['fecha_fin']=pd.to_datetime([data_agregada['fecha_analisis'][j]+relativedelta(months=1) for j in range(len(data_agregada['fecha_analisis']))])
data_agregada['dias_mes']=data_agregada['fecha_fin']-data_agregada['fecha_analisis']
data_agregada['dias_mes']=data_agregada['dias_mes'].dt.days
data_agregada['solicitudes_per_day']=data_agregada['Solicitud']/data_agregada['dias_mes']
data_agregada['autorizaciones_per_day']=data_agregada['Autorizacion']/data_agregada['dias_mes']
data_agregada['codigos_per_day']=data_agregada['codigo']/data_agregada['dias_mes']


###profesion##

data_agregada['PROFESION']=data_agregada['PROFESION'].str.lower()

prueba=[]
for i in range(len(data_agregada['PROFESION'])):
    
    try:
        prueba.append(normalizar(data_agregada['PROFESION'][i]))
    except:
        
        prueba.append(np.nan)
   
    
data_agregada['PROFESION']=prueba
#data_agregada['edad']=

###### Exploratoy Data Analysis#######

## info general
data_agregada.info() ## la variables provenientes de los sueldos año a año, tienen cerca del 56% de la data dañada por falta de info de sueldos en ciertos años, 

## describe
data_agg_describe_numeric=data_agregada.describe()
data_agg_describe_obbject=data_agregada.describe(include=['O'])

#### grafica de correlacion
corr = data_agregada.corr()
sm.graphics.plot_corr(corr, xnames=list(corr.columns))
plt.show()


## graficas de visualizacion

plt.figure(figsize=(8,9))

## solicitud atendidas por year
sns.barplot(x='year',y='Solicitud',data=data_agregada)

## solicitudes per capita atendias por year
suma_solicitudes=data_agregada.groupby('year').agg({'Solicitud': ['sum'], 'NOMBRE_CLAVE': 'count'}).reset_index()

suma_solicitudes['prod_per_capita']=suma_solicitudes.Solicitud/suma_solicitudes.NOMBRE_CLAVE

sns.barplot(x='year',y='Solicitud',data=data_agregada)
