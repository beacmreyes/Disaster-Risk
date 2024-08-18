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



@st.cache_data
def create_donut_chart(_df, category_col):   
    # Define the desired order
    category_order = ['Low', 'Medium', 'High']

    # Compute counts for each category
    category_counts = _df[category_col].value_counts()

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
@st.cache_data
def render_legend(colors):
    legend = ""
    for category, color in colors.items():
        legend += f'<div style="display: flex; align-items: center; margin-right: 15px;">' \
                  f'<div style="width: 20px; height: 20px; background-color: {color}; margin-right: 5px;"></div>' \
                  f'<div>{category}</div>' \
                  '</div>'
    legend = f'<div style="display: flex; flex-wrap: wrap;">{legend}</div>'
    
    return legend



@st.fragment
def create_map(m,gdf,metric):

    # Add GeoJSON to the map with colors based on category
    geojson_data = gdf.to_json()
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': category_colors.get(feature['properties'][metric], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity':0.7
            
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['barangay', metric],
            aliases=['Barangay:', 'Risk Level:'],
            localize=True
        )
    ).add_to(m)

    return m

# Streamlit application
def main():
    st.title('Evaluating Flood Risk in Davao City Barangays with Machine Learning')

    st.write('We evaluated various machine learning models to classify flood risk in Davao City. Our approach involved preprocessing the data using the Yeoh-Johnson transformation and Standard Scaler, followed by testing multiple traditional classification algorithms to determine their effectiveness.')


    # Render the HTML in Streamlit
    # st.markdown(f"<div style='text-align: center;'><img src='images/ml_base_models.png' width='600'></div>", unsafe_allow_html=True)
    st.image('images/ml_base_models.png', use_column_width=False)
    
    st.markdown("""Initial performance metrics revealed that the LightGBM classification model achieved the highest performance. To further improve its accuracy, the model underwent hyperparameter tuning. The optimal parameters identified are:
- Learning rate: 0.05
- Minimum child samples: 50
- Number of estimators: 500

The performance scores with these parameters are detailed in the table below:"""
)
    col1, col2, col3 = st.columns([0.2, 5, 0.2])
    col2.image('images/hypertuned_scores.png', use_column_width=False)

    st.write("Additionally, we analyzed feature importance using SHAP (SHapley Additive exPlanations) to understand the contribution of each feature to the model's predictions.")

    col1, col2, col3 = st.columns([1,1,1])

    col1.image('images/feat_imp_lowrisk.png', caption='Low Risk', use_column_width=True)
    col2.image('images/feat_imp_medrisk.png', caption='Medium Risk', use_column_width=True)
    col3.image('images/feat_imp_highrisk.png', caption='High Risk', use_column_width=True)

    st.markdown("""
     - **Low Risk Score barangays** can be characterized by their low exposure to rare but severe flooding hazards, but are generally less vulnerable in terms of socioeconomic, physical and environmental factors
     - **Medium Risk Score barangays** can be characterized by their exposure to rare but severe flooding hazards, and are highly vulnerable in terms of socioeconomic, physical and geographical factors
     - **High Risk Score barangays** can be characterized by their high exposure to less severe but frequent flooding hazards, and are moderately vulnerable in terms of socioeconomic, physical and environmental factors
    """)

    # col1, col2 = st.columns([1,1])
 #    col1.markdown("""
 # **Low Risk Score barangays** can be characterized by their low exposure to rare but severe flooding hazards, but are generally less vulnerable in terms of socioeconomic, physical and environmental factors""")
 #    col2.image('images/feat_imp_lowrisk.png', caption='Low Risk', use_column_width=True)    

    col1, col2 = st.columns([1,1])
    df = st.session_state.data    
    ml_df = pd.read_csv('data/predicted_risk_score.csv')
    df = pd.merge(df, ml_df[['barangay', 'predicted_risk_category']], on = 'barangay')
    gdf = df
    # st.write(gdf)
    m_actual = folium.Map(location=[7.25, 125.45], scrollWheelZoom=True, tiles='CartoDB positron', zoom_start=9.5)
    m_ml = folium.Map(location=[7.25, 125.45], scrollWheelZoom=True, tiles='CartoDB positron', zoom_start=9.5)
    
    # map_actual = create_map(m_actual,gdf, 'risk_category')
    map_ml = create_map(m_ml,gdf, 'predicted_risk_category')
    with col1:        
    #     st_folium(map_actual, width=350, height=500,returned_objects=[], key='map_actual')
    #     st.markdown("""<div style="text-align: center;font-size: 12px;padding-right:50px">Computed Risk Level</div>""",unsafe_allow_html=True)
        st.markdown("""
    
        The model's predictions matched the computed risk levels for 177 instances. However, there are some discrepancies:
        
        **Barangays Classified as Medium Risk but Predicted as Low Risk:**
        - Mintal
        - Barangay 19-B (Pob.)
        - Catalunan Pequeno
        - Matina
        
        **Barangays Classified as High Risk but Predicted as Medium Risk:**
        - Pangi
        - Mabuhay
        - Lampianao
        """)
    with col2:
        st_folium(map_ml, width=350, height=500,returned_objects=[], key="map_ml")
        st.markdown("""<div style="text-align: center; font-size: 12px;padding-right:50px;"">ML Predicted Risk Level</div>""",unsafe_allow_html=True)
        

    # with col2:
    # # Create and display the map
    # map_ = create_map(m,gdf)
    # st_folium(map_, width=800, height=500,returned_objects=[])
if __name__ == "__main__":
    main()
