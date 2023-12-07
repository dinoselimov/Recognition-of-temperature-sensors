from threading import Thread
import paho.mqtt.client as mqtt
import json
import time
import tkinter as tk
import numpy as np
import math

import training_data
import temperature_reading

class App:
    """
    The `App` class encapsulates the entire functionality of the application, providing a modular and organized
    structure. It contains the following functions:
    
    - `connect_to_broker`: Manages the connection to the MQTT broker with username and password.
    - `send_command`: Sends commands to start measurements to the ESP32 device.
    - `receive_measurements`: Handles the reception and processing of resistance measurements from the ESP32.
    - `on_connect`: Callback function for handling MQTT connection events.
    - `on_message`: Callback function for processing MQTT messages, specifically resistance measurements.
    - `on_publish`: Callback function to check the publish status of MQTT commands.
    - `start_temperature_measurements`: Initiates the process to start temperature measurements.
    - `additional_code`: Executes additional code after receiving and processing resistance measurements.
    - `store_temperature`: Stores temperature values provided by the user.
    - `start_measurements_process`: Orchestrates the process of starting and receiving measurements.
    - `start_measurements_button`: Initializes the GUI for the application, including buttons and labels.

    GUI Components:
    - Buttons for starting temperature measurements for three sensors individually.
    - Entry fields for entering actual temperatures corresponding to each sensor.
    - Buttons for confirming entered temperatures.
    - A label displaying the recognized sensor type.
    - A button to start calculated temperatures (disabled until a sensor type is recognized).

    """
    def __init__(self):
        self.temperature = None
        self.stop_mqtt_thread = False
        self.mqtt_processing_over = False
        self.measurements_received = 0
        self.measurements = []
        self.measurement_pack_first = []
        self.measurement_pack_second = []
        self.measurement_pack_third = []
        self.temperatures = []
        self.sensor_type = None
        self.flag = False

        self.received_packs = 0

    # Function which stores temperature
    def store_temperature(self, temperature, index):
        print(f"Temperature {index}: {temperature}")
        self.temperatures.append(temperature)

    # Callback function which is used, when the MQTT is connected to a broker
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print("Failed to connect to MQTT broker")
    
    # Callback function when we receive measurements
    def on_message(self, client, userdata, message):
        self.topic = message.topic
        print("message:", message.payload)
        self.payload = json.loads(message.payload.decode('utf-8'))
        print("on_message called")
   
        if self.topic == "resistances":
            resistance = self.payload["R"]                       
            self.measurements.append(resistance) # to je lista iz katere shranjujemo
            self.measurements_received += 1
            print("Received resistance measurement:", resistance)

            if len(self.measurements) > 90:
                if not self.measurement_pack_first:
                    self.measurement_pack_first = self.measurements[:]
                elif not self.measurement_pack_second:
                    self.measurement_pack_second = self.measurements[:]
                elif not self.measurement_pack_third:
                    self.measurement_pack_third = self.measurements[:] 
                    self.flag = True

                self.measurements_received = 0
                self.measurements.clear()
                client.disconnect()     
                
                if (
                    len(self.measurement_pack_first) > 90
                    and len(self.measurement_pack_second) > 90
                    and len(self.measurement_pack_third) > 90
                    
                ):
                    self.additional_code() 

        print(self.measurement_pack_first) 
        print(self.measurement_pack_second)
        print(self.measurement_pack_third)

        if self.topic == "temperature":
            print("Debugging payload", self.payload)
            resistance = self.payload["R"]                       
            self.measurements.append(resistance) # to je lista iz katere shranjujemo
            print("Appending one resistance")
            self.measurements_received += 1
            print("Received resistance measurement:", resistance)

    # Function which connects to broker with our username and password             
    def connect_to_broker(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        broker_address = "broker.hivemq.com"
        broker_port = 1883
        mqtt_user = "DinoSelim"
        mqtt_password = "IdeaPad+-.2604"
        
        client.connect(broker_address, broker_port)
        client.username_pw_set(mqtt_user, mqtt_password)
    
        print("Python MQTT established")

        return client # We return client to use as a object
    
    def send_command(self):
        client = self.connect_to_broker()

        measurements_count = 100
        command = {
            "action": "start_measurements",
            "measurements_count": 100
        }
        message = json.dumps(command)
        topic = "control"
        client.subscribe(topic)
        
        # Send command to start measurements on the ESP32
        self.result, self.mid = client.publish(topic, message)

        if self.result == mqtt.MQTT_ERR_SUCCESS:
            print("Successfully published control to topic")
        else:
            print(f"failed to publish a message, error number:{self.result}")
        
        time.sleep(1)
        client.disconnect() # Because of this not being here, messages were not deployed to broker

    def receive_measurements(self):
        # Because is another Thread, we need to connect to broker again
        client = self.connect_to_broker() # Getting a MQTT client object
        received_measurements = 0
        # Subscribe to the topic for receiving measurements
        topic = "resistances"
        client.subscribe(topic)
        print("Subscribed to topic:", topic)

        # Start background thread for MQTT communication
        client.loop_start()
        while len(self.measurements) < 100:
            time.sleep(0.01)

        time.sleep(1)       # Sleep to wait for next message
        client.disconnect() # Disconnecting MQTT after receiving message
        # Receive and process measurements from the ESP32

    # Check the publish status in the on_publish callback
    def on_publish(self, client, userdata, mid):
        if mid == mid:
            print("Command published successfully")
        else:
            print("Failed to publish command")

    # Start temperature measurements after recognition
    def start_measurement_thread(self):
        client = self.connect_to_broker()
        
        # Set the on_publish callback
        client.on_publish = self.on_publish

        client.loop_start()
        
        topic = "temperature"
        client.subscribe(topic)
        command = {
            "action": "start/temperature",
            "measurements_count": 100
        }
        message = json.dumps(command)

        # Publish the message
        self.mid = client.publish(topic, message)[1]
 
        '''
        # Disable the button to prevent multiple clicks
        self.start_calculated_button.config(state=tk.DISABLED)
        measurement_thread = Thread(target=self.start_temperature_measurements)
    
        measurement_thread.start()
        '''
    def start_temperature_measurements(self):
        
        client = self.connect_to_broker()
        
        # Set the on_publish callback
        client.on_publish = self.on_publish

        client.loop_start()
        
        topic = "temperature"
        client.subscribe(topic)
        command = {
            "action": "start/temperature"
        }
        message = json.dumps(command)

        # Publish the message
        self.mid = client.publish(topic, message)[1]
 
    def additional_code(self):   
        print("additional code called")
        average_first = sum(self.measurement_pack_first)/len(self.measurement_pack_first)
        average_second = sum(self.measurement_pack_second)/len(self.measurement_pack_second)
        average_third = sum(self.measurement_pack_third)/len(self.measurement_pack_third)

        print(average_first)
        print(average_second)
        print(average_third)

        data = [
            (average_first, self.temperatures[0]),
            (average_second , self.temperatures[1]),
            (average_third , self.temperatures[2])
        ]

        print(data)   
        self.sensor_type = training_data.recognize_instrument(data)
        # Define the known temperature-resistance values for each sensor type
        self.sensor_type_label.config(text=f"Sensor Type: {self.sensor_type}")

        '''
        mqtt_thread2 = Thread(target=self.start_temperature_measurements)
        mqtt_thread2.start()
        
        '''
        time.sleep(5)
        print("Additional code execution completed.")

    # Function which starts process, sends command to start measurements
    def start_measurements_process(self, i):
        # We are calling send_command to send command for starting measurements
        self.send_command()
        # We are calling receive_measurements 
        mqtt_thread = Thread(target=self.receive_measurements)
        mqtt_thread.start()

        #self.receive_measurements()    
        
    def start_measurements_button(self):
        window = tk.Tk()
        window.title("Measurements App")
        window.geometry("600x600")

        # Create a frame to hold the widgets
        frame = tk.Frame(window)
        frame.pack(pady=20)

        # Makes three buttons for three temperatures
        for i in range(1, 4):
            button_text = f"Začni meritev temperature št. {i}"
            start_button = tk.Button(frame, text=button_text, command=lambda i=i: self.start_measurements_process(i))
            start_button.pack(anchor="w", pady=5)

            
        # Create the temperature labels, entries, and store buttons
        temperature_frame = tk.Frame(window)
        temperature_frame.pack(pady=20)

        temperature_labels = []
        temperature_entries = []
        store_buttons = []

        for i in range(3):
            label_text = f"Zapiši dejansko vrednost temperature št. {i+1} v °C:"
            temperature_label = tk.Label(temperature_frame, text=label_text, anchor="w", justify="left")
            temperature_label.pack(pady=5, anchor="w")

            temperature_entry = tk.Entry(temperature_frame)
            temperature_entry.pack(pady=5, anchor="w")
            temperature_entries.append(temperature_entry)

            store_button = tk.Button(temperature_frame, text="Potrdi", command=lambda index=i: self.store_temperature(temperature_entries[index].get(), index+1))
            store_button.pack(pady=5, anchor="w")
            store_buttons.append(store_button)
            
        # Create the label to display self.sensor_type
        self.sensor_type_label = tk.Label(window, text="Tip senzorja: ")
        self.sensor_type_label.pack(pady=10)        

        # Create the button to start calculated temperatures
        self.start_calculated_button = tk.Button(window, text="Začni meritve temperature", command=self.start_measurement_thread, state=tk.DISABLED)
        self.start_calculated_button.pack(pady=10)
            
        def check_sensor_type_entry():
            if self.sensor_type:
                self.start_calculated_button.config(state=tk.NORMAL)
            else:
                self.start_calculated_button.config(state=tk.DISABLED)
            window.after(200, check_sensor_type_entry)

        window.after(200, check_sensor_type_entry)

        window.mainloop()
# Create an instance of the App class
app = App()
'''app.run()'''
app.start_measurements_button()



