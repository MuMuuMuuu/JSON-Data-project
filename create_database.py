"""
filename: create_database.py

description:
This module creates a new MongoDB database and collection, and inserts initial data from a JSON file into the collection.


Author: Yinzheng Xiong
Date: 10/28/2024
"""

from pymongo import MongoClient
import json

def create_database(uri="mongodb://localhost:27017/", db_name="hw3", json_file_path='restaurants.json'):
    '''
    Create a new MongoDB database and collection, and insert initial data from a JSON file.
    :param uri:  MongoDB URI
    :param db_name:  Name of the database
    :param json_file_path:  Path to the JSON file containing initial data
    :return:  None
    '''

    # Connect to the MongoDB client
    client = MongoClient(uri)
    db = client[db_name]

    # Check if the "restaurants" collection exists
    if "restaurants" in db.list_collection_names():
        # If it exists, drop the collection to start fresh
        db["restaurants"].drop()
        print("Existing 'restaurants' collection dropped.")

    # Create a new "restaurants" collection
    db.create_collection("restaurants")
    print("New 'restaurants' collection created.")

    # Insert initial data into the "restaurants" collection from the specified JSON file
    with open(json_file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                db.restaurants.insert_one(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

    print(f"Inserted initial data into 'restaurants' collection from {json_file_path}.")

    print("Database setup complete.")
    client.close()

if __name__ == "__main__":
    create_database(json_file_path='restaurants.json')
