import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from prophet import Prophet
import geopandas as gpd
import folium
from streamlit_folium import folium_static
import json

st.set_page_config(layout="wide")

# Load datasets
calendar_data = pd.read_csv("data/raw/calendar.csv.gz", usecols=["listing_id", "date", "available"])
calendar_data["available"] = calendar_data["available"].map({"t": 1, "f": 0})
calendar_data["date"] = pd.to_datetime(calendar_data["date"])

listings = pd.read_csv("data/raw/listings.csv", usecols=["id", "neighbourhood"])

# Group data for analysis
availability_trend = calendar_data.groupby("date")["available"].sum().reset_index()
availability_trend.rename(columns={"date": "ds", "available": "y"}, inplace=True)

# Merge with neighborhood data
data_merged = calendar_data.merge(listings, left_on="listing_id", right_on="id")
data_merged["date"] = pd.to_datetime(data_merged["date"])
data_merged = data_merged.groupby(["date", "neighbourhood"])["available"].sum().reset_index()
data_merged["timestamp"] = data_merged["date"].astype(int) // 10**9
unique_dates = data_merged["date"].dt.strftime("%Y-%m-%d").unique()

# Load geographical data
neighbourhoods = gpd.read_file("data/raw/neighbourhoods.geojson")
neighbourhoods["id"] = neighbourhoods.index
neighbourhoods_json = json.loads(neighbourhoods.to_json()) if isinstance(neighbourhoods, gpd.GeoDataFrame) else {}

# Plot functions
def plot_availability_trend():
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.lineplot(x=availability_trend["ds"], y=availability_trend["y"], ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Available Listings")
    st.pyplot(fig)

def plot_availability_by_neighborhood():
    availability_by_neighborhood = data_merged.groupby("neighbourhood")["available"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(y=availability_by_neighborhood.index, x=availability_by_neighborhood.values, palette="coolwarm", ax=ax)
    ax.set_ylabel("")
    ax.set_xlabel("Number of Available Listings")
    st.pyplot(fig)

def plot_forecast():
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=False, changepoint_prior_scale=0.1)
    model.add_seasonality(name="monthly", period=30.5, fourier_order=5)
    model.fit(availability_trend)
    future = model.make_future_dataframe(periods=180, freq="D")
    forecast = model.predict(future)
    fig, ax = plt.subplots(figsize=(12, 6))
    model.plot(forecast, ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Available Listings")
    st.pyplot(fig)

def update_map(selected_date):
    max_available = data_merged["available"].max()
    selected_data = data_merged[data_merged["date"].dt.strftime("%Y-%m-%d") == selected_date]
    availability_dict = selected_data.set_index("neighbourhood")["available"].to_dict()

    def get_color(value, max_value):
        ratio = value / max_value
        return f"rgb({int(255 * (1 - ratio))}, 0, {int(255 * ratio)})"

    def style_function(feature):
        neighbourhood = feature["properties"].get("neighbourhood", "")
        available = availability_dict.get(neighbourhood, 0)
        return {"fillColor": get_color(available, max_available), "color": "black", "weight": 1, "fillOpacity": 0.6}

    for feature in neighbourhoods_json.get("features", []):
        feature["properties"]["available"] = availability_dict.get(feature["properties"].get("neighbourhood", ""), "No data")

    munich_map = folium.Map(location=[48.1351, 11.5820], zoom_start=11)
    folium.GeoJson(neighbourhoods_json, style_function=style_function,
                   tooltip=folium.GeoJsonTooltip(fields=["neighbourhood", "available"], aliases=["Neighbourhood", "Available Apartments"], localize=True)).add_to(munich_map)
    return munich_map



# Streamlit Interface
st.markdown("""
    <h1 style="text-align: center; font-size: 45px">Airbnb Data Insights</h1>
    """, unsafe_allow_html=True)

option = st.sidebar.radio("Select an insight:", ["Availability Trend", "Availability by Neighborhood", "Time Series Forecasting", "Map of Munich Neighborhood Availability"])

if option == "Availability Trend":
    st.markdown("<h1 style='text-align: center; font-size: 25px;'>Availability Trend Over Time</h1>", unsafe_allow_html=True)
    plot_availability_trend()
elif option == "Availability by Neighborhood":
    st.markdown("<h1 style='text-align: center; font-size: 25px;'>Airbnb Availability by Neighborhood</h1>", unsafe_allow_html=True)
    plot_availability_by_neighborhood()
elif option == "Time Series Forecasting":
    st.markdown("<h1 style='text-align: center; font-size: 25px;'>Predicting Future Availability (Prophet)</h1>", unsafe_allow_html=True)
    plot_forecast()
elif option == "Map of Munich Neighborhood Availability":
    st.markdown("<h1 style='text-align: center; font-size: 25px;'>Map of Munich Neighborhood Availability</h1>", unsafe_allow_html=True)
    selected_date = st.selectbox("Select a date:", unique_dates)
    map_object = update_map(selected_date)
    col1, col2, col3 = st.columns([1, 2.5, 1])  # Center column is wider
    with col2:
        folium_static(map_object)
