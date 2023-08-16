import paho.mqtt.client as mqtt
import json
import numpy as np
from sklearn.linear_model import LinearRegression
import time
import matplotlib.pyplot as plt
import threading
import probat

class MqttProcessing:
    def __init__(self):
        self.stevilo_meritev = 10
        self.prve_upornosti = []
        self.druge_upornosti = []
        self.tretje_upornosti = []
        self.temperature = []
        self.mqtt_processing_over = False
        
    def on_message(self, client, userdata, message):
        topic = message.topic
        payload = json.loads(message.payload.decode('utf-8'))
        if topic.startswith("upornosti/"):
            upornost = payload["R"]
            temp = payload["T"]
            self.temperature.append(temp)
            print("Dobljena temperatura:", temp)
            print("temperature:", self.temperature)

            if topic == "upornosti/one":
                self.prve_upornosti.append(upornost)
            elif topic == "upornosti/two":
                self.druge_upornosti.append(upornost)
            elif topic == "upornosti/three":
                self.tretje_upornosti.append(upornost)
            print("Dobljena upornost:", upornost)
            print("prve_upornosti:", self.prve_upornosti)
            print("druge_upornosti:", self.druge_upornosti)
            print("tretje_upornosti:", self.tretje_upornosti)

            if topic == "upornosti/three" and len(self.tretje_upornosti) == self.stevilo_meritev:
                self.mqtt_processing_over = True
                
    def mqtt_thread_function(self):
        # Povezava z MQTT brokerjem
        client = mqtt.Client()
        client.on_message = self.on_message

        # Parametri3
        broker_address = "broker.hivemq.com"
        broker_port = 1883

        mqtt_user = "DinoSelim"
        mqtt_password = "IdeaPad+-.2604"
   #    client.loop_start()
        client.connect(broker_address, broker_port)
        client.username_pw_set(mqtt_user, mqtt_password)

        # Teme
        client.subscribe("upornosti/one")
        client.subscribe("upornosti/two")
        client.subscribe("upornosti/three")

        client.subscribe("temperature/one")
        client.subscribe("temperature/two")
        client.subscribe("temperature/three")
    #   client.subscribe("temperature")

        client.loop_forever()

    # Define the function to be executed after client.loop_forever()
    def additional_code(self, prve_upornosti, druge_upornosti, tretje_upornosti, temperature):   
        while not self.mqtt_processing_over:
            time.sleep(0.1)
        average_first = sum(self.prve_upornosti)/len(self.prve_upornosti)
        average_second = sum(self.druge_upornosti)/len(self.druge_upornosti)
        average_third = sum(self.tretje_upornosti)/len(self.tretje_upornosti)
     
        print(average_first)
        print(average_second)
        print(average_third)
        
        average = [average_first, average_second, average_third]

        temperature_new = [temperature[0], temperature[11], temperature[22]]
        probat.recognizeInstrument(average, temperature_new)
        # Define the known temperature-resistance values for each sensor type

        resistances = np.array([average_first, average_second, average_third])
        
        time.sleep(5)
        print("Additional code execution completed.")

    def process_mqtt_data(self):	
        # Start the MQTT thread
        mqtt_thread = threading.Thread(target=self.mqtt_thread_function)
        mqtt_thread.start()

        # Wait for MQTT messages to be processed
        while not self.mqtt_processing_over:   # Ključ kode, ko to postane True, nadaljuje se spodnji del
            time.sleep(0.1)

        # Delay to allow messages to be received and processed
        time.sleep(1) #Važen delay, počaka eno sekundo da bi lahko zadnji podatek poslali

        # Execute additional code here
        self.additional_code(self.prve_upornosti, self.druge_upornosti, self.tretje_upornosti, self.temperature)

        # Wait for the MQTT thread to complete
        mqtt_thread.join()

        # Code execution continues here after the MQTT client loop is finished
        print("All code execution completed.")

my_object = MqttProcessing()
my_object.process_mqtt_data()