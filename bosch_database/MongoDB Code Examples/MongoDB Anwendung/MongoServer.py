import pymongo
from pymongo import MongoClient

class MongoServer:
    def __init__(self, host):
        client = MongoClient()
        client = MongoClient(host, 27017)
        database = client.admin
        self.collection = database.nosql

    #def insert(self, key, value):
    def count(self):
        return self.collection.count()

    def remove(self):
        self.collection.remove()

    def find(self, attributes=None, projection=None):
        return self.collection.find(attributes, projection)

    def maxByKeyOne(self, key):
        return self.collection.find_one(sort=[(key, pymongo.DESCENDING)])

    def minByKeyOne(self, key):
        return self.collection.find_one(sort=[(key, pymongo.ASCENDING)])

    def maxByKey(self, key):
        return self.collection.find(sort=[(key, pymongo.DESCENDING)])

    def minByKey(self, key):
        return self.collection.find(sort=[(key, pymongo.ASCENDING)])

    def update(self, spec, document, upsert=False, manipulate=False, multi=False, check_keys=True, **kwargs):
        self.collection.update(spec, document, upsert=upsert, manipulate=manipulate, multi=multi, check_keys=check_keys, **kwargs)
