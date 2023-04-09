import pdb
import dash
import json
import base64
import requests
import numpy as np
import pandas as pd
from PIL import Image
from io import BytesIO
import plotly.express as px
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dateutil import relativedelta
from datetime import datetime, date
from IPython.display import display
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import ThemeChangerAIO

# =========== App =========== #

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

# =========== Data Auxiliar =========== #

# === Geo Analysis === #
path = (r'https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/wine_country.csv')
data = pd.read_csv(path)

data.rename(columns = {'Total_Wine_Consumption':'Total Wine Consumption'}, inplace = True)

# === Filters === #
    # Geo Analysis #
# Country
data_country = data['Country'].unique()
# Continents
data_continent = data['Region'].unique()
# Sub_region
data_sub_region = data['Sub_region'].unique()
# Metric
data_metrics = data.iloc[:, [5, 10, 11]].columns

# === Geojson === #
url = "https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/countries.json"
response = requests.get(url)
country_geojson = response.json()

# === Vivino === #
path1 = "https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/Vivino_scrap.xlsx"
data_vivino = pd.read_excel(path1)

    # Drop nulls
data_vivino.dropna(inplace=True)

    # Total Reveiw per country per Year
data_vivino_total_reviews_country_year = data_vivino.groupby(['Country'])['N_Classifications'].sum().reset_index()
data_vivino_total_reviews_country_year

    # Mean Reviews per country per Year
data_vivino_avg_rating_country_year = data_vivino.groupby(['Country'])['Ratings'].mean().reset_index()
data_vivino_avg_rating_country_year

# === Top 10 Countries Wine data === #
path2 = (r'https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/vivino_top_ten.csv')
data_top10 = pd.read_csv(path2)
    
    # Drop nulls
data_top10.dropna(inplace=True)

    # Data Cleaning
data_top10 = data_top10[data_top10['Year'] != 'N.V.']
data_top10['Year'] = data_top10['Year'].astype('int')

    # Additionaly
geo = data[['Country','Region','Sub_region']]
geo = geo.drop_duplicates(keep='first')
data_top10 = pd.merge(data_top10, geo, left_on='Country', right_on='Country' )

today = date.today().year
year = data_top10.loc[data_top10['Wine'] == 'Rosado de Lágrima 2020', 'Year'].values[0]

data_top10['Year Market'] = date.today().year - data_top10['Year'] 

data_top10['Wine Continent'] = data_top10['Region_y']


# === Wine Analysis Top 10=== #
# === Filters === #

# Country
data_country_wine = data_top10['Country'].unique()
# Style
data_style_wine = data_top10['Style'].unique()
# Continent
data_continent_wine = data_top10['Wine Continent'].unique()
# Sub_region
data_sub_region_wine = data_top10['Sub_region'].unique()
# Year
data_year_wine = data_top10['Year'].unique()
# Wine
data_wine = data_top10['Wine'].unique()

# Bibliography
# 1 - https://www.kaggle.com/datasets/joshuakalobbowles/vivino-wine-data-top-10-countries-exchina | Vivino data base
# 2 - https://ourworldindata.org/grapher/wine-production | Wine Production and Compsumption
# 3 - https://use.fontawesome.com/releases/v5.10.2/css/all.css | Icons
# 4 - https://datahub.io/core/geo-countries#python | ISO file all countries
# 5 - https://vivino.com | Webscrapp 


# This dictionary defines the parameters of each icon in kpi
card_icon = {
    "color": "black",
    "textAlign": "center",
    "fontSize": 60,
    "margin": "auto",
}


# ===========  Total Layout  =========== #

