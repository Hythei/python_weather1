import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

location = input("Enter a location: ")

params = {
    "key": API_KEY,
    "q":location,
    "aqi":"no"
}

# Current.json refers to current weather
response = requests.get(f"{BASE_URL}/current.json", params=params)

data = response.json()
print(data)
weather_current = data["current"]
weather_location = data["location"]

print(f"Location: {weather_location['name']}, current temperature is {weather_current['temp_c']} degrees Celsius")