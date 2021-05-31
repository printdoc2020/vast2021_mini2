import itertools
import folium.plugins as plugins
import json
import os
import folium
import geopandas as gpd
import pandas as pd
import datetime

def show_1_car_mutiple_day(car_id, gdf, map_file, latitude, longtitude, style1):
    car_id = int(car_id)
    gdf_filtered = gdf[gdf["id"] == car_id]
    gdf_filtered = gdf_filtered.sort_values(["Timestamp"])
    all_dates = sorted(gdf_filtered['Timestamp'].dt.date.unique())
    multi_list = list()
    for date in all_dates:
        tmp = gdf_filtered[gdf_filtered['Timestamp'].dt.date == date]
        multi =  list((tmp.groupby(["Timestamp"]).apply(lambda x: pd.DataFrame.to_numpy(x[["lat", "long"]]).tolist())))
        multi = list(itertools.chain(*multi))

        multi_list.append(multi)
        
   
    m = folium.Map([latitude, longtitude], zoom_start=14)
    folium.GeoJson(map_file, style_function=lambda x:style1).add_to(m)


    weight = 1  # default value
    data = multi_list # multi #gdf_filtered[["latitude", "longtitude"]].values
    index = list(map(str,all_dates)) #gdf_filtered.Timestamp.astype(str).unique().tolist(),

    for time_entry in data:
        for row in time_entry:
            row.append(weight)

    hm = plugins.HeatMapWithTime( data, index =index,min_speed= 0.5, 
                                 radius=35,
                                 auto_play=True, max_opacity=1)

    hm.add_to(m)
    m.save("html_files/my_map.html")
    return m


def show_mulple_cars_in_date_range(car_id_list, gdf, map_file, latitude, longtitude, style1, colors, date_range):
    car_id_list = list(map(int, car_id_list))
    gdf_filtered = gdf[gdf["id"].isin(car_id_list)]

    gdf_filtered = gdf_filtered[ (date_range[0] <= gdf_filtered["Timestamp"].dt.date) &  (gdf_filtered["Timestamp"].dt.date <= date_range[1])]
    
    gdf_filtered = gdf_filtered.sort_values(["Timestamp", "id"])
    multi =  list((gdf_filtered.groupby(["Timestamp"]).apply(lambda x: pd.DataFrame.to_numpy(x[["lat", "long"]]).tolist())))

   
    m = folium.Map([latitude, longtitude], zoom_start=14)
    folium.GeoJson(map_file, style_function=lambda x:style1).add_to(m)

    gdf_filtered["Timestamp"] = gdf_filtered["Timestamp"].astype(str)

    folium.GeoJson(
        gdf_filtered,
        name="Dot to locations",
        marker=folium.Circle(radius=30,  fill_opacity=1, weight=1, fill=True),
        tooltip=folium.GeoJsonTooltip(fields=["id", "Timestamp", "lat", "long"]),
        popup=folium.GeoJsonPopup(fields=["id", "Timestamp", "lat", "long"]),
    #        style_function=style_function,
        style_function=lambda x: {
            "fillColor": colors[x['properties']['id']%len(colors)],
             "color":colors[x['properties']['id']%len(colors)]
    #         "radius": (x['properties']['lines_served'])*30,
        },
        highlight_function=lambda x: {"fillOpacity": 0.8},
        zoom_on_click=True,
        ).add_to(m)


    weight = 1  # default value
    data = multi # multi #gdf_filtered[["latitude", "longtitude"]].values
    index = gdf_filtered.Timestamp.astype(str).unique().tolist(),

    for time_entry in data:
        for row in time_entry:
            row.append(weight)
    hm = plugins.HeatMapWithTime(data,   
                    min_speed=1,
                    max_speed=20,
                    speed_step=0.1,
                    overlay=True,
                    index =gdf_filtered.Timestamp.astype(str).unique().tolist(),
                    auto_play=True,  
                    radius=25,
                    min_opacity=0,
                    max_opacity=0.6)

    hm.add_to(m)
    m.save("html_files/my_map.html")
    return m

