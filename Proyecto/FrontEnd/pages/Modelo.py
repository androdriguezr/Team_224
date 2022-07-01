import dash
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page
from dash import html, dcc

register_page(__name__, path="/modelo")


# os.chdir('C:\Users\juliandnp\Downloads\dash-template-repo-master')
# all_data_final_model=load_model('model_selected_pipeline')
##load_model('model_selected_pipeline')## para cargar de vuelta el modelo
# age=35
# gender='FEMALE'
# is_special_population='NO APLICA'
# municipio_living='monteria'
# home_type='ARRENDADA'
# education_level='PROFESIONAL'
# PROFESION='admin_empresas'
# marital_status='SINGLE'
# total_dependants='1.0'
# ESTRATO_SOCIAL='1.0'
# years_exp_current_role=1

# new_data=datos_to_model.iloc[[0,]].copy()
# new_data=new_data.drop(columns='request_attend_per_day')
# new_data['age']=float(age)
# new_data['age2']=float(age)**2
# new_data['age3']=float(age)**3
# new_data['age4']=float(age)**4
# new_data['age5']=float(age)**5
# new_data['is_special_population']=is_special_population
# new_data['municipio_living']=municipio_living
# new_data['home_type']=home_type
# new_data['education_level']=education_level
# new_data['marital_status']=marital_status
# new_data['total_dependants']=str(total_dependants)
# new_data['ESTRATO_SOCIAL']=str(ESTRATO_SOCIAL)
# new_data['years_exp_current_role']=float(years_exp_current_role)
# new_data['PROFESION']=PROFESION

# predicted_value=predict_model(all_data_final_model, data = new_data)

# predicted_value.Label

# {'gender': array(['FEMALE', 'MALE', 'OTHER'], dtype=object),
#  'is_special_population': array(['NO APLICA', 'MADRE CABEZA DE FAMILIA', 'DESPLAZADO',
#         'VICTIVA CONFLICTO ARMADO', 'MUJER GESTANTE'], dtype=object),
#  'any_disability': array(['NO', 'no_reported'], dtype=object),
#  'MUNICIPIO_DE_RESIDENCIA': array(['monteria', 'sahagun', 'montelibano', 'planeta_rica', 'san_pelayo',
#         'cienaga_de_oro', 'cerete', 'murindo', 'NO_REPORTADO'],
#        dtype=object),
#  'home_type': array(['ARRENDADA', 'FAMILIAR', 'PROPIA', 'OTHER'], dtype=object),
#  'education_level': array(['PROFESIONAL', 'TECNICO', 'TECNOLOGO', 'OTHER'], dtype=object),
#  'PROFESION': array(['admin_empresas', 'admin_servicios_salud', 'secretariado',
#         'asistente_administrativo', 'auxiliar_enfermeria', 'OTHER',
#         'agente_call_center', 'auxiliar administrativa',
#         'tecnico auxiliar en auxiliar contable sistematizado  -- tecnico agente de contac center',
#         'secretariado y asisten administrativo',
#         'tecnico asistencia en organizacion de archivos'], dtype=object),
#  'marital_status': array(['SINGLE', 'MARRIED', 'CONSENSUAL UNION', 'DIVORCED', 'OTHER'],
#        dtype=object),
#  'total_depedants': array(['2.0', '1.0', '3.0', '0.0', '7.0', '4.0', '8.0', 'nan'],
#        dtype=object),
#  'ESTRATO_SOCIAL': array(['3.0', '1.0', '2.0', 'nan'], dtype=object)}



