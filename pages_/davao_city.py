import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors
import plotly.graph_objects as go



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
        
        
        city_rainfall_df = pd.read_csv('data/city_rainfall.csv')
        # Convert 'date' column to datetime
        city_rainfall_df['date'] = pd.to_datetime(city_rainfall_df['date'])
        
        city_rainfall_df['month'] = city_rainfall_df['date'].dt.strftime('%b')  # Short month name (Jan, Feb, Mar, etc.)
        city_rainfall_df = city_rainfall_df.set_index('month')
        
        # Create the Plotly figure
        fig = go.Figure()
    
        # Add a bar trace
        fig.add_trace(go.Line(
            x=city_rainfall_df.index,
            y=city_rainfall_df['pr_norm'],
            marker=dict(color='blue')
        ))
        
        # Update layout
        fig.update_layout(
            title='Accumulated Monthly Normal Rainfall (mm) for the Period 1991-2020',
            # xaxis_title='Month',
            # yaxis_title='Accumulated Rainfall (mm)',
            xaxis=dict(
                tickmode='array',
                tickvals=city_rainfall_df.index,  # Set tick values to the months
                ticktext=city_rainfall_df.index   # Set tick text to month names
            ),
            xaxis_title_font_size=14,
            yaxis_title_font_size=14,
            title_font_size=16,
        )
        
        # Display the Plotly plot in Streamlit
        st.plotly_chart(fig)
        
        
        # Create the Plotly figure


if __name__ == "__main__":
    main()
