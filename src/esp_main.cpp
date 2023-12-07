#define PT10032 32 // Analog IN
#define PT10033 33 // Analog IN
#define DRUGIMERILNIK 34 // DRUGI ANALOGNI

#include <Arduino.h>
#include <PubSubClient.h>
#include <json.h>
#include <string.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <iostream>
#include <Wire.h>
#include "ADS1X15.h"

using namespace ADS1X15;

//ADS1015<TwoWire> ads(Wire); /* Use this for the 12-bit version */
ADS1115<TwoWire> ads(Wire); /* Use this for the 16-bit version */  

// Data about WiFi, MQTT broker, MQTT topics, and other constants
const char* ssid = "GNX611368";
const char* password = "12345678";
const char *mqttServer = "broker.hivemq.com";
const int mqttPort = 1883; // pri 1883 dela, pri 8883 ne
const char* mqtt_user = "DinoSelim";
const char* mqtt_password = "mqttpassword";
const unsigned long MEASUREMENT_INTERVAL = 5000; // Dolžina intervala med dvema meritvama
const char* control_topic = "control";
const char* topicOne = "resistances";
const char* topicTemperature = "temperature";
const char *topic_start_temperature = "start/temperature";

bool start_temperature_measurement = false; //uporablja se po prepoznavi, da začnemo druga merjenja

double ReadVoltage();

// Connecting to WiFi and MQTT library
WiFiClient espClient;
PubSubClient client(espClient);

/*
float adc_voltage(float left_voltage){
  float output_voltage = left_voltage * (3.3/pow(2,12));
  return output_voltage; //to je v pravih vrednostih
}
*/

// Calculating voltage divider with measured voltage of source and resistance of divider
int voltage_divider(float output_voltage){
  float R_0 = 980;
  float Rth = R_0*((3.266/output_voltage) - 1);
  return Rth;
}
 
void callback(char* topic, byte* payload, unsigned int length) {
  // Handle received MQTT messages
  Serial.println(topic);
  if (strncmp(topic, control_topic, length) == 0) {
    String message = "";
    for (int i = 0; i < length; i++) {
      message += (char)payload[i]; // Convert from payload to string
    }

    Serial.println(message);
    // Parse the received JSON message
    // Assuming the message has the format: {"action": "start_measurements", "measurements_count": 10}
    // Extract the action and measurements_count values
    String action = "";
    int measurements_count = 0;

    // Parse the JSON message
    DynamicJsonDocument doc(256); 
    DeserializationError error = deserializeJson(doc, message);
    Serial.println("JSON message recieved:" + message);
    
    // Check for parsing errors
    if (error) {
      Serial.print("Failed to parse JSON message: ");
      Serial.println(error.c_str());
      return;
    }

    // Extract the values
    if (doc.containsKey("action")) {
      action = doc["action"].as<String>();
    }
    Serial.println(action); 
     
    if (doc.containsKey("measurements_count")) {
      measurements_count = doc["measurements_count"].as<int>();
    }
    Serial.println(action);
    
    // Check the received action
    if (action == "start_measurements") {
      // Start measuring temperatures
      for (int i = 0; i < measurements_count; i++) {        
        // Perform the temperature measurement and obtain the resistance value
        float voltage = ReadVoltage();
        float resistance = voltage_divider(voltage);
        Serial.println(resistance);

        // Create a JSON document to store the resistance value
        StaticJsonDocument<80> resistanceDoc;
        char output[50];
        resistanceDoc["R"] = resistance;
        serializeJson(resistanceDoc, output);

        // Publish the resistance value to the MQTT topic
        String topicStr = topicOne; 
        client.publish(topicStr.c_str(), output, false); // QoS 0

        delay(100);
    }
    if (action == "start/temperature"){
      // After recognition, received command to start measuring actual temperature
      start_temperature_measurement = true;
    }
  }
}
}

// Function to reconnect if we are disconnected disconnect
void reconnect(){
  Serial.println("Connecting to MQTT Broker...");
  while (!client.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
      
      if (client.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // Subscribe to four topics
        client.subscribe("resistances");
        client.subscribe(control_topic);
        client.subscribe("start/temperature");
        client.subscribe(topicTemperature);

      }
    }
}

// Connect with local WiFi, initialization of ADS, connection with MQTT broker and setting callback function
void setup() {
  Serial.begin(9600); 

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
    }
  Serial.println("");
  Serial.println("Wifi Connected, IP:");
  Serial.println(WiFi.localIP());

  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  ads.begin();
  ads.setGain(Gain::TWOTHIRDS_6144MV);
  ads.setDataRate(Rate::ADS1015_250SPS);

  // Nastavitev MQTT protokola
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
      if (client.connect("ESP32_client")) {
        Serial.println("Connected to MQTT broker!");
        client.subscribe(topicOne);
        client.subscribe(control_topic);
        client.subscribe(topicTemperature);
        client.subscribe("start/temperature");
      }else {
        Serial.println("Failed to connect to MQTT broker. Retrying in 5 seconds...");
        delay(5000);
      }
  }
  delay(1000);
}

void loop() {
  if(!client.connected()){
    reconnect();
  }    
  client.loop();

  // After recognition, this section of code sends resistances and measures actual temperatures
  if(start_temperature_measurement){
    float voltage, resistance;
    voltage = ReadVoltage();
    resistance = voltage_divider(voltage);
    Serial.println(resistance);
    StaticJsonDocument<50> resistanceDoc;
    char output[50];
    resistanceDoc["R"] = resistance;
    serializeJson(resistanceDoc, output);
    Serial.println(output);
    String topicStr = topicTemperature; 
    client.publish(topicStr.c_str(), output, false); // QoS 0

    // Delay for next measurement
    delay(1000);
  }
}

// ADS1115 function for measuring voltage
double ReadVoltage(){
  int16_t adc0, adc1, adc2, adc3;
  float volts0, volts1, volts2, volts3;

  adc0 = ads.readADCSingleEnded(0);
  volts0 = ads.computeVolts(adc0);

  Serial.println("-----------------------------------------------------------");

  return volts0;
  } 
