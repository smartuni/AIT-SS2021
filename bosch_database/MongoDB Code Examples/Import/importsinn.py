import regex
import json
import pymongo
from pymongo import MongoClient

def importData(collection):
    with open('sinndeslebens.txt', 'r') as sinnfile:
        sinn_file = sinnfile.readlines()
    
    print("Import started...")
    for line in sinn_file:
        modified = regex.sub(r'db\.fussball\.insert\(','',line)
        modified = regex.sub(r'\);','',modified)
        modified = regex.sub(r',\sgruendung.+\)','',modified)
        modified = regex.sub(r'','',modified)
        keys = regex.findall(r'\w+:',modified)
        for key in keys:
            modified = regex.sub(key,'"'+key[0:-1]+'":' ,modified)
        modified = modified.replace(" ","")
        modified = modified.replace("'",'"')
        modified = regex.sub(r',\]',']',modified)
        modified = regex.sub(r',}','}',modified)
        modified = regex.sub(r',}','}',modified)
        keys = regex.findall(r',\w+"',modified)
        for key in keys:
            modified = regex.sub(key,',"'+key[1:] ,modified)
        sinn_data = json.loads(modified)
        collection.insert(sinn_data)
    print("Import complete...")

client = MongoClient()
client = MongoClient('localhost', 27017)
database = client.admin
collist = database.list_collection_names()
collection = None
if not "nosql" in collist:
    collection = database["nosql"]
    importData(collection)
else:
    print("Already exist")
#collection = database["nosql"]
#importData(collection)

