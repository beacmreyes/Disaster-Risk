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
        st.write(r"""
        Davao City, a highly urbanized dity in Davao del Sur, has a total land area of 2,443.61 square kilometers making it the largest city in the Philippines in terms of land area. It is composed of 1,776,949 people according to the 2020 census and is the third-most populous city in the Philippines after Quezon City and Manila. The city is an independently-governed city. it is divided into three (3) congressional districts, which are subdivided into 11 administrative districts with a total of 182 barangays.
        """)
        st.write("""
        Davao City, despite its significant urban development and growth, is prone to flooding. Its geographical features and heavy rainfall contribute to this vulnerability, particularly during the rainy season. In July 2024, heavy rainfall caused by a southwest monsoon exacerbated by a low-pressure area displaced over 200 families in five villages, namely Buhangin, Cabantian, Angliongto, Panacan, and Sasa.
        """)
        
        # # Provide the citation
        # st.markdown("<a href='https://www.davaocity.gov.ph' target='_blank' style='font-size: 12px; text-decoration: none; color: inherit'> - Official Website of Davao City</a>", unsafe_allow_html=True)



    with col2:
        # Create and display the map
        st_folium(m, width=800, height=500,returned_objects=[])

if __name__ == "__main__":
    main()
