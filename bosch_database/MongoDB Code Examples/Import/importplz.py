import json
import pymongo
from pymongo import MongoClient

def importData(collection):
    with open('plz.data', 'r') as plzfile:
        plz_file = plzfile.readlines()
    
    print("Import started...")
    for line in plz_file:
        plz_data = json.loads(line)
        collection.insert(plz_data)
    print("Import complete...")

client = MongoClient()
client = MongoClient('localhost', 27017)
database = client.admin
collist = database.list_collection_names()
collection = None
if not "nosql" in collist:
    collection = database["nosql"]
else:
    print("Already exist")
importData(collection)