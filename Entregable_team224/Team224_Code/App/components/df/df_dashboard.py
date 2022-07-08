import pandas as pd

df = pd.read_csv('./data/Dashboard/registros.csv', sep=';')
df['descripcion'] = df['descripcion'].replace('HEMOGRAMA IV [HEMOGLOBINA HEMATOCRITO RECUENTO DE ERITROCITOS INDICES ERITROCITARIOS LEUCOGRAMA RECUENTO DE PLAQUETA SINDICES PLAQUETARIOS Y MORFOLOGIA ELECTRONICA E HISTOGRAMA]METODO AUTOMATICO  (233)','HEMOGRAMA IV')

df2 = df.groupby(['Año','MES', 'NOMBRE_USUARIO'])['Solicitud'].count().reset_index()

df3 = df.groupby(['Año','MES', 'ORIGEN'])['Solicitud'].count().reset_index()

df4 = df.groupby(['Año','MES','NOMBRE_USUARIO', 'ORIGEN'])['Solicitud'].count().reset_index()

df5 = df.groupby(['descripcion'])['Solicitud'].count().reset_index()
df5.sort_values(by='Solicitud', ascending=False, inplace=True)
df5.reset_index(drop=True, inplace=True)
df5.rename(columns={'descripcion':'Solicitudes más frecuentes','Solicitud':'Número de solicitudes'}, inplace=True)
df5 = df5.head(10)