import os
from datetime import datetime

import requests

import mongodb_functions as mongo

# Weather API Key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

def weather_query():
    location = input("Enter a location: ")
    params = {
        "key": API_KEY,
        "q": location,
        "aqi": "no"
    }
    response = requests.get(f"{BASE_URL}/current.json", params=params)
    data = response.json()
    current = data["current"]
    location = data["location"]
    # Dictionary that will be sent to MongoDB
    # match_prediction will be used to showcase CRUD-functions
    data_model = {
        "location": location['name'],
        "temperature": current['temp_c'],
        "date": datetime.now(),
        "match_prediction": True
    }
    print (f"{location['name']} current temperature: {current['temp_c']}")
    return data_model

# def print_weather_data(weather_current, weather_location):
    print(f"Location: {weather_location['name']}, current temperature is {weather_current['temp_c']} degrees Celsius")
    print(f"Date: {datetime.now()}")

def main():
    mongo.check_mongodb_connection()
    # weather_current, weather_location, weather_data_model = weather_query()
    # print_weather_data(weather_current, weather_location)
    # mongodb_send(weather_data_model)
    # mongodb_find()
    # mongodb_update()
    # mongodb_delete()
    print("Program started")
    # Create a while-loop for the main() function
    while True:
        print("Choose an action:")
        print("1. Query for weather data via Weather API")
        print("2. Search for past weather data on MongoDB")
        print("Type 'exit' to exit")
        choice = input("Choice: ")
        if choice == "exit":
            break
        elif choice == "1":
            weather_query()
        elif choice == "2":
            mongo.mongodb_find()
    print("Program ended")

if __name__ == "__main__":
    main()
