# -*- coding: utf-8 -*-
"""
Created on Thu May 26 18:38:33 2022

@author: USUARIO
"""

#conda update -n base -c defaults conda
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
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer
import scipy
from scipy.stats import chi2_contingency
##### organizando rutas #########

#ruta_madre="C:/Users/relat/Documents/GitHub/Team_224/Proyecto"
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

## que quede solicitudes, autorizaciones por dia para evitar el sesgo por mayores dias en un mes

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

profesiones={'administracion de empresas':'admin_empresas',
             'administrador en servicios de la salud':'admin_servicios_salud',
             'secretaria':'secretariado',
             'asistente administrativo':'asistente_administrativo',
             'tecnico en auxiliar de enfermeria':'auxiliar_enfermeria',
             'auxiliar de enfermeria':'auxiliar_enfermeria',
             'tecnico auxiliar de enfermera':'auxiliar_enfermeria',
             'tecnico auxiliar de enfemeria':'auxiliar_enfermeria',
             'tecnico en agente  call center':'agente_call_center',
             'tecnico agente de contact center':'agente_call_center',
             'administrador en salud':'admin_servicios_salud',
             'administracion en salud':'admin_servicios_salud',
             'administrador de empresas':'admin_empresas',
             'tecnico en asistencia administrativa':'asistente_administrativo'
             }

data_agregada['PROFESION']=data_agregada['PROFESION'].replace(profesiones)

#### arreglando NIVEL ESCOLARIDAD###############

prueba=[]
for i in range(len(data_agregada['NIVEL_DE_ESCOLARIDAD'])):
    
    try:
        prueba.append(normalizar(data_agregada['NIVEL_DE_ESCOLARIDAD'][i]))
    except:
        
        prueba.append(np.nan)
   
  
data_agregada['NIVEL_DE_ESCOLARIDAD']=prueba


###### Exploratoy Data Analysis#######

## info general
data_agregada.info() ## la variables provenientes de los sueldos año a año, tienen cerca del 56% de la data dañada por falta de info de sueldos en ciertos años, 

## describe las variables numericas y categoricas
data_agg_describe_numeric=data_agregada.describe()
data_agg_describe_object=data_agregada.describe(include=['O'])


# 
# ax=sns.heatmap(corr_data, annot=True, cmap=sns.cubehelix_palette(20,  light=0.95, dark=0.15))
# ax.xaxis.tick_top
# plt.show()
#### grafica de correlacion
plt.figure(figsize=(12,10))
corr = data_agregada.corr()
ax=sns.heatmap(corr, annot=False, cmap=sns.cubehelix_palette(20,  light=0.95, dark=0.15))
ax.xaxis.tick_top
plt.show()


## graficas de visualizacion

plt.figure(figsize=(8,9))

## solicitud atendidas por year
sns.lineplot(x='year',y='Solicitud',data=data_agregada)


## solicitudes per capita atendias por year
suma_solicitudes=data_agregada.groupby('year').agg({'Solicitud': 'sum', 'NOMBRE_USUARIO': 'count'}).reset_index()
suma_solicitudes['prod_per_capita']=suma_solicitudes.Solicitud/suma_solicitudes.NOMBRE_USUARIO
sns.barplot(x='year',y='prod_per_capita',data=suma_solicitudes)


#######################################################################

# Análisis

# Se presentaton mayor número de solicitudes en el año 2016 y 2017, se ha venido disminuyendo con la puntuación más 
# baja en el 2020 esto se puede deber a impacto al COVID - 19

# La cantidad de solicitudes atendidas por Gestores de citas tiene un comportamiento similar al número de número de
# solicitudes, se presenta un incremento en el año 2016 y 2017.



## solicitudes per capita atendias por genero
suma_solicitudes_Genero =data_agregada.groupby(['year','GENERO']).agg({'Solicitud': 'sum', 'NOMBRE_USUARIO': 'count'}).reset_index()
suma_solicitudes_Genero['prod_per_capita']=suma_solicitudes_Genero.Solicitud/suma_solicitudes_Genero.NOMBRE_USUARIO
sns.barplot(x='year',y='prod_per_capita',hue='GENERO',data=suma_solicitudes_Genero)

#######################################################################

# Análisis

# En general se observa que la atención de solicitudes presentan un mayor rendimiento en los hombres en
# comparación con las mujeres.
## Por otro lado, al parecer las mujeres tecnologas lo hacen mejor, mientras que los hombres profesionales lo hacen mejor. aunque hay que mencionar
# que podemos tener patrones escondidos.
## del mismo modo al realizar una prueba de diferencia de medias, se observa queefectivamente las solicitudes por dia de los hombres es mas grand que el de las mujeres
## sin embargo, debido al sesgo de la medida, es posible que la prueba pueda dar resultados no tan creibles

sns.boxplot(x='GENERO',y='solicitudes_per_day',hue='NIVEL_DE_ESCOLARIDAD',data=data_agregada)
sns.boxplot(x='GENERO',y='solicitudes_per_day',data=data_agregada)
data_agregada.groupby('GENERO')['NIVEL_DE_ESCOLARIDAD'].value_counts()

pingouin.ttest(data_agregada[data_agregada.GENERO=='MASCULINO']['solicitudes_per_day'], data_agregada[data_agregada.GENERO=='FEMENINO']['solicitudes_per_day'],alternative='greater').iloc[0]

pingouin.qqplot(data_agregada[data_agregada.GENERO=='MASCULINO']['solicitudes_per_day'],'norm')
pingouin.qqplot(data_agregada[data_agregada.GENERO=='FEMENINO']['solicitudes_per_day'],'norm')

