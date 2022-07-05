import pandas as pd

df = pd.read_csv('./data/Dashboard/registros.csv', sep=';')

df2 = df.groupby(['Año','MES', 'NOMBRE_USUARIO'])['Solicitud'].count().reset_index()

df3 = df.groupby(['Año','MES', 'ORIGEN'])['Solicitud'].count().reset_index()