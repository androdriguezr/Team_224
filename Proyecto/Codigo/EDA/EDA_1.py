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

## de demográficos ##########
os.chdir(os.path.join(ruta_insumos,"Encuesta_sociodem_empleados"))
sendero_feature=os.path.join(os.getcwd(),str(os.listdir()[0]))
feature_demo=pd.read_excel(sendero_feature)
feature_demo.dropna(subset=["NOMBRE_CLAVE"],inplace=True)

#estadisticos_iniciales=consol_data.describe(include = ['O'])
## importando los datos de las actividades   #######

os.chdir(os.path.join(ruta_insumos,'Datos_eventos'))
sendero_eventos=os.path.join(os.getcwd(),str(os.listdir()[0]))
datos_eventos=pd.read_excel(sendero_eventos)
datos_eventos['cedula']=datos_eventos['cedula'].astype('str')
#datos_eventos.dropna(subset=["NOMBRE_CLAVE"],inplace=True)


'''descripcion variable. todo debe ser objeto porque ninguno se va a utilizar como float'''


##### unir con el DF de features_demograficos #####################

## la siguiente linea, permite verificar el A-B de dos grupos de Strings


feature_demo['NUMERO_DE_DOCUMENTO']=feature_demo.NUMERO_DE_DOCUMENTO.astype('int').astype('str').str.strip()
consol_data_con_features=feature_demo.merge(datos_eventos,how='left',left_on='NOMBRE_CLAVE',right_on='NOMBRE_USUARIO',)

#consol_data_con_features['NUMERO_DE_DOCUMENTO']=consol_data_con_features['NUMERO_DE_DOCUMENTO'].astype('str').str.strip()
sueldos['Codigo']=sueldos['Codigo'].str.strip()
data_agregada=consol_data_con_features.merge(sueldos[['year','Codigo','Sueldo','Cargo']],how="left",left_on=['year','NUMERO_DE_DOCUMENTO'],right_on=['year','Codigo'])



data_agregada['Wage_fixed']=np.where(data_agregada.Sueldo.isna(),data_agregada.SALARIO , data_agregada.Sueldo)

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