#######################################################################

# Análisis

# Notará que aunque la historia general muestra un mejor desempeño de lso hombres, si se segmenta por 
# año se puede ver que esto no sucede en los últimos años y que la tendencia se devuelve


sns.boxplot(hue='GENERO',x='year',y='solicitudes_per_day',data=data_agregada)
#######################################################################

# Análisis

# En general se observa que la atención de solicitudes presentan un mayor rendimiento en los hombres en
# comparación con las mujeres.

## solicitudes per capita atendias por edad
suma_solicitudes_Edad =data_agregada.groupby(['edad']).agg({'Solicitud': 'sum', 'NOMBRE_USUARIO': 'count'}).reset_index()
suma_solicitudes_Edad['prod_per_capita']=suma_solicitudes_Edad.Solicitud/suma_solicitudes_Edad.NOMBRE_USUARIO
plt.xticks(rotation=90)
sns.barplot(x='edad',y='prod_per_capita',data=suma_solicitudes_Edad)

#######################################################################

# Análisis

# Parece no haber una relacion importante entre años de experiencia, edad y solicitudes por dia

sns.scatterplot(x='years_antiguedad',y='solicitudes_per_day',hue='GENERO',data=data_agregada)
#plt.title('años de antiguedad vs solicitudes por dia')
sns.scatterplot(x='edad',y='solicitudes_per_day',hue='GENERO',data=data_agregada)


#######################################################################

# Análisis

# Aunque el ESTADO CIVIL dice que las persones en union libres tienden a ser menos aptas para procesar autorizaciones, lo que si se 
#observa es que entre mayores personas a cargo, hay una relacion cuadratica negativa con punto de inflexión en 3 personas

sns.boxplot(x='ESTADO_CIVIL',y='solicitudes_per_day',data=data_agregada)
#plt.title('años de antiguedad vs solicitudes por dia')
sns.boxplot(x='ESTRATO_SOCIAL',y='solicitudes_per_day',data=data_agregada)
sns.boxplot(x='OTRAS_PERSONAS_A_CARGO',y='solicitudes_per_day',data=data_agregada)
sns.boxplot(x='TIPO_DE_VIVIENDA',y='solicitudes_per_day',data=data_agregada)
sns.boxplot(x='CENTRO_DE_TRABAJO',y='solicitudes_per_day',data=data_agregada)
#######################################################################

# Análisis

# En general se observa que la atención de solicitudes presentan un mayor rendimiento en los hombres entre 
# el año 2016 y el 2020 en comparación con las mujeres. Sin embargo, se observa un incremento apartir del año 2021 
# y en lo que va corriendo del 2022.

#######################################################################

#######################################################################

# Análisis

# En general se observa que la atención de solicitudes presentan un mayor rendimiento en los hombres entre 
# el año 2016 y el 2020 en comparación con las mujeres. Sin embargo, se observa un incremento apartir del año 2021 
# y en lo que va corriendo del 2022.

######################################################

# Análisis

# Las personas con mayor nivel educativo que se encuentran en este cargo, viven en arriendo en su mayoria. puede ser que
#los altos niveles de endeudamiento por recurrir a un profesional y una remuneracion estandar, no les permita tener vivienda propia

prof_tipovi=pd.crosstab(data_agregada['NIVEL_DE_ESCOLARIDAD'],data_agregada['TIPO_DE_VIVIENDA'])
chi2_contingency(prof_tipovi)[1] 

######################################################

# Análisis

# Tambien se observa que las personas condiciones especiales, tienden a ser excluidas y no pueden formarse profesionalmente
## tambien hay una relacion importante entre ambas variables
prof_esp=pd.crosstab(data_agregada['NIVEL_DE_ESCOLARIDAD'],data_agregada['POBLACION_ESPECIAL'])
sns.heatmap(pd.crosstab(data_agregada['NIVEL_DE_ESCOLARIDAD'],data_agregada['POBLACION_ESPECIAL'],normalize='index'),cmap="Reds")
chi2_contingency(prof_esp)[1]


######################################################

# Análisis

# importante relacipn entre las personas profesionales y su nivel dde estrato socioeconomico
prof_ESTRATO=pd.crosstab(data_agregada['NIVEL_DE_ESCOLARIDAD'],data_agregada['ESTRATO_SOCIAL'])
sns.heatmap(pd.crosstab(data_agregada['NIVEL_DE_ESCOLARIDAD'],data_agregada['ESTRATO_SOCIAL'],normalize='columns'),cmap="Reds")
chi2_contingency(prof_ESTRATO)[1]


######################################################

# Análisis

# Debido a que los sueldos tienen una varianza relativamente baja y no se diferenica significativamente entre hombres y mujeres, 
## se hace una iputaciond e los valores faltantes

sns.kdeplot(x='Sueldo',hue='year',data=data_agregada,fill=True, common_norm=False, palette="crest",
  alpha=.5, linewidth=0
  )

sns.boxplot(y='Sueldo',x='year',hue='GENERO',data=data_agregada)

sns.boxplot(y='Sueldo',x='GENERO',data=data_agregada)


####imputacion de datos==========

imputer = KNNImputer( weights="uniform")
nueva_data=pd.DataFrame(imputer.fit_transform(data_agregada[['year','Sueldo']]),columns=['year','Sueldo_imputed'])

data_agregada['Sueldo_imputed']=nueva_data['Sueldo_imputed']


















