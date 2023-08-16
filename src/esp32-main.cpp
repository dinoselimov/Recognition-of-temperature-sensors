

#include <Arduino.h>
#include <PubSubClient.h>
#include <json.h>
#include <string.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include <iostream>

#define PT10032 32 // Analog IN
#define PT10033 33 // Analog IN
#define DRUGIMERILNIK 34 // DRUGI ANALOGNI

const char* ssid = "GNX611368";
const char* password = "12345678";
const char *mqttServer = "broker.hivemq.com";
const int mqttPort = 1883; // pri 1883 dela, pri 8883 ne
const char* mqtt_user = "DinoSelim";
const char* mqtt_password = "";
const unsigned long MEASUREMENT_INTERVAL = 5000; // Dolžina intervala med dvema meritvama
const char* control_topic = "control";
const char* topicOne = "upornosti/one";
const char* topicTwo = "drugi/merilnik";
const char* topicTemperature = "temperature";

bool start_temperature_measurement = false; //uporablja se po prepoznavi, da začnemo druga merjenja

double ReadVoltage(byte pin);

WiFiClient espClient;
PubSubClient client(espClient);

float adc_voltage(float left_voltage){
  float output_voltage = left_voltage * (3.3/pow(2,12));
  return output_voltage; //to je v pravih vrednostih
}

int wheatstone_resistance(float output_voltage){
  float R_0 = 1000;
  float Rth = R_0*((3.3/output_voltage) - 1);
  return Rth;
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Handle received MQTT messages
  Serial.println("Message received!"); 
  if (strncmp(topic, control_topic, length) == 0) {
    String message = "";
    for (int i = 0; i < length; i++) {
      message += (char)payload[i]; //pretvorba payloada v string
    }

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

    if (doc.containsKey("measurements_count")) {
      measurements_count = doc["measurements_count"].as<int>();
    }
    
    // Check the received action
    if (action == "start_measurements") {
      // Start measuring temperatures
      for (int i = 0; i < measurements_count; i++) {
      // TODO: Start the temperature measurement here
      
      // Perform the temperature measurement and obtain the resistance value
   //  float Vin2 = analogRead(PT10033);
      float voltage = ReadVoltage(PT10033);
      float resistance = wheatstone_resistance(voltage);
      Serial.println(resistance);

      // Create a JSON document to store the resistance value
      StaticJsonDocument<80> resistanceDoc;
      char output[50];
      resistanceDoc["R"] = resistance;
      serializeJson(resistanceDoc, output);

      // Publish the resistance value to the MQTT topic
      String topicStr = topicOne; // Modify the topic according to the temperature you are measuring
      client.publish(topicStr.c_str(), output, false); // QoS 0

      // Delay for 1 second before the next measurement
      delay(1000);
    }
    if (action = "start/temperature"){
  //    start_temperature_measurement = true;
    }
  }
}

}

void reconnect(){
  Serial.println("Connecting to MQTT Broker...");
  while (!client.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
      
      if (client.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // subscribe to topic
        client.subscribe("upornosti/one");
        client.subscribe(control_topic);
      }
    }
}

void setup() {
  Serial.begin(9600); 

  // Povezati se z lokalnim WiFi omrežjem
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
    }
  Serial.println("");
  Serial.println("Wifi Connected, IP:");
  Serial.println(WiFi.localIP());

  // Nastavitev MQTT protokola
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
      if (client.connect("ESP32_client")) {
        Serial.println("Connected to MQTT broker!");
        client.subscribe("upornosti/one");
        client.subscribe(control_topic);
        client.subscribe(topicTwo);
        client.subscribe(topicTemperature);
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

  if(start_temperature_measurement){
    float voltage, resistance;
    voltage = ReadVoltage(DRUGIMERILNIK);
    resistance = wheatstone_resistance(voltage);
    Serial.println(resistance);
    StaticJsonDocument<80> resistanceDoc;
    char output[50];
    resistanceDoc["R"] = resistance;
    serializeJson(resistanceDoc, output);
    String topicStr = topicTemperature; // Modify the topic according to the temperature you are measuring
    client.publish(topicStr.c_str(), output, false); // QoS 0

    // Delay for 1 second before the next measurement
    delay(1000);
  }

}

double ReadVoltage(byte pin){
  double reading = analogRead(pin); // Reference voltage is 3v3 so maximum reading is 3v3 = 4095 in range 0 to 4095
  if(reading < 1 || reading > 4095) return 0;
  return -0.000000000000016 * pow(reading,4) + 0.000000000118171 * pow(reading,3)- 0.000000301211691 * pow(reading,2)+ 0.001109019271794 * reading + 0.034143524634089;
} // poskus kalibracije


/* ADC readings v voltage
 *  y = -0.000000000009824x3 + 0.000000016557283x2 + 0.000854596860691x + 0.065440348345433
 // Polynomial curve match, based on raw data thus:
 *   464     0.5
 *  1088     1.0
 *  1707     1.5
 *  2331     2.0
 *  2951     2.5 
 *  3775     3.0
 *  
 */
