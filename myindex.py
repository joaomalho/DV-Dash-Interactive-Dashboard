import dash
import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# import from folder
from components import sidebar, geoanalysis, wine
from app import *

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