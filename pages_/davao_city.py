import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors



# Streamlit application
def main():
    st.title('Davao City')
    gdf = st.session_state.data    
    m = folium.Map(location=[7.25, 125.6], scrollWheelZoom=True, zoom_start=10.49)
    # geojson_data = gdf.to_json()
    folium.GeoJson(
        gdf,
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
    
    col1, col2 = st.columns([3, 6])

    with col1:
        # Display the quote
        st.write("""
        "Davao City is the regional center of Davao Region. It is the most populous city in Mindanao and the third largest city in the Philippines. Known for its bustling economic activities, urban build-up and modern amenities, Davao City is one of the most important economies in the island, and the third most important urban center in the Philippines."
        """)
        
        # Provide the citation
        st.markdown("<a href='https://philippines.travel/destinations/davao-city' target='_blank' style='font-size: 12px; text-decoration: none; color: inherit'> - Official Website of the Department of Tourism, Philippines</a>", unsafe_allow_html=True)



    with col2:
        # Create and display the map
        st_folium(m, width=800, height=500,returned_objects=[])

if __name__ == "__main__":
    main()
