print("Hier gehts noch")
import random
from paho.mqtt import client as mqtt_client
import json
import base64
from MongoServer import MongoServer

print("Main Started")
#client = connect_mqtt()
mongoDB = MongoServer("mongo")
dbInputDict = {"test": "bestanden"}
mongoDB.insert(dbInputDict)
#subscribe(client, mongoDB)
#client.loop_forever()