import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors




def create_map(gdf):
    # Create a base map
    m = folium.Map(location=[7.25, 125.6], scrollWheelZoom=True, zoom_start=10.49)


    # Add GeoJSON to the map with colors based on category
    geojson_data = gdf.to_json()
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
        'fillColor': 'grey',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['barangay'],
            aliases=['Barangay:'],
            localize=True
        )
    ).add_to(m)

    return m

# Streamlit application
def main():
    st.title('Davao City')
    df = st.session_state.data    
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    
    col1, col2 = st.columns([3, 6])

    with col1:
        st.write("About Davao City....")


    with col2:
        # Create and display the map
        map_ = create_map(gdf)
        st_folium(map_, width=800, height=500)

if __name__ == "__main__":
    main()