app.layout = dbc.Container(children=[
    
# ===========  Sidebar Layout  =========== #
    
    dbc.Row([
        dbc.Col([
            dbc.Col([
                dbc.Card([
                    html.H1('Wine Analysis',className='text-info', style={'font-size': '40px','fontStyle': 'bulk', 'color': 'rgba(161, 37, 72, 1)'}),
                    html.P('By Team:', className='text-info', style={'textDecoration': 'underline', 'fontStyle': 'italic','padding': '5px', 'margin': '0px', 'font-size': '20px'}),
                    html.P('João Malho     | 20220696', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                    html.P('Daniel Franco  | 20210719', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                    html.P('Sabeen Mubashar| 20220726', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),
                    html.P('Tomas Vicente  | 20221355', className='text-primary', style={'padding': '0px', 'margin': '0px', 'font-size': '15px'}),

    # NAV section === #
                    html.Hr(),              
                    #ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.DARKLY})

                ], 
                outline=False,
                style={
                        "padding": "10px", 
                        'margin': '20px',
                        'box-shadow': '0px 10px 10px 0px rgba(0, 0, 0, 1), 0px 10px 10px 0 rgba(0, 0, 0, 0.1)',
                        'color': '#FFFFFF',
                        "background-color": "rgba(0, 0, 0, 0.8)",
                    }, id='sidebar'), 
            ], style={
                        'height': '100%',
                        'margin': '0px',
                        'padding': '0px',
                        'overflow-x': 'hidden',
                        'overflow-y': 'hidden',
                        'position': 'fixed',
                        'background-image': 'url("/assets/vinha-roxo.avif")', 'background-size': 'cover', 'background-position': 'center'}
            )
        ], md=2),

        dbc.Col([
            
# ========= Graphs Wine Top 10 ========= # 

# =========  Layout  =========== #
        dbc.Col([

# =========  KPIs =========== # 
            dbc.Row([
                # Population
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                        html.Legend("Avg. Total Population", style={'font-size': '25px'}),                              # Title
                                        html.H5(id="p-population-geoanalysis", style={'font-size': '20px'}),           # Value and id 
                                ], color='dark',
                                    outline=False,
                                    style={"height": 100, 
                                            "padding-left": "20px", 
                                            "padding-top": "10px", 
                                            'margin-right': '10px',
                                            'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                            'color': '#FFFFFF'
                                    }
                                ),                              # Location
                                dbc.Card(
                                    html.Div(className="fa fa-wine-bottle", style=card_icon),                           # Icon
                                    style={"maxWidth": 100, 
                                        "height": 100, 
                                        "margin-left": "-10px", 
                                        'margin-right': '10px', 
                                        'backgroundColor': '#6666FF',
                                        'opacity':0.7},                      # Position of icon
                                        )
                                    ])
                        ], width=4),                                                                                    # Row occupancy

                # Consumption
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                    html.Legend("Avg. Consumption (Lt)", style={'font-size': '25px'}),
                                    html.H5(id="p-consumption-geoanalysis", style={'font-size': '20px'}),
                                        ], color='dark',
                                            outline=False,
                                            style={"height": 100, 
                                                    "padding-left": "20px", 
                                                    "padding-top": "10px", 
                                                    'margin-right': '10px',
                                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                                    'color': '#FFFFFF'
                                            }
                            ),
                                dbc.Card(
                                    html.Div(className="fa fa-wine-glass", style=card_icon), 
                                    style={"maxWidth": 100, "height": 100, "margin-left": "-10px", 'margin-right': '10px', 'backgroundColor': '#6666FF','opacity':0.7},
                                        )
                                    ])
                        ], width=4),

                # Production
                dbc.Col([
                    dbc.CardGroup([
                        dbc.Card([
                            html.Legend("Avg. Production (Lt)", style={'font-size': '25px'}),
                            html.H5(id="p-production-geoanalysis", style={'font-size': '20px'}),
                                ], color='dark',
                                    outline=False,
                                    style={"height": 100, 
                                            "padding-left": "20px", 
                                            "padding-top": "10px", 
                                            'margin-right': '10px',
                                            'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                            'color': '#FFFFFF'
                                    }
                                ),
                        dbc.Card(
                            html.Div(className="fa fa-industry", style=card_icon), 
                            style={"maxWidth": 100, "height": 100, "margin-left": "-10px", 'margin-right': '10px', 'backgroundColor': '#6666FF','opacity':0.7},
                                )])
                        ], width=4),
                    ], style={"margin": "10px", '--bs-gutter-x': '0'}),
    
