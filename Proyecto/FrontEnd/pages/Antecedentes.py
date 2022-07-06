#libraries
from dash import html
import dash_bootstrap_components as dbc
from dash_labs.plugins.pages import register_page

# dash-labs plugin call, menu name and route
register_page(__name__, path="/antecedentes")

from components.markdown.markformat import markformat

file1 = open('./data/mdsamples/story1.md',encoding='utf-8')
file2 = open('./data/mdsamples/story2.md',encoding='utf-8')

texto1  = markformat('Problemática', file1.read())
texto2  = markformat('Objetivos', file2.read())

# specific layout for this page
layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                 html.H2(['Perfilamiento del personal en el proceso de atención al usuario para futuros procesos de selección'],id="div_title_maps", style={'textAlign': 'center', 'color':'#0380C4'}),
                 html.Hr()
            ], lg=12), 
        ]),

        dbc.Row([
            dbc.Col([
                 texto1.show()
            ], lg=4,style={'textAlign': 'justify',"font-size": "20px"}), 
            dbc.Col([ ], lg=1),
            dbc.Col([html.Img(src='/assets/salud.png',className="img-fluid")
            ], lg=6),
        ]),

        dbc.Row([
            dbc.Col([
                 texto2.show()
            ], lg=4,style={'textAlign': 'justify',"font-size": "20px"}), 
            dbc.Col([ ], lg=1),
            dbc.Col([html.Img(src='/assets/reclu.png',className="img-fluid")
            ], lg=6), 
        ]),        
    ]
)