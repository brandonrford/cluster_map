# -*- coding: utf-8 -*-
"""clusters_map.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1S68x2Ry9LmdbiG0nswZ-HhsAzQ4T8H7X
"""

import folium #https://towardsdatascience.com/making-3-easy-maps-with-python-fb7dfb1036
import pandas as pd
import json
from folium import plugins
import math


data = pd.read_csv("data/clusters_mapdata.csv")

#set colors
colors = ['black', 'green', 'red']
data['marker_color'] = pd.cut(data['Cluster'], bins=3,  #for conditional replace https://stackoverflow.com/questions/21608228/conditional-replace-pandas
                              labels=colors)

#initialize the map
map = folium.Map(location=[10,0], tiles='OpenStreetMap', zoom_start=2) #tiles='Stamen Terrain' tiles='OpenStreetMap'

#creating legend
import branca
legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    bottom: 350px;
    left: 75px;
    width: 200px;
    height: 150px;
    z-index:9999;
    font-size:14px;
    ">
    <p><a style="color:black;font-size:40px">&#9679;</a>&emsp;Cluster 1</p>
    <p><a style="color:green;font-size:40px">&#9679;</a>&emsp;Cluster 2</p>
    <p><a style="color:red;font-size:40px">&#9679;</a>&emsp;Cluster 3</p>
</div>
<div style="
    position: fixed;
    bottom: 300px;
    left: 50px;
    width: 160px;
    height: 200px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    filter: blur(8px);
    -webkit-filter: blur(8px);
    opacity: 0.7;
    ">
</div>
{% endmacro %}
"""

legend = branca.element.MacroElement()
legend._template = branca.element.Template(legend_html)

#for each row in the data, plot the corresponding latitude and longitude on the map
for i,row in data.iterrows():
    folium.CircleMarker((row.latitude,row.longitude), 
                        radius=6, weight=1, 
                        color=row.marker_color, 
                        fill_color=row.marker_color, 
                        popup=folium.map.Popup("Cluster: " + str(row.Cluster) + "<br />Religion: " +
                                                row.religion_label + "<br />Primary Domesticated Animal: " +
                                                row.domesticated_label + "<br />Role of God(s): " +
                                                row.roleofgods_label + "<br />Animals Hunted: " +
                                                row.animalshunted_label, 
                                                min_width=250,max_width=250), 
                        tooltip=row.society_name, 
                        fill_opacity=.9).add_to(map) 

map.get_root().add_child(legend) #adds legend to the html map

#save the map as an html 
map.save('output/cluster_map.html')
map