# =========  Filters =========== #

            # 1st Row Filters
            dbc.Row([
                
                # Slider Filter Year
                dbc.Col([
                    dbc.Card([
                        html.Label('Date Period', style={'margin-top': '10px'}),
                        dcc.RangeSlider(
                            min= data['Year'].min(),                                                        # Min range                                                         
                            max= data['Year'].max(),                                                        # Max Range
                            value= [2010, 2019],                                # Default Range selected
                            step=1,                                                                         # Step by step selection
                            persistence=True,                                                               # will remain selected
                            persistence_type="session",                                                     # will remain selected per session
                            id='RangeSlider_Year',                                                          # Ref for coding
                            tooltip={'placement': 'bottom', 'always_visible': True},                        # Fixed tooltip
                            marks={
                                year: {"label": str(year), "style": {"writing-mode": "vertical-rl"}}        # Names / Number in each point of slider
                                for year in range(data['Year'].min(),data['Year'].max(), 5)
                                }
                                    ),
                            ], color='dark',
                                outline=False,
                                style={"height": 100, 
                                    "padding-left": "20px", 
                                    "padding-top": "5px", 
                                    'margin-right': '10px',
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'
                                    })                                                                   # Card Sizes and margins
                        ], width=12),                                                                       # Row occupancy
                    ], style={"margin": "10px", '--bs-gutter-x': '0'}),                                     # Row Margins

            # 2nd Row Filters
            dbc.Row([

                # Country Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Country", style={}),
                        dcc.Dropdown(           
                            id="dropdown-country",                                                                  # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": country, "value": country} for country in data_country],
                            value=''
                                    )           
                            ], color='dark',
                                outline=False,
                                style={"height": 80, 
                                    "padding-left": "20px", 
                                    "padding-top": "10px", 
                                    'margin-right': '10px',
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'
                                    })              # Style parameters
                        ], width=4),
                
                # Region Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Continent", style={}),
                        dcc.Dropdown(           
                            id="dropdown-continent",                                                                # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": region, "value": region} for region in data_continent],
                            value=''
                                    )           
                            ], color='dark',
                                outline=False,
                                style={"height": 80, 
                                    "padding-left": "20px", 
                                    "padding-top": "10px", 
                                    'margin-right': '10px',
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'
                                    })   
                        ], width=4), 

# Sub-Region Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Sub-Region", style={}),
                        dcc.Dropdown(           
                            id="dropdown-sub-region",                                                                # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": sub, "value": sub} for sub in data_sub_region],
                            value=''
                                    )           
                            ], color='dark',
                                outline=False,
                                style={"height": 80, 
                                    "padding-left": "20px", 
                                    "padding-top": "10px", 
                                    'margin-right': '10px',
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'
                                    })                # Style parameters
                        ], width=4),
                    ], style={"margin": "10px", '--bs-gutter-x': '0'}),

