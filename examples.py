"""
WeatherAPI.com — Python Example (requests library)
Docs: https://www.weatherapi.com/docs/
Sign up free: https://www.weatherapi.com/signup.aspx

Install: pip install requests
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"


class WeatherAPIError(Exception):
    """Raised when WeatherAPI returns an error response."""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"WeatherAPI error {code}: {message}")


def get_current_weather(location: str, aqi: bool = True) -> dict:
    """
    Get current weather for a location.

    Args:
        location: City name, lat/lon (e.g. "51.5,-0.1"), zip code, or IP address
        aqi: Include air quality data

    Returns:
        Dictionary containing location and current weather data

    Raises:
        WeatherAPIError: If the API returns an error
    """
    params = {
        "key": API_KEY,
        "q": location,
        "aqi": "yes" if aqi else "no",
    }

    response = requests.get(f"{BASE_URL}/current.json", params=params)

    if not response.ok:
        error = response.json()["error"]
        raise WeatherAPIError(error["code"], error["message"])

    return response.json()


def get_forecast(location: str, days: int = 3, alerts: bool = True) -> dict:
    """
    Get weather forecast for a location.

    Args:
        location: City name, lat/lon, zip code, or IP address
        days: Number of forecast days (1-14; plan limits may apply)
        alerts: Include weather alerts

    Returns:
        Dictionary containing location, current, and forecast data
    """
    params = {
        "key": API_KEY,
        "q": location,
        "days": days,
        "aqi": "yes",
        "alerts": "yes" if alerts else "no",
    }

    response = requests.get(f"{BASE_URL}/forecast.json", params=params)

    if not response.ok:
        error = response.json()["error"]
        raise WeatherAPIError(error["code"], error["message"])

    return response.json()


def get_history(location: str, date: str) -> dict:
    """
    Get historical weather data.

    Args:
        location: City name, lat/lon, zip code, or IP address
        date: Date in yyyy-MM-dd format (from 2010-01-01)

    Returns:
        Dictionary containing historical weather data
    """
    params = {
        "key": API_KEY,
        "q": location,
        "dt": date,
    }

    response = requests.get(f"{BASE_URL}/history.json", params=params)

    if not response.ok:
        error = response.json()["error"]
        raise WeatherAPIError(error["code"], error["message"])

    return response.json()


def get_astronomy(location: str, date: str) -> dict:
    """
    Get astronomy data (sunrise, sunset, moon phase).

    Args:
        location: City name, lat/lon, zip code, or IP address
        date: Date in yyyy-MM-dd format

    Returns:
        Dictionary containing astronomy data
    """
    params = {
        "key": API_KEY,
        "q": location,
        "dt": date,
    }

    response = requests.get(f"{BASE_URL}/astronomy.json", params=params)

    if not response.ok:
        error = response.json()["error"]
        raise WeatherAPIError(error["code"], error["message"])

    return response.json()


def search_locations(query: str) -> list:
    """
    Search/autocomplete locations.

    Args:
        query: Partial city name (min 3 characters)

    Returns:
        List of matching location dictionaries
    """
    params = {
        "key": API_KEY,
        "q": query,
    }

    response = requests.get(f"{BASE_URL}/search.json", params=params)

    if not response.ok:
        error = response.json()["error"]
        raise WeatherAPIError(error["code"], error["message"])

    return response.json()


def main():
    # --- Current Weather ---
    query_location = input("Enter a location: ")
    print(f"=== Current Weather: {query_location} ===")
    data = get_current_weather(query_location)
    loc = data["location"]
    cur = data["current"]

    print(f"📍 {loc['name']}, {loc['country']}")
    print(f"🕐 Local time: {loc['localtime']}")
    print(f"🌡️  Temperature: {cur['temp_c']}°C / {cur['temp_f']}°F")
    print(f"🌤️  Condition: {cur['condition']['text']}")
    print(f"💧 Humidity: {cur['humidity']}%")
    print(f"💨 Wind: {cur['wind_kph']} km/h from {cur['wind_dir']}")
    print(f"👁️  Visibility: {cur['vis_km']} km")
    print(f"☀️  UV Index: {cur['uv']}")
    print(f"🌡️  Feels like: {cur['feelslike_c']}°C")

    if "air_quality" in cur:
        aqi = cur["air_quality"]
        print(f"🌬️  PM2.5: {aqi['pm2_5']:.1f} µg/m³")
        print(f"🌬️  US EPA Index: {aqi['us-epa-index']} / 6")

    # --- Forecast ---
    print("\n=== 3-Day Forecast: Tokyo ===")
    forecast_data = get_forecast("Tokyo", days=3)

    for day in forecast_data["forecast"]["forecastday"]:
        d = day["day"]
        print(
            f"  {day['date']}: {d['condition']['text']} | "
            f"Max {d['maxtemp_c']}°C | Min {d['mintemp_c']}°C | "
            f"Rain {d['daily_chance_of_rain']}% | "
            f"Sunrise {day['astro']['sunrise']}"
        )

    # --- Today's hourly breakdown ---
    print("\n=== Hourly Forecast: Tokyo (today) ===")
    today = forecast_data["forecast"]["forecastday"][0]
    for hour in today["hour"][::3]:  # every 3 hours
        print(
            f"  {hour['time'][-5:]}: {hour['temp_c']}°C  "
            f"{hour['condition']['text']}  "
            f"Rain: {hour['chance_of_rain']}%"
        )

    # --- Astronomy ---
    print("\n=== Astronomy: Paris today ===")
    today_str = datetime.today().strftime("%Y-%m-%d")
    astro_data = get_astronomy("Paris", today_str)
    astro = astro_data["astronomy"]["astro"]
    print(f"  🌅 Sunrise: {astro['sunrise']}")
    print(f"  🌇 Sunset: {astro['sunset']}")
    print(f"  🌙 Moon phase: {astro['moon_phase']}")
    print(f"  🌕 Moon illumination: {astro['moon_illumination']}%")

    # --- Search ---
    print("\n=== Location Search: 'ber' ===")
    results = search_locations("ber")
    for loc in results[:3]:
        print(f"  {loc['name']}, {loc['region']}, {loc['country']}")


if __name__ == "__main__":
    main()
