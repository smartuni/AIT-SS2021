print("Hier gehts noch")
import random
from paho.mqtt import client as mqtt_client
import json
import base64
from MongoServer import MongoServer

# Simple approach
# 1. Connect to MQTT API from TTN
# 2. Register for updates
# 3. Print/Save received information

# More sophisticated approach (NO MQTT)
# 1. Periodically connect to TTN
# 2. Check for new data
# 3. Download + Save

topics = [
    'v3/ait-app@ttn/devices/test-dev/join',
    'v3/ait-app@ttn/devices/test-dev/up',
    'v3/ait-app@ttn/devices/test-dev/down/queued',
    'v3/ait-app@ttn/devices/test-dev/down/sent',
    'v3/ait-app@ttn/devices/test-dev/down/ack',
    'v3/ait-app@ttn/devices/test-dev/down/nack',
    'v3/ait-app@ttn/devices/test-dev/down/failed',
    'v3/ait-app@ttn/devices/test-dev/service/data',
    'v3/ait-app@ttn/devices/test-dev/location/solved'
]


username = 'ait-app@ttn'
key = 'NNSXS.ARGCTO55QWQAQNJ2ISZ5MQW7GAZKH3UCW6YEUVY.CYA6RIX7EEX2KT3B3QHG4BK3AVICSJRZ2KDUQFRW42XMWY56FFBQ'
address = 'eu1.cloud.thethings.network'
port = 1883
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt():
  def on_connect(client, userdata, flags, rc):
    if rc == 0:
      print("Connected to MQTT Broker!")
    else:
      print("Failed to connect, return code %d\n", rc)
  # Set Connecting Client ID
  client = mqtt_client.Client(client_id)
  client.username_pw_set(username, key)
  client.on_connect = on_connect
  client.connect(address, port)
  return client


def subscribe(client: mqtt_client, mongoDB: MongoServer):
  def on_message(client, userdata, msg):
    # Message from LowRaWAn Network Recieved
    try:
      print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
      # Convert Json Strong to dict
      inMessage = json.loads(msg.payload.decode())

      dbInputDict = {"device_id": str(inMessage['end_device_ids']['device_id']), "received_at": str(inMessage['received_at']), "data": str(base64.b64decode(inMessage['uplink_message']['frm_payload']))}
      mongoDB.insert(dbInputDict)
    except Exception as e:
      print("Error after recieving message: " + str(e))
    


  client.subscribe(topics[1])
  client.on_message = on_message

print("Main Started")
client = connect_mqtt()
mongoDB = MongoServer("mongo")
subscribe(client, mongoDB)
client.loop_forever()