# ========= Graphs ========= # 

            # === 1st Line of graphs === #
            dbc.Card([                                                                                           # Container regard a sub group of Rows and Columns
                dbc.Row([                                                                                             # New Row
                    dbc.Col([ 
    
                        # === Metric Selection === #
                        html.P('*Select the metric for evolution analysis', style={'margin': '10px', 
                                                                                'margin-bottom':'15px', 
                                                                                'textDecoration': 'underline', 
                                                                                'fontStyle': 'italic', 
                                                                                'color': 'white'}),
                        
                        dcc.Dropdown(           
                                        id="dropdown-metric",                                                                   # Ref id for coding
                                        clearable=True,                                                                        # Able to click on x in drop cleaning data 
                                        style={"width": "80%", 'color':'#242424', 'margin':'10px'},                                                                # Occupancy of bar
                                        persistence=True,                                                                       # Remain after page refresh
                                        persistence_type="session",                                                             # Store in session
                                        multi=False,                                                                             # Ability to choose multi selections
                                        options=[{"label": metric, "value": metric} for metric in data_metrics],
                                        value='Population'
                                    ),

                        # === Map === #
                        dcc.Loading(
                                        id='loading-1', 
                                        type='default', 
                                        children=[
                                                    dcc.Graph(
                                                                id='choropleth-map',
                                                                figure={}, 
                                                                style={'padding' : '10px'})
                                                ]
                                    ),
                    ], style={'margin' : '0px'}),
                ]), 
            ], color='dark',
                    outline=False,
                    style={"height": '100%',  
                        'margin-right': '20px',
                        'margin-left': '10px',
                        'margin-top': '20px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
            ),

            # === 2nd Line of graphs === #
            dbc.Card([
                dbc.Row([                                                                                             # New Row
                    dbc.Col([ 
                        
                        # === Graph 2 === #
                        dcc.Loading(
                                        id='loading-1', 
                                        type='default', 
                                        children=[
                                                    dcc.Graph(
                                                                id='graph1_geoanalysis',
                                                                figure={}, 
                                                                style={'padding' : '10px'})
                                                ]
                                    ),
                    ], width= 6),

                    dbc.Col([
                        # === Graph 3 === #
                        dcc.Loading(
                                        id='loading-1', 
                                        type='default', 
                                        children=[
                                                    dcc.Graph(
                                                                id='sunburst',
                                                                figure={}, 
                                                                style={'padding' : '10px'})
                                                ]
                                    ),

                    ], width= 6),
                ]),
            ], color='dark',
                    outline=False,
                    style={"height": '100%',  
                        'margin-right': '20px',
                        'margin-left': '10px',
                        'margin-top': '20px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
                ),

# ========= Graphs Wine Top 10 ========= # 
# =========  Filters =========== #
            dbc.Row([
                dbc.Col([
                dbc.Card([
                    html.H1('Top 10 Wine Produtors (Countries)',className='text-info', style={'font-size': '35px',
                                                                                        'fontStyle': 'bulk', 
                                                                                        'color': 'rgba(161, 37, 72, 1)',
                                                                                        'text-align': 'center'}),
                ], color='dark',
                    outline=False,
                    style={'margin-right': '20px',
                        'margin-left': '10px',
                        'margin-top': '50px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'})
            ], md=12,),
            ]),
            
            # === 1st Line of graphs === #
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.P('*Select the Wine Name for detailed analysis', style={'margin': '10px', 
                                                                                'margin-bottom':'15px', 
                                                                                'textDecoration': 'underline', 
                                                                                'fontStyle': 'italic', 
                                                                                'color': 'white'}),
                        
                        dcc.Dropdown(           
                                        id="dropdown-wine-name",                                                                   # Ref id for coding
                                        clearable=True,                                                                        # Able to click on x in drop cleaning data 
                                        style={"width": "80%", 'color':'#242424', 'margin':'10px'},                                                                # Occupancy of bar
                                        persistence=True,                                                                       # Remain after page refresh
                                        persistence_type="session",                                                             # Store in session
                                        multi=False,                                                                             # Ability to choose multi selections
                                        options=[{"label": wine, "value": wine} for wine in data_wine],
                                        value='Vintage Port Nacional 1994'
                                    ),

                        # === Graph 1 - image === #
                        dcc.Loading(
                                    id='loading-1', 
                                    type='default', 
                                    children=[
                                        html.Div([
                                                html.Div([
                                                    html.Img(id='wine-image', src='', style={'MaxWidth': '100%','height': '300px'})
                                                ], style={'textAlign': 'center', 'padding':'25px'})
                                            ])
                                    ]
                                ),
                    ], width=7),

                    dbc.Col([
                        dbc.Card([
                            html.P('Wine Details:', className='text-info', style={'margin-top': '10px', 'font-size': '27px', 'padding-left':'10px'}),
                            dbc.Row([
                            # === Graph 2 === #
                            dcc.Loading(
                                            id='loading-1', 
                                            type='default', 
                                            children=[
                                                    html.Legend("Country", style={'font-size': '20px'}),                              # Title
                                                    html.H5(id="metric1", style={'font-size': '15px', 'margin_left':'10px'}),
                                                    ]
                                        ),
                                    ], style={'padding-left':'25px'}),
                            dbc.Row([
                            # === Graph 2 === #
                            dcc.Loading(
                                            id='loading-1', 
                                            type='default', 
                                            children=[
                                                    html.Legend("Style", style={'font-size': '20px'}),                              # Title
                                                    html.H5(id="metric2", style={'font-size': '15px'}),
                                                    ]
                                        ),
                                    ], style={'padding-left':'25px'}),
                            dbc.Row([
                            # === Graph 2 === #
                            dcc.Loading(
                                            id='loading-1', 
                                            type='default', 
                                            children=[
                                                    html.Legend("Rating", style={'font-size': '20px'}),                              # Title
                                                    html.H5(id="metric3", style={'font-size': '15px'}),
                                                    ]
                                        ),
                                    ], style={'padding-left':'25px'}),
                            dbc.Row([
                            # === Graph 2 === #
                            dcc.Loading(
                                            id='loading-1', 
                                            type='default', 
                                            children=[
                                                    html.Legend("Reviews", style={'font-size': '20px'}),                              # Title
                                                    html.H5(id="metric4", style={'font-size': '15px'}),
                                                    ]
                                        ),
                                    ], style={'padding-left':'25px'}),
                            dbc.Row([
                            # === Graph 2 === #
                            dcc.Loading(
                                            id='loading-1', 
                                            type='default', 
                                            children=[
                                                    html.Legend("Price", style={'font-size': '20px'}),                              # Title
                                                    html.H5(id="metric5", style={'font-size': '15px'}),
                                                    ]
                                        ),
                                    ], style={'padding-left':'25px'}),
                            ],color='dark',
                            outline=False, 
                            style={'margin':'10px', 
                                    'margin-top':'90px',
                                    'margin-bottom':'10px', 
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'}),
                    ], width= 5),
                ]),
            ], color='dark',
                    outline=False,
                    style={"height": '100%',  
                        'margin-right': '20px',
                        'margin-left': '10px',
                        'margin-top': '20px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
                ),
            
            # 1st Row Filters
            dbc.Row([

                # Style Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Wine Style", style={}),
                        dcc.Dropdown(           
                            id="dropdown-style-wine",                                                                  # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": style, "value": style} for style in data_style_wine],
                            value=''
                                    )           
                            ], color='dark',
                                outline=False,
                                style={"height": 80, 
                                    "padding-left": "20px", 
                                    "padding-top": "10px", 
                                    'margin-right': '10px',
                                    'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                                    'color': '#FFFFFF'
                                    })              # Style parameters
                        ], width=12),
            
                    ], style={"margin": "10px",
                            '--bs-gutter-x': '0',
                            'margin-top': '30px'}),


            # === 2rd Line of graphs === #
            dbc.Card([
                dbc.Row([                                                                                             # New Row
                    dbc.Col([ 
                        
                        # === Graph 3 === #
                        dcc.Loading(
                                        id='loading-1', 
                                        type='default', 
                                        children=[
                                                    dcc.Graph(
                                                                id='graph3_winerating_wine',
                                                                figure={}, 
                                                                style={'padding' : '10px'})
                                                ]
                                    ),
                    ], width= 12),
                ]),
            ], color='dark',
                    outline=False,
                    style={"height": '100%',  
                        'margin-right': '20px',
                        'margin-left': '10px',
                        'margin-top': '10px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
                ),

    ]),
        ], md=10),
    ])

], fluid=True, 
    style={"padding": "0px",
        'color':'#242424',
        "background-color": "rgba(0, 0, 0, 0.8)"},
    className="dbc",
    )

