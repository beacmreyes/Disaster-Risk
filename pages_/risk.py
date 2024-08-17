import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors
import plotly.graph_objects as go






category_colors = {
    'Low': 'rgba(40, 167, 69, 0.7)',    # Green with 50% opacity
    'Medium': 'rgba(255, 165, 0, 0.7)', # Orange with 70% opacity
    'High': 'rgba(255, 0, 0, 0.7)',     # Red with 80% opacity
}



@st.fragment()
def create_donut_chart(df, category_col):   
    # Define the desired order
    category_order = ['Low', 'Medium', 'High']

    # Compute counts for each category
    category_counts = df[category_col].value_counts()

    # Reorder categories based on predefined order
    ordered_categories = pd.Categorical(category_counts.index, categories=category_order, ordered=True)
    category_counts = category_counts.reindex(ordered_categories.categories)

    # Create a donut chart using Plotly
    fig = go.Figure(data=[go.Pie(
        labels=category_counts.index,
        values=category_counts,
        hole=0.7,  # Create a hole in the center for the donut chart
        textinfo='percent',
        hoverinfo='label+value+percent',  # Show label, value, and percentage on hover
        marker=dict(
            colors=[category_colors.get(label, '#000000') for label in category_counts.index],  # Get colors from the map
            line=dict(color='white', width=2),
        )
    )])

    # Update layout to center the total count inside the donut
    total_count = category_counts.sum()
    fig.update_layout(
        title_text="Donut Chart of Risk Score Categories",
        annotations=[dict(
            text=f'{total_count}\n Barangays',
            x=0.5,
            y=0.5,
            font_size=20,
            showarrow=False,
            xanchor='center',
            yanchor='middle',
            # Adjust the position if needed
        )],
        showlegend=False,
        width=200,  # Set the width of the chart
        height=200,
        margin=dict(t=0, b=0, l=0, r=0)  # Adjust margins if necessary
    )

    return fig



# Create a function to render the legend
def render_legend(colors):
    legend = ""
    for category, color in colors.items():
        legend += f'<div style="display: flex; align-items: center; margin-right: 15px;">' \
                  f'<div style="width: 20px; height: 20px; background-color: {color}; margin-right: 5px;"></div>' \
                  f'<div>{category}</div>' \
                  '</div>'
    legend = f'<div style="display: flex; flex-wrap: wrap; align-items: center;">{legend}</div>'
    
    return legend




def create_map(gdf):
    # Create a base map
    m = folium.Map(location=[7.25, 125.6], scrollWheelZoom=True, tiles='CartoDB positron', zoom_start=10.49)

    # Add GeoJSON to the map with colors based on category
    geojson_data = gdf.to_json()
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': category_colors.get(feature['properties']['risk_category'], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity':0.7
            
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['barangay', 'risk_score_category'],
            aliases=['Barangay:', 'Risk Level:'],
            localize=True
        )
    ).add_to(m)

    return m

# Streamlit application
def main():
    st.title('Davao City Flood Risk')
    df = st.session_state.data    
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    
    col1, col2 = st.columns([3, 6])

    with col1:

        st.markdown("Risk is the potential loss of life, injury, or destroyed or damaged assets which could occur to a system, society or a community in a specific period of time, determined probabilistically as a function of hazard, exposure, vulnerability and capacity.")
        
        
        
        fig = create_donut_chart(df, 'risk_category')

        # Display the chart in Streamlit
        st.plotly_chart(fig)

        # Streamlit app
        st.caption('Risk Level:')
        st.markdown(render_legend(category_colors), unsafe_allow_html=True)

    with col2:
        # Create and display the map
        map_ = create_map(gdf)
        st_folium(map_, width=800, height=500)

if __name__ == "__main__":
    main()
