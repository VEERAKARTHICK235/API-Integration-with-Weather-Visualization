import streamlit as st
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

# --- Fetch weather data ---
def fetch_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# --- Parse data ---
def parse_data(data):
    times, temps, humidities, wind_speeds, conditions = [], [], [], [], []
    for item in data['list']:
        dt = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        times.append(dt)
        temps.append(item['main']['temp'])
        humidities.append(item['main']['humidity'])
        wind_speeds.append(item['wind']['speed'])
        conditions.append(item['weather'][0]['main'])
    return times, temps, humidities, wind_speeds, conditions

# --- Plotting ---
def plot_dashboard(times, temps, humidities, wind_speeds, conditions, city):
    fig, axs = plt.subplots(3, 1, figsize=(12, 10))

    # Temperature + AI Trend
    x = np.arange(len(temps)).reshape(-1, 1)
    y = np.array(temps).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    predicted = model.predict(x)

    axs[0].plot(times, temps, 'o-', color='orange', label='Actual Temp')
    axs[0].plot(times, predicted, '--', color='red', label='Predicted Trend')
    axs[0].set_title(f"🌡️ Temperature Forecast for {city}")
    axs[0].set_ylabel("Temp (°C)")
    axs[0].legend()
    axs[0].grid(True)
    axs[0].tick_params(axis='x', rotation=45)

    # Humidity
    axs[1].bar(times, humidities, color='skyblue')
    axs[1].set_title("💧 Humidity Forecast")
    axs[1].set_ylabel("Humidity (%)")
    axs[1].tick_params(axis='x', rotation=45)

    # Wind Speed
    axs[2].plot(times, wind_speeds, 'x-', color='green')
    axs[2].set_title("🌬️ Wind Speed Forecast")
    axs[2].set_ylabel("Wind Speed (m/s)")
    axs[2].set_xlabel("Date/Time")
    axs[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

# --- Streamlit UI ---
st.set_page_config(page_title="Weather Forecast Dashboard", layout="centered")
st.title("🌍 Weather Forecast Dashboard with AI")
st.write("Enter any city to get a 5-day forecast with AI-predicted temperature trend.")

city_input = st.text_input("🔎 Enter city name:")

if st.button("📊 Show Weather Forecast"):
    if city_input.strip() == "":
        st.warning("Please enter a valid city name")
    else:
        try:
            with st.spinner(f"Fetching weather for {city_input}..."):
                data = fetch_weather_data(city_input)
                parsed = parse_data(data)
                plot_dashboard(*parsed, city_input)
        except Exception as e:
            st.error(f"❌ Error: {e}")