# =========  Callbacks Geo analysis  =========== #

# Graph 1 - choropleth-map
@app.callback(
# Data Filter Callbacks
    Output('choropleth-map', 'figure'),                         # We want to affect "graph1" component "figure"
    [
        Input('dropdown-country', 'value'),
        Input('dropdown-continent', 'value'),                   # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-sub-region', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('RangeSlider_Year', 'value'),
        Input('dropdown-metric', 'value')
    ]
)

def update_graph_1(countries, continents, sub_regions, year, metric):

    # In case of no selection return an Image ?????
    if len(metric) <= 0:
        return go.Figure()

    countries = list(countries) if countries else []
    continents = list(continents) if continents else []
    sub_regions = list(sub_regions) if sub_regions else []
    #metric = list(metric) if metric else []                                    # This is only required when dropdow tool have multiple choice possibility

    # Dataset filter according to the filter dropboxs
    filtered_df = data[
        (data['Country'].isin(countries) if countries else True) &
        (data['Region'].isin(continents) if continents else True) &
        (data['Sub_region'].isin(sub_regions) if sub_regions else True) &
        (data['Year'] >= year[0]) &
        (data['Year'] <= year[1])]

    # Group the data by location and aggregate the color values ||| MEAN
    grouped_data = filtered_df.groupby(['ISO_Code','Country','Year','Sub_region','Region'])[metric].mean().reset_index()

    fig = go.Figure()

    fig = px.choropleth_mapbox(
                            grouped_data,                                                                                                                        # dataset filter
                            locations='ISO_Code',                                                                                                               # ISO code location
                            geojson=country_geojson,
                            featureidkey='properties.ISO_A3',
                            color=metric,                                                                                                                 # Feature that change color
                            center={'lat': 39.03291112993306, 'lon': -9.078044878535563},                                                                       # center
                            color_continuous_scale='Redor',                                                                                                     # Scale color
                            opacity=0.4, 
                            hover_name='Country', # specify the column name of the country names you want to display on hover
                            hover_data={metric: True}, # specify the columns you want to display on hover
                            zoom=3,                                                                                                                             # Zoom view 
                        )
    
    fig.update_layout(
        plot_bgcolor='#242424',
        paper_bgcolor='#242424',
        mapbox_style='carto-darkmatter',                                                                                                                         # Style theme
        autosize=True,                                                                                                                                           # Scale the size automatically    
        margin=dict(l=0, r=0, t=0, b=0),                                                                                                                    # Map margin   
        showlegend=False,
        coloraxis_colorbar={
                            'tickfont': {'color': 'white','size': 12}
                            },   
        )


    return fig
    
