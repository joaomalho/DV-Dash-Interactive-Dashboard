import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd


import pdb
from dash_bootstrap_templates import ThemeChangerAIO


# ========= Settings ========= #
background_images = {
    '/geoanalysis': '/assets/vinha-roxo.avif',
    '/wine': '/assets/wine_background_barrils.avif',
}

# ========= Layout ========= #
layout = dbc.Col([
            dbc.Card([
                html.H1('Wine Analysis',className='text-info', style={'font-size': '40px','fontStyle': 'bulk', 'color': 'rgba(161, 37, 72, 1)'}),
                html.P('By Team:', className='text-info', style={'textDecoration': 'underline', 'fontStyle': 'italic','padding': '5px', 'margin': '0px', 'font-size': '20px'}),
                html.P('João Malho     | 20220696', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                html.P('Daniel Franco  | 20210719', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                html.P('Sabeen         | xxxxxxxx', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                html.P('Tomas Vicente  | xxxxxxxx', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),


# NAV section ============== #
                html.Hr(),
                dbc.Nav([
                    dbc.NavLink('Geo Analysis', href='/geoanalysis', active='exact'),               # Link to page Geo Analysis
                    dbc.NavLink('Wine Analysis', href='/wine', active='exact'),               # Link to page Geo Analysis
                ], 
                vertical=True,
                pills=True, 
                id='nav_buttons', 
                style={'margin-bottom':'10px'}
                ),    # Buttoms settings | Vertcial order | Pills is the border details
                
                ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.DARKLY})

            ], 
            outline=False,
            style={
                "padding": "10px", 
                'margin': '20px',
                'box-shadow': '0px 10px 10px 0px rgba(0, 0, 0, 1), 0px 10px 10px 0 rgba(0, 0, 0, 0.1)',
                'color': '#FFFFFF',
                "background-color": "rgba(0, 0, 0, 0.8)",
            }, id='sidebar' 
        ), 
        ], style={
                    'height': '100%',
                    'margin': '0px',
                    'padding': '0px',
                    'overflow-x': 'hidden',
                    'overflow-y': 'hidden',
                    'position': 'fixed',
                    'background-image': 'url("/assets/vinha-roxo.avif")', 'background-size': 'cover', 'background-position': 'center'}
    )

