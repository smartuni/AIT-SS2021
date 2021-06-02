import random
from paho.mqtt import client as mqtt_client

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
key = '<YOUR_KEY_HERE!>e'
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


def subscribe(client: mqtt_client):
  def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

  client.subscribe(topics[1])
  client.on_message = on_message


def main():
  client = connect_mqtt()
  subscribe(client)
  client.loop_forever()


if __name__ == '__main__':
  main()
