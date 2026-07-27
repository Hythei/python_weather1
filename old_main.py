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

def main():
    mongo.check_mongodb_connection()
    print("Program started")
    while True:
        print("Choose an action:")
        print("1. Query for weather data via Weather API")
        print("2. Search for past weather data on MongoDB")
        print("3. Update a document's match_prediction value on MongoDB")
        print("4. Delete a document from MongoDB")
        print("Type 'exit' to exit")
        choice = input("Choice: ").lower().strip()
        if choice == "exit":
            break
        elif choice == "1":
            data_model = weather_query()
            mongo.mongodb_send(data_model)
        elif choice == "2":
            mongo.mongodb_find()
        elif choice == "3":
            mongo.mongodb_update()
        elif choice == "4":
            mongo.mongodb_delete()
    print("Program ended")

if __name__ == "__main__":
    main()