layout = html.Div(
    [
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H1("MODELO PREDICTOR DE PRODUCTIVIDAD CON BASE EN CARACTERISTICAS SOCIODEMOGRAFICAS"),style={'textAlign': 'center', 'color': '#7FDBFF'}, width={"size": 10, "offset": 1}))]),
        html.Hr(),
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H5("Seleccione de las listas desplegables las caracteristicas de la persona seleccionada"), style={'textAlign': 'center'},width={"size": 8, "offset": 2}))]),
        html.Hr(),
        html.H5("EDAD"),
        html.Div([dcc.Dropdown([18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65], 'EDAD', id='edad-dropdown'),    html.Div(id='edad-output-container')]),
        html.H5("GENERO"),
        html.Div([dcc.Dropdown(['MALE', 'FEMALE','OTHER'], 'GENERO', id='genero-dropdown'),    html.Div(id='genero-output-container')]),
        html.H5("Población Especial"),
        html.Div([dcc.Dropdown(['NO APLICA', 'MADRE CABEZA DE FAMILIA','DESPLAZADO','VICTIVA CONFLICTO ARMADO', 'MUJER GESTANTE'], 'Población Especial', id='poblacion-dropdown'),    html.Div(id='poblacion-output-container')]),
        html.H5("Alguna Discapacidad"),
        html.Div([dcc.Dropdown(['NO', 'no_reported'], 'Alguna Discapacidad', id='dis-dropdown'),    html.Div(id='dis-output-container')]),
        html.H5("Municipio de Residencia"),
        html.Div([dcc.Dropdown(['monteria', 'sahagun', 'montelibano', 'planeta_rica', 'san_pelayo','cienaga_de_oro', 'cerete', 'murindo', 'NO_REPORTADO'], 'Municipio Residecnia', id='mun-dropdown'),    html.Div(id='mun-output-container')]),
        html.H5("Estado Civil"),
        html.Div([dcc.Dropdown(['Soltero', 'Casado', 'Unión Libre'], 'Estado', id='est-dropdown'),    html.Div(id='est-output-container')]),
        html.H5("Tipo de Casa"),
        html.Div([dcc.Dropdown(['ARRENDADA', 'FAMILIAR', 'PROPIA', 'OTHER'], 'Tipo de Casa', id='casa-dropdown'),    html.Div(id='casa-output-container')]),
        html.H5("Nivel Academico"),
        html.Div([dcc.Dropdown(['PROFESIONAL', 'TECNICO', 'TECNOLOGO', 'OTHER'], 'Nivel Academico', id='nivel-dropdown'),    html.Div(id='nivel-output-container')]),
        html.H5("Profesión"),
        html.Div([dcc.Dropdown(['admin_empresas', 'admin_servicios_salud', 'secretariado','asistente_administrativo', 'auxiliar_enfermeria', 'OTHER','agente_call_center', 'auxiliar administrativa','tecnico auxiliar en auxiliar contable sistematizado  -- tecnico agente de contac center','secretariado y asisten administrativo',
        'tecnico asistencia en organizacion de archivos'], 'Profesión', id='pro-dropdown'),    html.Div(id='pro-output-container')]),
        html.H5("Estado Civil"),
        html.Div([dcc.Dropdown(['SINGLE', 'MARRIED', 'CONSENSUAL UNION', 'DIVORCED', 'OTHER'], 'Estado Civil', id='estado-dropdown'),    html.Div(id='estado-output-container')]),
        html.H5("Dependientes"),
        html.Div([dcc.Dropdown(['2.0', '1.0', '3.0', '0.0', '7.0', '4.0', '8.0', 'nan'], 'Dependientes', id='dep-dropdown'),    html.Div(id='dep-output-container')]),
        html.H5("Estrato Social"),
        html.Div([dcc.Dropdown(['3.0', '1.0', '2.0', 'nan'], 'Estrato', id='Est-dropdown'),    html.Div(id='Est-output-container')]),
        html.Br(),
        dbc.Button("Calcular", id="btncalcular", n_clicks=0,style={"horizontalAlign": "middle",'textAlign': 'center'}),     
        html.Hr(),
        html.Div(className="Principal",children=[dbc.Row(dbc.Col(html.H5("Resultados Obtenidos"), style={'textAlign': 'center'},width={"size": 6, "offset": 3}))]),
        html.Hr(),
        html.Br(),
        dbc.Container([dbc.Input(id="salida", placeholder="Waiting", type="text", value="Aquí aparece su resultado"),]),  
        html.Br(),
        dbc.Button("INGRESAR AL DASHBOARD", id="btndashboard",href="/dashboard", n_clicks=0,style={"horizontalAlign": "middle",'textAlign': 'center'}),   
     
    ],
)







# layout= dbc.Container([
#     dbc.Row([
#         dbc.Col([         
           
#         ])
#     ], className= "card"),
#     dbc.Row([
#         dbc.Col([
           
#         ])
#     ], className= "card"),
# ])