# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 19:35:06 2024

@author: Hederson
"""

import plotly as plt
import plotly.express as px
import json
from urllib.request import urlopen
import pandas as pd

#adaptar para o python
with urlopen(‘https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
 Brazil = json.load(response) # Javascrip object notation 
Brazil

state_id_map = {}
for feature in Brazil [‘features’]:
 feature[‘id’] = feature[‘properties’][‘name’]
 state_id_map[feature[‘properties’][‘sigla’]] = feature[‘id’]
 
soybean = pd.read_csv(‘https://raw.githubusercontent.com/nayanemaia/Dataset_Soja/main/soja%20sidra.csv')
print(soybean)

fig = px.choropleth(
 soybean, #soybean database
 locations = “Estado”, #define the limits on the map/geography
 geojson = Brazil, #shape information
 color = "Produção", #defining the color of the scale through the database
 hover_name = “Estado”, #the information in the box
 hover_data =["Produção","Longitude","Latitude"],
 title = "Produtivida da soja (Toneladas)", #title of the map
 animation_frame = “ano” #creating the application based on the year
)
fig.update_geos(fitbounds = "locations", visible = False)
fig.show()

fig = px.choropleth_mapbox(
 soybean, #soybean database
 locations = “Estado”, #define the limits on the map/geography
 geojson = Brazil, #shape information
 color = "Produção", #defining the color of the scale through the database
 hover_name = “Estado”, #the information in the box
 hover_data =["Produção","Longitude","Latitude"],
 title = "Produtivida da soja (Toneladas)", #title of the map
 mapbox_style = "carto-positron", #defining a new map style 
 center={"lat":-14, "lon": -55},#define the limits that will be plotted
 zoom = 3, #map view size
 opacity = 0.5, #opacity of the map color, to appear the background
 animation_frame = “ano” #creating the application based on the year
fig.show()

plt.offline.plot(fig, filename = ‘map.html’)