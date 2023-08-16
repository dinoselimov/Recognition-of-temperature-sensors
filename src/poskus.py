import paho.mqtt.client as mqtt
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import time
import matplotlib.pyplot as plt
import threading

stevilo_meritev = 10

prve_upornosti = []
druge_upornosti = []
tretje_upornosti = []
temperature = []

def on_message(client, userdata, message):
    topic = message.topic
    payload = json.loads(message.payload.decode('utf-8'))
    if topic.startswith("upornosti/"):
        upornost = payload["R"]
        if topic == "upornosti/one":
            prve_upornosti.append(upornost)
        elif topic == "upornosti/two":
            druge_upornosti.append(upornost)
        elif topic == "upornosti/three":
            tretje_upornosti.append(upornost)
        print("Dobljena upornost:", upornost)
        print("prve_upornosti:", prve_upornosti)
        print("druge_upornosti:", druge_upornosti)
        print("tretje_upornosti:", tretje_upornosti)
    elif topic.startswith("temperature/"):
        temperature.append(payload)
        print("Dobljena temperatura:", payload)
        print("temperature:", temperature)
        
print("------------------------------------------------------")

def average(lst):
    return sum(lst) / len(lst)

# Parametri
broker_address = "broker.hivemq.com"
broker_port = 1883
mqtt_user = "DinoSelim"
mqtt_password = "IdeaPad+-.2604"
#topic = "upornost"

# Povezava z MQTT brokerjem
client = mqtt.Client()
client.username_pw_set(mqtt_user, mqtt_password)
client.connect(broker_address, broker_port)

# Callback funckija
client.on_message = on_message

# Teme
client.subscribe("upornosti/one")
client.subscribe("upornosti/two")
client.subscribe("upornosti/three")

client.subscribe("temperature/one")
client.subscribe("temperature/two")
client.subscribe("temperature/three")
#client.subscribe("temperature")

client.loop_forever()

average_first = average(prve_upornosti)
average_second = average(druge_upornosti)
average_third = average(tretje_upornosti)

print(average_first)
print(average_second)
print(average_third)




