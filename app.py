# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from sklearn.datasets import fetch_california_housing

# ---------------------------
# Load dataset directly from sklearn
# ---------------------------
data = fetch_california_housing(as_frame=True)
df = data.frame

# Rename columns for consistency
df.rename(columns={
    'MedInc': 'MedianIncome',
    'HouseAge': 'HouseAge',
    'AveRooms': 'AveRooms',
    'AveBedrms': 'AveBedrms',
    'Population': 'Population',
    'AveOccup': 'AveOccup',
    'Latitude': 'Latitude',
    'Longitude': 'Longitude',
    'MedHouseVal': 'MedianHouseValue'
}, inplace=True)

# Create new features
df['RoomsPerHousehold'] = df['AveRooms'] / df['AveOccup']
df['BedroomsPerRoom'] = df['AveBedrms'] / df['AveRooms']
df['PopulationDensity'] = df['Population'] / df['AveOccup']

# ---------------------------
# Streamlit App Layout
# ---------------------------
st.title("California Housing Dashboard")

# Sidebar filter: Median Income
min_income = float(df['MedianIncome'].min())
max_income = float(df['MedianIncome'].max())
income_range = st.sidebar.slider(
    "Median Income (10k USD)",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income)
)

# Filter data
filtered_df = df[(df['MedianIncome'] >= income_range[0]) & (df['MedianIncome'] <= income_range[1])]
st.subheader(f"Filtered Data: {len(filtered_df)} records")

# ---------------------------
# Map of House Values
# ---------------------------
st.subheader("House Values Map")
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=filtered_df['Latitude'].mean(),
        longitude=filtered_df['Longitude'].mean(),
        zoom=7,
        pitch=0
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position='[Longitude, Latitude]',
            get_color='[255, 0, 0, 160]',
            get_radius='MedianHouseValue*10',
            pickable=True
        )
    ]
))

# ---------------------------
# Scatter Plot: Median Income vs Median House Value
# ---------------------------
st.subheader("Median Income vs Median House Value")
st.vega_lite_chart(filtered_df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'MedianIncome', 'type': 'quantitative', 'title': 'Median Income (10k USD)'},
        'y': {'field': 'MedianHouseValue', 'type': 'quantitative', 'title': 'Median House Value'},
        'color': {'field': 'MedianHouseValue', 'type': 'quantitative', 'scale': {'scheme': 'reds'}},
        'size': {'field': 'MedianHouseValue', 'type': 'quantitative'}
    }
}, use_container_width=True)

# ---------------------------
# Summary Statistics
# ---------------------------
st.subheader("Summary Statistics")
st.write(filtered_df.describe().round(2))

# ---------------------------
# Optional: show first 5 rows
# ---------------------------
st.subheader("Sample Data")
st.dataframe(filtered_df.head())
