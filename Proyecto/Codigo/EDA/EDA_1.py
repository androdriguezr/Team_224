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

##### importando los datos de los sueldos #########
os.chdir("C:/Users/relat/Documents/GitHub/Team_224/Proyecto/Insumos/Descripcion_empleados")
sendero_sueldos=os.path.join(os.getcwd(),'Sueldos_nomina_consolidados.csv')
sueldos=pd.read_csv(sendero_sueldos,sep=";")
#sueldos['year']=sueldos['year'].astype('float64')
sueldos['Codigo']=sueldos['Codigo'].astype('int').astype('str')
sueldos.drop_duplicates(['year','Codigo','Nombres'],inplace=True)

##### importando los datos de demográficos ##########
os.chdir("C:/Users/relat/Documents/GitHub/Team_224/Proyecto/Insumos/Encuesta_sociodem_empleados")
sendero_feature=os.path.join(os.getcwd(),str(os.listdir()[0]))
feature_demo=pd.read_excel(sendero_feature)
feature_demo.dropna(subset=["NOMBRE_CLAVE"],inplace=True)

###### importando los datos de las actividades   #######
os.chdir("C:/Users/relat/Documents/GitHub/Team_224/Proyecto/Insumos/Asignacion_citas")

sendero=os.path.join(os.getcwd(),str(os.listdir()[0]))
data0=pd.read_excel(sendero, sheet_name='01-09')
data1=pd.read_excel(sendero, sheet_name='10-12')

sendero=os.path.join(os.getcwd(),str(os.listdir()[1]))
data2=pd.read_excel(sendero)
                
sendero=os.path.join(os.getcwd(),str(os.listdir()[2]))
data3=pd.read_excel(sendero)
                 
sendero=os.path.join(os.getcwd(),str(os.listdir()[3]))
data4=pd.read_excel(sendero)  

consol_data=pd.concat([data1,data0,data2,data3,data4])

consol_data = consol_data[['Año', 'MES', 'Fecha', 'ORIGEN', 'PuntoAtencion', 'Contrato',
       'NOMBRE_USUARIO', 'Tipo', 'Solicitud', 'Autorizacion', 'codigo',
       'descripcion', 'cantidad']]
consol_data['year']=consol_data['Fecha'].dt.year
del consol_data['Año']

###############  Trabajando con el set de datos  #################################

'''descripcion variable. todo debe ser objeto porque ninguno se va a utilizar como float'''

consol_data.info()
consol_data['Solicitud']=consol_data.Solicitud.astype('str')
consol_data['Autorizacion']=consol_data.Solicitud.astype('str')
consol_data['NOMBRE_USUARIO']=consol_data.NOMBRE_USUARIO.str.upper()

# Revisando la data
consol_data.info()
estadisticos_iniciales=consol_data.describe(include = ['O'])
consol_data.shape
consol_data.dropna(how='all',inplace=True)

### creacion conteos en la BD de eventos #####################

consol_data_solicitudes=consol_data.drop_duplicates(['year','MES','NOMBRE_USUARIO','Solicitud']).groupby(['year','MES','NOMBRE_USUARIO'])['Solicitud'].count()
consol_data_solicitudes.reset_index().sort_values(by=['year','MES','NOMBRE_USUARIO'])
consol_data_solicitudes=consol_data_solicitudes.reset_index()

consol_data_autorizaciones=consol_data.drop_duplicates(['year','MES','NOMBRE_USUARIO','Autorizacion']).groupby(['year','MES','NOMBRE_USUARIO'])['Autorizacion'].count()
consol_data_autorizaciones.reset_index().sort_values(by=['year','MES','NOMBRE_USUARIO'],inplace=True)
consol_data_autorizaciones=consol_data_autorizaciones.reset_index()

consol_data_codigo=consol_data.drop_duplicates(['year','MES','NOMBRE_USUARIO','codigo']).groupby(['year','MES','NOMBRE_USUARIO'])['codigo'].count()
consol_data_codigo.reset_index().sort_values(by=['year','MES','NOMBRE_USUARIO'],inplace=True)
consol_data_codigo=consol_data_codigo.reset_index()

##### unir con el DF de features_demograficos #####################

## la siguiente linea, permite verificar el A-B de dos grupos de Strings
set(feature_demo.NOMBRE_CLAVE.unique())-set(consol_data_solicitudes.NOMBRE_USUARIO.unique())






feature_demo['NUMERO_DE_DOCUMENTO']=feature_demo.NUMERO_DE_DOCUMENTO.astype('int').astype('str').str.strip()
consol_data_con_features=feature_demo.merge(consol_data_solicitudes,how='left',left_on='NOMBRE_CLAVE',right_on='NOMBRE_USUARIO',)

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
