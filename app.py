# app.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# Load your cleaned dataset
df = pd.read_csv("california_housing_clean.csv")  # make sure CSV is in same folder

# Title
st.title("California Housing Dashboard")

# Sidebar slider for Median Income
min_income = float(df['median_income'].min())
max_income = float(df['median_income'].max())
income_range = st.sidebar.slider(
    "Median Income (10k USD)",
    min_value=min_income,
    max_value=max_income,
    value=(min_income, max_income)
)

# Filter dataset
filtered_df = df[(df['median_income'] >= income_range[0]) & (df['median_income'] <= income_range[1])]

# Map visualization
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=filtered_df['latitude'].mean(),
        longitude=filtered_df['longitude'].mean(),
        zoom=7,
        pitch=0
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[255, 0, 0, 160]',
            get_radius='median_house_value/1000',
            pickable=True
        )
    ]
))

# Scatter plot
st.subheader("Median Income vs Median House Value")
st.vega_lite_chart(filtered_df, {
    'mark': {'type': 'circle', 'tooltip': True},
    'encoding': {
        'x': {'field': 'median_income', 'type': 'quantitative'},
        'y': {'field': 'median_house_value', 'type': 'quantitative'},
        'color': {'field': 'median_house_value', 'type': 'quantitative'},
        'size': {'field': 'median_house_value', 'type': 'quantitative'}
    }
})

# Summary statistics
st.subheader("Summary Statistics for Filtered Data")
st.write(filtered_df.describe().round(2))
