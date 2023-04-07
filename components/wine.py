import dash
import base64
import requests
import numpy as np
import pandas as pd
from dash import dcc
from PIL import Image
from dash import html
from io import BytesIO
import pandas_ta as pta
from datetime import date
from dash import dash_table
import plotly.express as px
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dateutil import relativedelta
from IPython.display import display
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output

from data import *


# This dictionary defines the parameters of each icon in kpi
card_icon = {
    "color": "black",
    "textAlign": "center",
    "fontSize": 60,
    "margin": "auto",
}

# =========  Layout  =========== #
layout = dbc.Col([

# =========  Filters =========== #

            # 1st Row Filters
            dbc.Row([

                # Country Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Wine Country", style={}),
                        dcc.Dropdown(           
                            id="dropdown-country-wine",                                                                  # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": country, "value": country} for country in data_country_wine],
                            value='Portugal'
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
                        ], width=3),
                
                # Region Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Wine Continent", style={}),
                        dcc.Dropdown(           
                            id="dropdown-continent-wine",                                                                # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": region, "value": region} for region in data_continent_wine],
                            value='Europe'
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
                        ], width=3), 
                
                # Year Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Wine Year", style={}),
                        dcc.Dropdown(           
                            id="dropdown-year-wine",                                                                # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": year, "value": year} for year in data_year_wine],
                            value='1994'
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
                        ], width=3), 

# Sub-Region Filter    
                dbc.Col([
                    dbc.Card([
                        html.Label("Wine Sub-Region", style={}),
                        dcc.Dropdown(           
                            id="dropdown-sub-region-wine",                                                                # Ref id for coding
                            clearable=True,                                                                         # Able to click on x in drop cleaning data 
                            style={"width": "100%", 'color':'#242424'},                                                                # Occupancy of bar
                            persistence=True,                                                                       # Remain after page refresh
                            persistence_type="session",                                                             # Store in session
                            multi=True,                                                                             # Ability to choose multi selections
                            options=[{"label": sub, "value": sub} for sub in data_sub_region_wine],
                            value='Southern Europe'
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
                        ], width=3),
                    ], style={"margin": "10px", '--bs-gutter-x': '0'}),

# ========= Graphs ========= # 

            # === 1st Line of graphs === #
            dbc.Card([
                dbc.Row([
                    html.H1('10 Biggest Wine Producing Countries (ex-China)',className='text-info', style={'font-size': '35px',
                                                                                        'fontStyle': 'bulk', 
                                                                                        'color': 'rgba(161, 37, 72, 1)',
                                                                                        'text-align': 'center'}),
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
                            ], style={'margin':'10px', 
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
                        'margin-left': '30px',
                        'margin-top': '20px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
                ),
            
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
                        'margin-top': '20px',
                        'box-shadow': '0 10px 10px 0 rgba(0, 0, 0, 1), 0 10px 10px 0 rgba(0, 0, 0, 1)',
                        'color': '#FFFFFF'}
                ),
            ])
# =========  Callbacks  =========== #


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
        Input('dropdown-country-wine', 'value'),
        Input('dropdown-continent-wine', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-sub-region-wine', 'value'),                  # The filter that trigger this change is ID = 'dropdown-country' the component 'value' | Much inputs as filters
        Input('dropdown-year-wine', 'value')]
    )

def update_graph_3(countries, continents, sub_regions, year):

    countries = list(countries) if countries else []
    continents = list(continents) if continents else []
    sub_regions = list(sub_regions) if sub_regions else []
    year = list(year) if year else []

    if not any([countries, continents, sub_regions, year]):
        filtered_df = data_top10.copy()
    else:
        filtered_df = data_top10[
            (data_top10['Country'].isin(countries) if countries else True) &
            (data_top10['Wine Continent'].isin(continents) if continents else True) &
            (data_top10['Sub_region'].isin(sub_regions) if sub_regions else True) &
            (data_top10['Year'].isin(year) if year else True)]

    fig = px.scatter(filtered_df, x='Price', y="Rating",
            size="Reviews", color="Wine Continent", hover_name="Wine",
            log_x=True, facet_col_wrap=1)

    layout = {'template': 'plotly_dark'}

    fig.update_layout(layout)    

    fig.update_layout(
        xaxis_title='Price',
        yaxis_title='Reviews',
        showlegend=True,
        height=400,
        margin=dict(l=20, r=20, t=80, b=20),
        autosize=True,
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        title=dict(
            text='Wine Reviews vs Price by Country',
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            font=dict(size=20, color='#66B2FF'),
        ),
    )

    return fig
