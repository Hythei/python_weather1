import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi


load_dotenv()

# MONGODB URL/API
MONGODB_URL = os.getenv("MONGODB_URL")
client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))

# Weather API Key
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.weatherapi.com/v1"

# This thing checks that we have a successful MongoDB connection
def check_mongodb_connection():
    try:
        client.admin.command('ping')
        print("Connection to MongoDB successful")
    except Exception as e:
        print(f"Connection to MongoDB failed: {e}")

def get_mongo_db():
    return client["weather_test1"]

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

# Dictionary that will be sent to MongoDB
# match_prediction will be used to showcase CRUD-functions
weather_data_model = {
    "location": weather_location['name'],
    "temperature": weather_current['temp_c'],
    "date": datetime.now(),
    "match_prediction": 'True'
}



print(f"Location: {weather_location['name']}, current temperature is {weather_current['temp_c']} degrees Celsius")
print(f"Date: {datetime.now()}")

check_mongodb_connection()

db = get_mongo_db()
collection = db["weather_information"]
collection.insert_one(weather_data_model)
item_details = collection.find({})
for item in item_details:
    print(item)