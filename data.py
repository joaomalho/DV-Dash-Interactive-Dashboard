import json
import requests
import pandas as pd
from datetime import date


# ======== Geo Analysis ======== #

# =========== Data Auxiliar =========== #
path = (r'https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/wine_country.csv')
data = pd.read_csv(path)

# === Filters === #
    # Geo Analysis #
# Country
data_country = data['Country'].unique()
# Continent
data_continent = data['Region'].unique()
# Sub_region
data_sub_region = data['Sub_region'].unique()
# Metric
data_metrics = data.iloc[:, [5, 10, 11]].columns


# === Geojson === #


url = "https://raw.githubusercontent.com/joaomalho/Data-Visualization-Project/main/Data/Data_files/countries.geojson"
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
# ======== Wine Analysis ======== #

# === Filters === #

# Country
data_country_wine = data_top10['Country'].unique()
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
