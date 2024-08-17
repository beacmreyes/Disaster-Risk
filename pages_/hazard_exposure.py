import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from folium import Choropleth
from folium.plugins import HeatMap
from branca.colormap import linear
from folium.features import GeoJsonTooltip

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from io import BytesIO
from datetime import datetime

@st.cache_data
def create_gradient_legend(min_value, max_value,color):
    # Get the original colormap
    original_cmap = plt.get_cmap(color)
    
    # Extract the colormap colors and add alpha channel
    colors = original_cmap(np.linspace(0, 1, 256))
    colors[:, -1] = 0.7  # Set the alpha channel
    
    # Create a new colormap with the modified colors
    new_cmap = LinearSegmentedColormap.from_list('modified_cmap', colors)
    
    # Create a gradient image from 0 to 1
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    
    # Create a figure and axis to display the gradient
    fig, ax = plt.subplots(figsize=(8, 1), subplot_kw=dict(xticks=[], yticks=[]))

    # Display the gradient with the modified colormap
    img = ax.imshow(gradient, aspect='auto', cmap=new_cmap)
    
    # Add color bar with legend
    cbar = plt.colorbar(img, ax=ax, orientation='horizontal', fraction=0.8, pad=0.1)
    cbar.ax.xaxis.set_label_position('top')
    
    # Adjust the color bar ticks and labels to match min and max values
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels([f'{min_value:.2f}', f'{max_value:.2f}'])

    # Convert figure to a BytesIO object
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    buf.seek(0)
    
    plt.close(fig)  # Close the figure to free up memory
    
    return buf
  
@st.fragment
def create_map(m,_gdf, feature, display_feature, min_value, max_value, color):
  
    # Add Choropleth layer to the map
    choropleth = Choropleth(
        geo_data=_gdf,
        data=_gdf,
        columns=['barangay_code', feature],
        key_on='feature.properties.barangay_code',
        fill_color=color,
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color='white'
    )
    
    for key in choropleth._children:
        if key.startswith('color_map'):
            del(choropleth._children[key])
            
    choropleth.add_to(m)
    
    # Add tooltips with Barangay and Metric Value
    tooltip = GeoJsonTooltip(
        fields=['barangay', feature],
        aliases=['Barangay:', f'{display_feature}:'],
        localize=True
    )
    # Add GeoJson to the map with tooltips and thinner lines
    folium.GeoJson(
        _gdf,
        style_function=lambda x: {
            'color': 'darkgrey',  # Line color'
            'weight': 0.5, 
        },
        tooltip=tooltip
    ).add_to(m)



    return m


# Streamlit application
features_df = pd.read_csv('data/Disaster_Risk_Flood_Hazard.csv', encoding='utf-8')
hazards = features_df.set_index('display_name').T.to_dict('dict')


def main():
    m = folium.Map(location=[7.25, 125.6], scrollWheelZoom=True, tiles='CartoDB positron', zoom_start=10.49)    
    
    df = st.session_state.data
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

    
    display_feature = st.sidebar.radio(
            "Flood Hazard:",features_df['display_name']
        )
    st.title('Davao City Flood Hazard Exposure')

    feature = hazards[display_feature]['feature']
    color = 'Reds'

    min_value = df[feature].min()
    max_value = df[feature].max()
    
    # Create and display the map
    map_ = create_map(m,gdf, feature, display_feature, min_value, max_value, color)

    col1, col2 = st.columns([3, 6])

    with col1:
        
        st.markdown("""A **hazard** is a process, phenomenon or human activity that may cause loss of life, injury or other health impacts, property damage, social and economic disruption or environmental degradation. Hazards may be natural, anthropogenic or socionatural in origin.  
                 **Hazard exposure** is the situation of people, infrastructure, housing, production capacities and other tangible human assets located in hazard-prone areas.""")
        
        st.markdown(hazards[display_feature]['caption'])
        
        st.caption(display_feature)
        # Create and display the gradient legend
        gradient_buf = create_gradient_legend(min_value, max_value,color)
        st.image(gradient_buf, use_column_width=True)
                
        
        
    with col2:
        st_folium(map_, width=800, height=500,returned_objects=[])

    st.markdown ("""
    Flood hazards consider take both the height and velocity of the water into consideration and calculates the hazard levels based on the danger they pose to people and structures. Generally, flood hazard level is estimated for an average Filipino with a height of 5\' 6\". However, since the flow velocity is also considered, areas that have shallow but fast-flowing flood waters may have a higher hazard level than that denoted by the height of the flood covering it.
    
- **Low flood hazard level** is a knee-level flood (up to 0.5m) for an average Filipino with a height of 5\' 6\"
- **Medium flood hazard level** is knee to neck level (up to 1.5m) for an average Filipino with a height of 5\' 6\"
- **High flood hazard level** is described as flood that is above the neck (above 1.5m) for an average Filipino with a height of 5\' 6\" """)
    st.markdown("""<p style="font-size: 12px;">Data Source: Project NOAH, Project CCHAIN</p>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()