
from threading import Thread
import paho.mqtt.client as mqtt
import json
import time
import tkinter as tk
import novialgoritem
import numpy as np
import math

class App:
    def __init__(self):
        self.temperature = None
        self.stop_mqtt_thread = False
        self.mqtt_processing_over = False
        self.measurements_received = 0
        self.measurement_pack_received = 0
        self.measurements = []
        self.measurement_pack_first = []
        self.measurement_pack_second = []
        self.measurement_pack_third = []
        self.new_second_table = []
        self.new_third_table = []
        self.temperatures = []
        self.sensor_type = None


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
        topic = message.topic
        payload = json.loads(message.payload.decode('utf-8'))
        print("on_message called")
        
        if topic == "resistances":
            resistance = payload["R"]                       
            self.measurements.append(resistance) # to je lista iz katere shranjujemo
            print("Appending one resistance")
            self.measurements_received += 1

            print("Received resistance measurement:", resistance)
            if len(self.measurements) == 10 and not self.measurement_pack_first:
                self.measurement_pack_first = self.measurements[:]
                self.measurements.clear()
                self.measurement_pack_received += 1
                print("Sprejeta prva lista:", self.measurement_pack_first)
            
            if len(self.measurement_pack_first) == 10 and not self.new_second_table:                
                for i in range(len(self.measurements)): 
                    self.new_second_table.append(self.measurements[i])
                    self.measurements.clear()
                    self.measurement_pack_received += 1
                    print("Sprejeta druga lista:", self.new_second_table)

            if len(self.measurement_pack_first) == 10 and len(self.new_second_table) == 10 and not self.new_third_table:
                for i in range(len(self.measurements)):    
                    self.new_third_table.append(self.measurements[i])
                    self.measurements.clear()
                    self.measurement_pack_received += 1
                    print("Sprejeta tretja lista:", self.new_third_table)

            if (
                len(self.measurement_pack_first) == 10
                and len(self.new_second_table) == 10
                and len(self.new_third_table) == 10
            ):
                self.additional_code() 

        if topic == "temperature":  
            resistance = payload["R"]

            if self.sensor_type == "PT100":
                alfa = 0.00385
                delta = 1.5
                A = alfa*(1+delta/100)
                B = -alfa*delta*0.0001
                PT100T = (-A + math.sqrt(A*A -4*B*(1-resistance/100)))/(2*B)
                print(PT100T)
            elif self.sensor_type == "PT1000":
                alfa = 0.00385
                delta = 1.5
                A = alfa*(1+delta/100)
                B = -alfa*delta*0.0001
                R = 0
                PT1000T = (-A + math.sqrt(A*A -4*B*(1-resistance/1000)))/(2*B)
                print(PT1000T)
            elif self.sensor_type == "TH5K":    
                '''            
                T1 = # Assign the value of T1 here
                T2 = # Assign the value of T2 here
                T3 = # Assign the value of T3 here
                TR1 = # Assign the value of TR1 here
                TR2 = # Assign the value of TR2 here
                TR3 = # Assign the value of TR3 here
                Rth = # Assign the value of Rth here
                
                gamma2 = (1/T2 - 1/T1) / (math.log(TR2) - math.log(TR1))
                gamma3 = (1/T3 - 1/T1) / (math.log(TR3) - math.log(TR1))
                thC = (gamma3 - gamma2) / (math.log(TR3) - math.log(TR2)) * (math.log(TR1) + math.log(TR2) + math.log(TR3))**-1
                thB = gamma2 - thC * (math.log(TR1)**2 + math.log(TR1) * math.log(TR2) + math.log(TR2)**2)
                thA = 1/T1 - (thB + math.log(TR1)**2 * thC) * math.log(TR1)
                T_th = 1 / (thA + thB * math.log(Rth) + thC * math.log(Rth)**3) - 273.15
                '''
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
        client.subscribe("control")
        client.subscribe("resistances")
    
        print("Python MQTT established")

        return client # We return client to use as a object
    
    def send_command(self):
        client = self.connect_to_broker()

        measurements_count = 10
        command = {
            "action": "start_measurements",
            "measurements_count": 10
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
        self.client_disconnect() # Because of this not being here, messages were not deployed to broker

    def receive_measurements(self):
        # Connect to MQTT broker
        client = self.connect_to_broker() # Getting a MQTT client object
        # Subscribe to the topic for receiving measurements
        topic = "resistances"
        client.subscribe(topic)
        print("Subscribed to topic:", topic)

        # Start background thread for MQTT communication
        client.loop_start()

        #while self.measurements_received < 10:
        #   time.sleep(1)
        
        print(f"Received measurements: ", self.measurements)

        # Remember to disconnect or handle the disconnection properly when you're done.
        client.disconnect()
        # Receive and process measurements from the ESP32


            
    # Check the publish status in the on_publish callback
    def on_publish(self, client, userdata, mid):
        if mid == mid:
            print("Command published successfully")
        else:
            print("Failed to publish command")

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
        average_first = sum(self.measurement_pack_first)/len(self.measurement_pack_first)
        average_second = sum(self.new_second_table)/len(self.new_second_table)
        average_third = sum(self.new_third_table)/len(self.new_third_table)
     
        print(average_first)
        print(average_second)
        print(average_third)
        average = np.array([average_first, average_second, average_third])
        
        print(self.temperatures)
        self.sensor_type = novialgoritem.recognizeInstrument(average, self.temperatures)
        # Define the known temperature-resistance values for each sensor type
        self.sensor_type_label.config(text=f"Sensor Type: {self.sensor_type}")

        mqtt_thread2 = Thread(target=self.start_temperature_measurements)
        mqtt_thread2.start()
        
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
        window.geometry("1200x600")

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
        self.sensor_type_label = tk.Label(window, text="Sensor Type: ")
        self.sensor_type_label.pack(pady=10)        

        # Create the button to start calculated temperatures
        start_calculated_button = tk.Button(window, text="Start Calculated Temperatures", command=self.start_temperature_measurements, state=tk.DISABLED)
        start_calculated_button.pack(pady=10)
            
        def check_sensor_type_entry():
            if self.sensor_type:
                start_calculated_button.config(state=tk.NORMAL)
            else:
                start_calculated_button.config(state=tk.DISABLED)
            window.after(200, check_sensor_type_entry)

        window.after(200, check_sensor_type_entry)

        window.mainloop()
# Create an instance of the App class
app = App()
'''app.run()'''
app.start_measurements_button()




