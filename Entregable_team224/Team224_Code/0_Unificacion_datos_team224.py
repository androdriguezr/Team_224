# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 14:23:11 2022

@author: USUARIO
"""

### MASEAR DATA====

import os
import numpy as np
import pandas as pd


os.chdir('C:/Users/USUARIO/Documents/data_bruta_DS4A')

senderos_datos=[os.path.join(os.getcwd(),x) for x in list(os.listdir()) ]

feature_demo=pd.read_excel(senderos_datos[0])

feature_demo1=pd.read_excel(senderos_datos[1])

feature_demo2=pd.read_excel(senderos_datos[2])

feature_demo3=pd.read_excel(senderos_datos[3])

feature_demo4=pd.read_excel(senderos_datos[4])

feature_demo5=pd.read_excel(senderos_datos[5])


consol_data=pd.concat([feature_demo,feature_demo1,feature_demo2,feature_demo3,feature_demo4,feature_demo5])

consol_data['Fecha']=pd.to_datetime(consol_data['Fecha'].str[0:10])
consol_data['year']=consol_data['Fecha'].dt.year

consol_data['cedula']=consol_data.cedula.astype('int').astype('str')

consol_data['Solicitud']=consol_data.Solicitud.astype('int').astype('str')


consol_data['MES']=consol_data.MES.astype('int')


consol_data_solicitudes=consol_data.drop_duplicates(['year','MES','cedula','Solicitud']).groupby(['year','MES','NOMBRE_USUARIO','cedula'])['Solicitud'].count()
consol_data_solicitudes.reset_index().sort_values(by=['year','MES','cedula'])
consol_data_solicitudes=consol_data_solicitudes.reset_index()

consol_data_autorizacion=consol_data.drop_duplicates(['year','MES','cedula','Autorizacion']).groupby(['year','MES','NOMBRE_USUARIO','cedula'])['Autorizacion'].count()
consol_data_autorizacion.reset_index().sort_values(by=['year','MES','cedula'])
consol_data_autorizacion=consol_data_autorizacion.reset_index()


consol_data_codigo=consol_data.drop_duplicates(['year','MES','cedula','codigo']).groupby(['year','MES','NOMBRE_USUARIO','cedula'])['codigo'].count()
consol_data_codigo.reset_index().sort_values(by=['year','MES','cedula'])
consol_data_codigo=consol_data_codigo.reset_index()
##listo. deme 2 minutos tengo que calentar la comida. no me demore jejeje


intermedio=consol_data_solicitudes.merge(consol_data_autorizacion[['year','MES','cedula','Autorizacion']],how='left',on=['year','MES','cedula'])

data_agregado_citas=intermedio.merge(consol_data_codigo[['year','MES','cedula','codigo']],how='left',on=['year','MES','cedula'])


data_agregado_citas.to_excel('DATA_EVENTOS_MES.xlsx', index=False)
