# API-Integration-with-Weather-Visualization

This Python project fetches real-time weather data from the OpenWeatherMap API and visualizes it using Matplotlib in an interactive GUI built with Tkinter. It includes AI-based prediction using linear regression to forecast temperature trends.


## Setup

1. Get an API key from [OpenWeatherMap](https://openweathermap.org/api).
2. Clone this repo.
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Replace the API key in `scripts/weather_plot.py` with your own.
5. Run the script:
    ```
    python scripts/weather_plot.py
    ```

## Output

- A line plot showing temperature changes over 5 days.
- A bar plot showing humidity percentage over 5 days.
