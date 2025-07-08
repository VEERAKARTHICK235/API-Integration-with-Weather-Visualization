import requests
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from sklearn.linear_model import LinearRegression
import numpy as np
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

if not API_KEY:
    raise ValueError("API key not found! Please add OPENWEATHER_API_KEY in .env file.")


def fetch_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

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

def plot_dashboard(times, temps, humidities, wind_speeds, conditions, city):
    plt.style.use('default')  
    plt.figure(figsize=(14, 12))

    # Temperature
    plt.subplot(3, 1, 1)
    plt.plot(times, temps, marker='o', color='orange', label='Actual Temp')
    x = np.arange(len(temps)).reshape(-1, 1)
    y = np.array(temps).reshape(-1, 1)
    model = LinearRegression()
    model.fit(x, y)
    predicted = model.predict(x)
    plt.plot(times, predicted, linestyle='--', color='red', label='Predicted Trend')
    plt.title(f"🌡️ Temperature Forecast for {city}", fontsize=14)
    plt.ylabel("Temp (°C)")
    plt.legend()
    plt.xticks(rotation=45)

    # Humidity
    plt.subplot(3, 1, 2)
    plt.bar(times, humidities, color='deepskyblue')
    plt.title("💧 Humidity Forecast", fontsize=14)
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)

    # Wind Speed
    plt.subplot(3, 1, 3)
    plt.plot(times, wind_speeds, marker='x', color='green')
    plt.title("🌬️ Wind Speed Forecast", fontsize=14)
    plt.ylabel("Wind Speed (m/s)")
    plt.xlabel("Date/Time")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

def on_show_weather():
    city = city_var.get()
    try:
        result_label.config(text=f"Fetching weather for {city}...")
        data = fetch_weather_data(city)
        parsed = parse_data(data)
        plot_dashboard(*parsed, city)
        result_label.config(text=f"Forecast shown for {city}.")
    except Exception as e:
        result_label.config(text=f"Failed: {e}")

# GUI
root = tk.Tk()
root.title("🌍 Weather Dashboard with AI Forecast")
root.configure(bg="white")

tk.Label(root, text="Select City:", font=("Arial", 12), bg="white", fg="black").pack(pady=5)

city_var = tk.StringVar(value='Chennai')
city_dropdown = ttk.Combobox(root, textvariable=city_var, font=("Arial", 12), width=30)

city_dropdown['values'] = sorted([
    'Chennai', 'London', 'New York', 'Tokyo', 'Mumbai', 'Delhi', 'Paris', 'Sydney', 'Berlin', 'Dubai', 'Beijing',
    'Los Angeles', 'San Francisco', 'Chicago', 'Seoul', 'Singapore', 'Rome', 'Moscow', 'Istanbul', 'Bangkok',
    'Toronto', 'Mexico City', 'Barcelona', 'Kuala Lumpur', 'Jakarta', 'Cape Town', 'Lagos', 'Buenos Aires',
    'Cairo', 'Tehran', 'Baghdad', 'Doha', 'Riyadh', 'Nairobi', 'Hanoi', 'Warsaw', 'Zurich', 'Amsterdam'
])
city_dropdown.pack(pady=5)

show_button = tk.Button(root, text="Show Weather", command=on_show_weather, font=("Arial", 12),
                        bg="#007acc", fg="white", relief="raised", padx=10, pady=5)
show_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 10), bg="white", fg="black")
result_label.pack()

root.mainloop()