# Graph  - graph1_geoanalysis
@app.callback(

# Data Filter Callbacks
    Output('graph1_geoanalysis', 'figure'),                         # We want to affect "graph1" component "figure"
    [
        Input('dropdown-country', 'value'),
        Input('dropdown-continent', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-sub-region', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('RangeSlider_Year', 'value'),
        Input('dropdown-metric', 'value'),
    ]
)

def update_graph_2(countries, continents, sub_regions, year, metric):

    countries = list(countries) if countries else []
    continents = list(continents) if continents else []
    sub_regions = list(sub_regions) if sub_regions else []
    
    # In case of no selection return an Image ?????
    if not any([metric]):
        return go.Figure()
        
    # Dataset filter according to the filter dropboxs
    filtered_df = data[
        (data['Country'].isin(countries) if countries else True) &
        (data['Region'].isin(continents) if continents else True) &
        (data['Sub_region'].isin(sub_regions) if sub_regions else True) &
        (data['Year'] >= year[0]) &
        (data['Year'] <= year[1])]
    
    fig2 = go.Figure(layout={'template':'plotly_dark'})
    
    if len(countries) > 0:
        for country in countries:
            country_filtered_df = filtered_df[filtered_df['Country'] == country]
            total_metric_by_year = country_filtered_df.groupby('Year')[metric].sum()
            mean_metric_by_year = country_filtered_df.groupby('Year')[metric].sum().mean()
            fig2.add_trace(
                    go.Scatter(
                                x=total_metric_by_year.index, 
                                y=total_metric_by_year.values,
                                mode='lines+markers',
                                marker=dict(size=10),
                                name=country
                            ))
            
            # Add a horizontal line for the mean value
            fig2.add_shape(
                        # Line Horizontal
                        type="line",
                        x0=total_metric_by_year.index.min(),
                        y0=mean_metric_by_year,
                        x1=total_metric_by_year.index.max(),
                        y1=mean_metric_by_year,
                        line=dict(color='red', width=2, dash='dash'),
                        name='Mean'
                    )

    elif len(continents) > 0:
        for continent in continents:
            continent_filtered_df = filtered_df[filtered_df['Region'] == continent]
            total_metric_by_year = continent_filtered_df.groupby('Year')[metric].sum()
            mean_metric_by_year = continent_filtered_df.groupby('Year')[metric].sum().mean()
            fig2.add_trace(
                    go.Scatter(
                                x=total_metric_by_year.index, 
                                y=total_metric_by_year.values,
                                mode='lines+markers',
                                marker=dict(size=10),
                                name=continent
                            ))
            # Add a horizontal line for the mean value
            fig2.add_shape(
                        # Line Horizontal
                        type="line",
                        x0=total_metric_by_year.index.min(),
                        y0=mean_metric_by_year,
                        x1=total_metric_by_year.index.max(),
                        y1=mean_metric_by_year,
                        line=dict(color='red', width=2, dash='dash'),
                        name='Mean'
                    )
            
    elif len(sub_regions) > 0:
        for sub_region in sub_regions:
            sub_region_filtered_df = filtered_df[filtered_df['Sub_region'] == sub_region]
            total_metric_by_year = sub_region_filtered_df.groupby('Year')[metric].sum()
            mean_metric_by_year = sub_region_filtered_df.groupby('Year')[metric].sum().mean()
            
            fig2.add_trace(
                    go.Scatter(
                                x=total_metric_by_year.index, 
                                y=total_metric_by_year.values,
                                mode='lines+markers',
                                marker=dict(size=10),
                                name=sub_region
                            ))
            # Add a horizontal line for the mean value
            fig2.add_shape(
                        # Line Horizontal
                        type="line",
                        x0=total_metric_by_year.index.min(),
                        y0=mean_metric_by_year,
                        x1=total_metric_by_year.index.max(),
                        y1=mean_metric_by_year,
                        line=dict(color='red', width=2, dash='dash'),
                        name='Mean'
                    )
    else:
        # Dataset filter according to the filter dropboxs
        filtered_df = data[
                            (data['Year'] >= year[0]) & 
                            (data['Year'] <= year[1])
                        ]
        total_metric_by_year = filtered_df.groupby('Year')[metric].sum()
        mean_metric_by_year = filtered_df.groupby('Year')[metric].sum().mean()
        # Add a horizontal line for the mean value
        fig2.add_shape(
                    # Line Horizontal
                    type="line",
                    x0=total_metric_by_year.index.min(),
                    y0=mean_metric_by_year,
                    x1=total_metric_by_year.index.max(),
                    y1=mean_metric_by_year,
                    line=dict(color='red', width=2, dash='dash'),
                    name='Mean'
                )
        
        fig2.add_trace(
                go.Scatter(
                            x=total_metric_by_year.index, 
                            y=total_metric_by_year.values,
                            mode='lines+markers',
                            marker=dict(size=10),
                            name='Total'
                        ))
            
    fig2.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        autosize=True,
        margin=dict(l=10, r=10, t=80, b=10),
        yaxis_title=f'Total {metric}',
        title=dict(text=f'Total {metric} per year evolution', x=0.5, y=0.95, xanchor='center', yanchor='top',font=dict(size=20, color='#66B2FF')),
        xaxis=dict(title='Year', dtick=1),
        showlegend=True
        )
    
    return fig2

