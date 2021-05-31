import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import folium
import dill
import geopandas as gpd
import datetime
import folium.plugins as plugins
import numpy as np
import plot_map_for_movements
from dateutil.relativedelta import relativedelta # to add days or years


## Range selector
def add_datetime_slider():
  cols1,_ = st.beta_columns((1,2)) # To make it narrower
  format = 'MMM DD, YYYY'  # format output
  start_date = datetime.date(year=2014,month=1,day=6)
  end_date = datetime.date(year=2014,month=1,day=6) + relatitudeivedelta(days=13)  #  I need some range in the past
  max_days = end_date-start_date
  slider = cols1.slider('Select date', min_value=start_date, value=end_date ,max_value=end_date, format=format)
  return None

@st.cache
def read_data(read_ffill, time_iterval):
    with open("Abila.json", 'r') as j:
        map_file = json.loads(j.read())
    if read_ffill:
        with open(f"gps_ffill_{time_iterval}.pkl", 'rb') as f:
            gdf = dill.load(f)
    else:
        with open("gps_2.pkl", 'rb') as f:
            gdf = dill.load(f)
    return map_file, gdf



st.set_page_config(
     page_title="VAST 2021 - 2",
     page_icon="penguin",
     layout="wide",
     initial_sidebar_state="expanded",
 )
st.title('VAST 2021 - Mini Challenge 2')
st.write('Last updated: May 28, 2021')


colors_1 =["#c51b7d",
    "#de77ae",
    "#f1b6da",
    "#fde0ef",
    "#f7f7f7",
    "#e6f5d0",
    "#b8e186",
    "#7fbc41",
    "#4d9221"]

colors_2 = [
    'red',
    'blue',
    'gray',
    'darkred',
    'lightred',
    'orange',
    'beige',
    'green',
    'darkgreen',
    'lightgreen',
    'darkblue',
    'lightblue',
    'purple',
    'darkpurple',
    'pink',
    'cadetblue',
    'lightgray',
    'black'
]

style1 = {'fillColor': 'gray', 'color': 'gray'}
time_iterval = "5T" ## 5 mins
colors=colors_2
style1 = {'fillColor': 'gray', 'color': 'gray'}
latitude, longtitude = 36.07, 24.865
height, width = 770, 1500

map_file, gdf=read_data(True, time_iterval) 

mode =st.sidebar.selectbox('select mode',('1 vehicle', 'multiple vehicles'))

m = None
if mode == 'multiple vehicles':
    car_id_list = st.sidebar.multiselect(
        'Vehicle IDs:',
        list(map(str,sorted(gdf.id.unique()))),
        ["1", "5", "7"])
    date_range = st.sidebar.date_input("date range without default", [datetime.date(2014, 1, 6), datetime.date(2014, 1, 7)])
    m = plot_map_for_movements.show_mulple_cars_in_date_range(car_id_list, gdf, map_file, latitude, longtitude, style1 , colors, date_range)
elif mode == '1 vehicle':
    car_id = st.sidebar.selectbox("Vehicle ID",  list(map(str,sorted(gdf.id.unique()))), 1)
    m = plot_map_for_movements.show_1_car_mutiple_day(car_id, gdf, map_file, latitude, longtitude, style1 )


overlay_map = st.sidebar.checkbox("Overlay Tourist Map")

if overlay_map:
    folium.raster_layers.ImageOverlay(
    image="img/MC2-tourist.jpg",
    name="Tourist Map",
    bounds=[[36.045, 24.82], [36.1, 24.91]],
    opacity=0.3,
    interactive=False,
    cross_origin=False,
    zindex=1,
    alt="Tourist Map",
).add_to(m)

folium.LayerControl().add_to(m)
m.save("html_files/my_map.html")



HtmlFile = open("html_files/my_map.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code, height = height)

