import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId


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
    return current, location, data_model



def print_weather_data(weather_current, weather_location):
    print(f"Location: {weather_location['name']}, current temperature is {weather_current['temp_c']} degrees Celsius")
    print(f"Date: {datetime.now()}")




def mongodb_find():
    db = get_mongo_db()
    collection = db["weather_information"]
    # Suppose we can leave the find() empty and it will return all the data
    enquiry = input("Find data in MongoDB? (y/n): ")
    if enquiry == 'n':
        return
    else:
        print("Type 1 to search for all documents within the collection.")
        print("Type 2 to search for a specific document according the location.")
        choice = input("Specify: ")
        if choice == '1':
            item_details = collection.find({})
        elif choice == '2':
            location = input("Enter a location: ")
            item_details = collection.find({"location" : location})
        else:
            print("Invalid choice. Please try again.")
            return
        for item in item_details:
            print(item)

def mongodb_send(data_model):
    db = get_mongo_db()
    collection = db["weather_information"]
    enquiry = input("Send data to MongoDB? (y/n): ")
    if enquiry == 'n':
        return
    else:
        collection.insert_one(data_model)
        print("Data sent to MongoDB")

def mongodb_update():
    db = get_mongo_db()
    collection = db["weather_information"]
    print("Use the ObjectId to update the document. This just changes the match_prediction to False.")
    target_id = input("Enter the ObjectId: ")

    try:
        object_id = ObjectId(target_id)
    except:
        print("Invalid ObjectId. Please try again.")
        return

    collection.update_one({"_id" : object_id}, {"$set" : {"match_prediction" : False}})
    print("Document updated:")
    updated_document = collection.find_one({"_id" : object_id})
    print(updated_document)

def mongodb_delete():
    db = get_mongo_db()
    collection = db["weather_information"]
    print("Use the ObjectId to delete the document.")
    # Initially we'll just use the object_id to delete the document
    # Once delete_one has been proven to work, we'll see if delete_many works with location
    target_id = input("Enter the ObjectId: ")
    try:
        object_id = ObjectId(target_id)
    except:
        print("Invalid ObjectId. Please try again.")
        return
    doc_to_be_removed = collection.find_one({"_id": object_id})
    print("Following document will be deleted from the collection")
    print(doc_to_be_removed)
    collection.delete_one({"_id": object_id})

def main():
    check_mongodb_connection()
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
            weather_current, weather_location, weather_data_model = weather_query()
            print_weather_data(weather_current, weather_location)
        elif choice == "2":
            mongodb_find()
    print("Program ended")

if __name__ == "__main__":
    main()
