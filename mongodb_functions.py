# This file will contain functions related to MongoDB when I get around to tidying up the main-file
import os

from bson.errors import InvalidId
from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from pymongo.server_api import ServerApi

load_dotenv()

# MONGODB URL/API
MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL, server_api=ServerApi('1'))
def get_mongo_db():
    return client["weather_test1"]

# This thing checks that we have a successful MongoDB connection
def check_mongodb_connection():
    try:
        client.admin.command('ping')
        print("Connection to MongoDB successful")
    except PyMongoError as error:
        print(f"Connection to MongoDB failed: {error}")
    except RuntimeError as error:
        print(f"MongoDB configuration error: {error}")

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