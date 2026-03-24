import os
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://root:password@localhost:27017/teenup?authSource=admin")

client = MongoClient(MONGO_URL)
db = client["teenup"]  

# Các collection
parents_collection = db["parents"]
students_collection = db["students"]
classes_collection = db["classes"]
registrations_collection = db["class_registrations"]
subscriptions_collection = db["subscriptions"]

def get_db():
    return db