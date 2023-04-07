import dash
import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# import from folder
from components import sidebar, geoanalysis, wine

# Import of styles and sources
estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons",'https://use.fontawesome.com/releases/v5.10.2/css/all.css', dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

# App initialization 
app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])

# App config
app.config['suppress_callback_exceptions'] = True

# App server initialization 
app.scripts.config.serve_locally = True
server = app.server


# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),
        dbc.Col([
            html.Div(id="page-content")
        ], md=10, style={"color": "#242424"}),
    ])

], fluid=True, 
    style={"padding": "0px"}, 
    className="dbc",
    )


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/geoanalysis":
        return geoanalysis.layout
    
    if pathname == "/wine":
        return wine.layout


if __name__ == '__main__':
    app.run_server(debug=True)