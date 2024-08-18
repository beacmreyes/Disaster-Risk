import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely import wkt
import matplotlib.colors as mcolors

st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/Disaster_Risk_Cleaned_With_Scores_Map.csv')
    df['risk_category'] = df['risk_score_category'].str.rsplit(n=1).str[-1]
    # Convert DataFrame to GeoDataFrame
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")
    return gdf

@st.cache_data
def create_map_grey():
    m = folium.Map(location=[7.25, 125.6], scrollWheelZoom=True, tiles='CartoDB positron', zoom_start=10.49)    
    return m
    
# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'map' not in st.session_state:
    st.session_state.map = create_map_grey()


# Define a dictionary to manage the pages and their corresponding titles
PAGES = {
    "Davao City": "pages_/davao_city.py",
    "Risk": "pages_/risk.py",
    "Flood Hazard Exposure": "pages_/hazard_exposure.py",
    "Vulnerabilities": "pages_/vulnerability.py",
    "Machine Learning Insights": "pages_/ml_analysis.py"
}

# Sidebar for navigation
st.sidebar.title("Davao City Flood Risk Assessment")
selection = st.sidebar.radio("", list(PAGES.keys()))

# Load the selected page
page = PAGES[selection]
with open(page) as f:
    exec(f.read())