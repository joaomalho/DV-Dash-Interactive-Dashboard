import dash
import numpy as np
import pandas as pd
from dash import dcc
from dash import html
import pandas_ta as pta
from dash import dash_table
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output

from data import *
from app import app


# This dictionary defines the parameters of each icon in kpi
card_icon = {
    "color": "black",
    "textAlign": "center",
    "fontSize": 60,
    "margin": "auto",
}

# =========  Layout  =========== #
layout = dbc.Col([

# =========  KPIs =========== # 
            dbc.Row([
                # Population
                dbc.Col([
                        dbc.CardGroup([
                                dbc.Card([
                                        html.Legend("Total Population", style={'font-size': '25px'}),                              # Title
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
                                    html.Legend("Consumption (Lt)", style={'font-size': '25px'}),
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
                            html.Legend("Production (Lt)", style={'font-size': '25px'}),
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
                            value= [data['Year'].min(), data['Year'].max()],                                # Default Range selected
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

            ])
# =========  Callbacks  =========== #

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

    # Group the data by location and aggregate the color values
    grouped_data = filtered_df.groupby(['ISO_Code', 'Country'])[metric].sum().reset_index()

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

    # In case of no selection return an Image ?????
    if not any([metric]):
        fig = go.Figure()
        return fig

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
    
    fig2 = go.Figure(layout={'template':'plotly_dark'})
    
    if len(countries) > 0:
        for country in countries:
            country_filtered_df = filtered_df[filtered_df['Country'] == country]
            total_metric_by_year = country_filtered_df.groupby('Year')[metric].sum()
            mean_metric_by_year = country_filtered_df[metric].mean()
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

    else:
        total_metric_by_year = filtered_df.groupby('Year')[metric].sum()
        mean_metric_by_year = filtered_df[metric].mean()
        
        fig2.add_trace(
                go.Scatter(
                            x=total_metric_by_year.index, 
                            y=total_metric_by_year.values,
                            mode='lines+markers',
                            marker=dict(size=10), #color="MediumPurple"
                            name='Total',
                            showlegend=True
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
        
    fig2.update_layout(
        paper_bgcolor='#242424',
        plot_bgcolor='#242424',
        autosize=True,
        margin=dict(l=10, r=10, t=80, b=10),
        yaxis_title=f'Total {metric}',
        title=dict(text=f'Total {metric} per year evolution', x=0.5, y=0.95, xanchor='center', yanchor='top',font=dict(size=20, color='#66B2FF')),
        xaxis=dict(title='Year', dtick=1)
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

    fig = px.sunburst(filtered_df, 
                    path=['Region', 'Sub_region', 'Country'], 
                    values=metric,
                    hover_data={'Region': True, 
                                'Sub_region': True, 
                                'Country': True, metric: ':,.2f'})

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
    Population = "# {:,.2f}".format(filtered_df['Population'].sum())
    consumption = "Lt {:,.2f}".format(filtered_df['Total_Wine_Consumption'].sum())
    production = "Lt {:,.2f}".format(filtered_df['Production (liters)'].sum())
    
    return [Population,
            consumption,
            production,
            ]