# Graph  - Sunburst
@app.callback(

# Data Filter Callbacks
    Output('sunburst', 'figure'),                         # We want to affect "graph1" component "figure"
    [
        Input('dropdown-country', 'value'),
        Input('dropdown-continent', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-sub-region', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('RangeSlider_Year', 'value'),
        Input('dropdown-metric', 'value'),
    ]
)

def update_graph_3(countries, continents, sub_regions, year, metric):

    # In case of no selection return an Image ?????
    if len(metric) <= 0:
        return go.Figure()

    countries = list(countries) if countries else []
    continents = list(continents) if continents else []
    sub_regions = list(sub_regions) if sub_regions else []
    #metric = list(metric) if metric else []

    # Dataset filter according to the filter dropboxs
    filtered_df = data[
        (data['Country'].isin(countries) if countries else True) &
        (data['Region'].isin(continents) if continents else True) &
        (data['Sub_region'].isin(sub_regions) if sub_regions else True) &
        (data['Year'] >= year[0]) &
        (data['Year'] <= year[1])]

    # Group the data by location and aggregate the color values ||| MEAN
    group_df = filtered_df.groupby(['ISO_Code','Country','Year','Sub_region','Region'])[metric].mean().reset_index()
    
    fig = px.sunburst(group_df, 
                    path=['Region', 'Sub_region', 'Country'], 
                    values=metric,
                    hover_data={'Region': True, 
                                'Sub_region': True, 
                                'Country': True,
                                metric: ':,.2f'},
                    custom_data=['Region', 'Sub_region', 'Country', metric])
                    
    fig.update_traces(hovertemplate='<b>%{label}</b><br>' +
                                'Region: %{customdata[0]}<br>' +
                                'Sub-region: %{customdata[1]}<br>' +
                                'Country: %{customdata[2]}<br>' +
                                f'{metric}: %{{customdata[3]:,.2f}}')
    
    layout = {'template': 'plotly_dark'}
    
    fig.update_layout(layout)

    fig.update_layout(paper_bgcolor='#242424',
                plot_bgcolor='#242424',
                autosize=True,
                title=dict(text=f'Total {metric} distribution', 
                x=0.5, 
                y=0.95, 
                xanchor='center', 
                yanchor='top',
                font=dict(size=20, color='#66B2FF')))

    return fig


# ======= KPIs Callbacks ======= #

# KPIs 
@app.callback(

# Data Filter Callbacks
    Output('p-population-geoanalysis', 'children'),                         # We want to affect "graph1" component "figure"
    Output('p-consumption-geoanalysis', 'children'),                         # We want to affect "graph1" component "figure"
    Output('p-production-geoanalysis', 'children'),                         # We want to affect "graph1" component "figure"                         # We want to affect "graph1" component "figure"
    [
        Input('dropdown-country', 'value'),
        Input('dropdown-continent', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-sub-region', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('RangeSlider_Year', 'value'),
    ]
)

def update_kpi_sales(countries, continents, sub_regions, year):

    countries = list(countries) if countries else []
    continents = list(continents) if continents else []
    sub_regions = list(sub_regions) if sub_regions else []

    # Dataset filter according to the filter dropboxs
    filtered_df = data[
        (data['Country'].isin(countries) if countries else True) &
        (data['Region'].isin(continents) if continents else True) &
        (data['Sub_region'].isin(sub_regions) if sub_regions else True) &
        (data['Year'] >= year[0]) &
        (data['Year'] <= year[1])]
    
    # KPIs Values
    Population = "# {:,.2f}".format(filtered_df.groupby('Year')['Population'].sum().mean())
    consumption = "Lt {:,.2f}".format(filtered_df.groupby('Year')['Total Wine Consumption'].sum().mean())
    production = "Lt {:,.2f}".format(filtered_df.groupby('Year')['Production (liters)'].sum().mean())
    
    return [Population,
            consumption,
            production,
            ]


# =========  Callbacks Wine top 10  =========== #

# Graph 1 - image
@app.callback(
# Data Filter Callbacks
    Output('wine-image', 'src'),                         # We want to affect "graph1" component "figure"
    [
    Input('dropdown-wine-name', 'value')
    ]
)

def update_image(wine):
    
    if not any([wine]):
        return ''
    else:
        # Get the URL of the wine image
        query = wine + " wine"
        url = "https://www.google.com/search?q=" + query + "&tbm=isch"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_url = soup.find_all('img')[1]['src']

        # Return the image URL
        return img_url
    
# Graph 2 - detail_wine
@app.callback(

# Data Filter Callbacks
    Output('metric1', 'children'),                         
    Output('metric2', 'children'),                         
    Output('metric3', 'children'),                         
    Output('metric4', 'children'),                         
    Output('metric5', 'children'),                                       
    [
    Input('dropdown-wine-name', 'value')
    ]
)

def update_wine_details(wine):

    if not any([wine]):
        return ['No wine selected','No wine selected',0,0,0]
    else:
        # Dataset filter according to the filter dropboxs
        wine_details = data_top10[data_top10['Wine'] == wine].iloc[0]
        
        # KPIs Values
        Country = wine_details['Country']
        Style = wine_details['Style']
        Rating = "{:,.2f}".format(wine_details['Rating'])
        Reviews = "# {:,.2f}".format(wine_details['Reviews'])
        Price = "€ {:,.2f}".format(wine_details['Price'])
        
        return [Country,
                Style,
                Rating,
                Reviews,
                Price,
                ]

# Graph 3 - graph3_winerating_wine
@app.callback(

# Data Filter Callbacks
    Output('graph3_winerating_wine', 'figure'),                         # We want to affect "graph1" component "figure"
    [
        Input('dropdown-style-wine', 'value'),]
    )

def update_graph_3(style):

    style = list(style) if style else []
    
    if not any([style]):
        filtered_df = data_top10.copy()
        
        average_reviews = filtered_df.groupby('Country')['Reviews'].mean()
        average_price = filtered_df.groupby('Country')['Price'].mean()
        average_rating = filtered_df.groupby('Country')['Rating'].mean()
        Country_unique = filtered_df.groupby('Country', as_index=False)['Rating'].count()['Country']
        
        fig = px.scatter(filtered_df, x= average_price, y=average_rating,
                        size=average_reviews, color=Country_unique, hover_name=Country_unique,
                        log_x=True, facet_col_wrap=1)
        
    else:     
        filtered_df = data_top10[
            (data_top10['Style'].isin(style) if style else True)]

        average_reviews = filtered_df.groupby('Country')['Reviews'].mean()
        average_price = filtered_df.groupby('Country')['Price'].mean()
        average_rating = filtered_df.groupby('Country')['Rating'].mean()
        Country_unique = filtered_df.groupby('Country', as_index=False)['Rating'].count()['Country']

        
        fig = px.scatter(filtered_df, x= average_price, y=average_rating,
                        size=average_reviews, color=Country_unique, hover_name=Country_unique,
                        log_x=True, facet_col_wrap=1)
            
    layout = {'template': 'plotly_dark'}

    fig.update_layout(layout)    

    fig.update_layout(
                    xaxis_title='Average Price',
                    yaxis_title='Average Rating',
                    showlegend=True,
                    height=400,
                    margin=dict(l=20, r=20, t=80, b=20),
                    autosize=True,
                    paper_bgcolor='#242424',
                    plot_bgcolor='#242424',
                    title=dict(
                        text='Wine Reviews vs Price per Country',
                        x=0.5,
                        y=0.95,
                        xanchor='center',
                        yanchor='top',
                        font=dict(size=20, color='#66B2FF'),
                    ),
                )
    
    fig.update_traces(
                    hovertemplate='<b>%{hovertext}</b><br><br>' +
                                'Avg. of Price: $%{x:.2f}<br>' +
                                'Avg. of Rating: %{y:.2f}<br>' +
                                'Avg. # of Reviews: %{marker.size:.2f}<br>' +
                                '<extra></extra>',
                    hovertext=Country_unique,
                    name='Country'
                )
        
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)   
