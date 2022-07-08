import dash
from dash import html
import dash_labs as dl
import dash_bootstrap_components as dbc
import os
from callbacks import register_callbacks


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY], update_title='Cargando...'
)

app.config.suppress_callback_exceptions=True

navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Inicio", href="/",className="mb-3")),
    dbc.DropdownMenu(
        [
            
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Estructura",
    ),
    ],
    brand="Medicina Integral",
    color="primary",
    dark=True,
    className="mb-5",
)

footer = dbc.Row([ 
            html.Img(src='/assets/DS4A_Colombia.svg', height='100px')
            #html.Img(src='/assets/Logo_empresa.png', height='70px')                     
            ], justify='center')



app.layout = dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
        footer

    ],
    className="dbc",
    fluid=True,
)

register_callbacks(app)


server = app.server


if __name__ == "__main__":
    port = os.environ.get('dash_port')
    debug = os.environ.get('dash_debug')
    app.run_server(debug=False, host="0.0.0.0", port=80)