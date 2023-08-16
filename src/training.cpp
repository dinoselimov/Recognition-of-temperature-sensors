#if 0

#include <iostream>
#include <cmath>
#include <Arduino.h>
#include "esp_adc_cal.h"
#include "driver/adc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define PT10033 33 
#define ADC_PIN 33
#define AN_Pot1 33
#define voltage_divider_offset 1.0 // Should be a value of 2.000, but ADC input impedance loads the voltage divider, requiring a correction

float ReadVoltage (byte ADC_Pin);
uint32_t readADC_Cal(int ADC_Raw);


float adc_voltage(float left_voltage){
  float output_voltage = left_voltage * (3.3/(pow(2,12)-1));
  return output_voltage; 
}
float wheatstone_resistance(float output_voltage){
  float R_0 = 980;
  float Rth = R_0*((3.3/output_voltage) - 1);
  return Rth;
}

float calculateTemperature(float resistance, std::string sensorType) {
    float alfa, delta, A, B;
    float PT100T, PT1000T, T1, T2, T3, TR1, TR2, TR3, Rth;
    float gamma2, gamma3, thC, thB, thA, T_th;

    if (sensorType == "PT100") {
        alfa = 0.00385;
        delta = 1.5;
        A = alfa * (1 + delta / 100);
        B = -alfa * delta * 0.0001;
        PT100T = (-A + std::sqrt(A * A - 4 * B * (1 - resistance / 100))) / (2 * B);
        std::cout << PT100T << std::endl;
        return PT100T;
    } else if (sensorType == "PT1000") {
        alfa = 0.00385;
        delta = 1.5;
        A = alfa * (1 + delta / 100);
        B = -alfa * delta * 0.0001;
        PT1000T = (-A + std::sqrt(A * A - 4 * B * (1 - resistance / 1000))) / (2 * B);
        std::cout << PT1000T << std::endl;
        return PT1000T;
    } else if (sensorType == "TH5K") {
        /*
        T1 = 273.15 + 26;
        T2 = 273.15 + 56.3;
        T3 = 273.15 + 85.5;
        TR1 = 6118;
        TR2 = 1647;
        TR3 = 546;
        */        
        float T1 = 273.15+2.88;
        float T2 = 273.15+87.4;
        float T3 = 273.15+22.31;
        float TR1 = 14738.46;
        float TR2 = 502.4;
        float TR3 = 5686.3;
        
        gamma2 = (1 / T2 - 1 / T1) / (std::log(TR2) - std::log(TR1));
        gamma3 = (1 / T3 - 1 / T1) / (std::log(TR3) - std::log(TR1));
        thC = (gamma3 - gamma2) / (std::log(TR3) - std::log(TR2)) * (std::log(TR1) + std::log(TR2) + std::log(TR3));
        thB = gamma2 - thC * (std::log(TR1) * std::log(TR1) + std::log(TR1) * std::log(TR2) + std::log(TR2) * std::log(TR2));
        thA = 1 / T1 - (thB + std::log(TR1) * std::log(TR1) * thC) * std::log(TR1);
        T_th = std::abs(1 / (thA + thB * std::log(resistance) + thC * std::log(resistance) * std::log(resistance) * std::log(resistance)) - 273.15);

        return T_th;   
    } else if (sensorType == "TH10K"){
        /*
        float T1 = 273.15+0;
        float T2 = 273.15+100;
        float T3 = 273.15+50;
        float TR1 = 32650;
        float TR2 = 678.3;
        float TR3 = 3603;
        
        gamma2 = (1 / T2 - 1 / T1) / (std::log(TR2) - std::log(TR1));
        gamma3 = (1 / T3 - 1 / T1) / (std::log(TR3) - std::log(TR1));
        thC = (gamma3 - gamma2) / (std::log(TR3) - std::log(TR2)) * (std::log(TR1) + std::log(TR2) + std::log(TR3));
        thB = gamma2 - thC * (std::log(TR1) * std::log(TR1) + std::log(TR1) * std::log(TR2) + std::log(TR2) * std::log(TR2));
        thA = 1 / T1 - (thB + std::log(TR1) * std::log(TR1) * thC) * std::log(TR1);
        */
        thA = 0.001125308852122;
        thB = 0.000234711863267;
        thC = 0.000000085663516;
        T_th = std::abs(1 / (thA + thB * std::log(resistance) + thC * std::log(resistance) * std::log(resistance) * std::log(resistance)) - 273.15);

        return T_th;   

    }
}
    
void setup(){
    Serial.begin(9600);
    float resistances[100] = {0.0};
    float temperatures[100] = {0.0};
    float temperatures_average;
    float resistances_average;
    /*
    for(int i = 0; i < 100; i++){
        float Vin2 = analogRead(PT10033);
        float voltage = adc_voltage(Vin2);
        Serial.println(voltage);
        float resistance = wheatstone_resistance(voltage);
        resistances[i] = resistance;
        temperatures[i] = calculateTemperature(resistances[i], "PT1000");
        Serial.print("R = ");
        Serial.print(resistances[i]);
        Serial.print("T = ");
        Serial.println(temperatures[i]);
        
        delay(100);
    }
    for(int j = 0; j < 100; j++){
        resistances_average += resistances[j];
        temperatures_average += temperatures[j]; 
    }
    resistances_average = resistances_average/100;
    temperatures_average = temperatures_average/100;
    Serial.print("Povprečna R = ");
    Serial.println(resistances_average);
    Serial.print("Povprečna T = ");
    Serial.print(temperatures_average);
    */
}

void loop(){  
  float resistance, resistance2;
  float AN_Pot1_Result, Voltage, voltage, temperature, adj_voltage, analog;
  /*
  analog = analogRead(PT10033);
  voltage = adc_voltage(analog);
  adj_voltage = ReadVoltage(PT10033);
  Serial.println("   adc = " + String(voltage,3) + "v");
  */

  AN_Pot1_Result = analogRead(AN_Pot1);
  Voltage = readADC_Cal(AN_Pot1_Result) / 1000.0;
  //Serial.println(Voltage/1000.0); // Print Voltage (in V)
  Serial.println(Voltage); // Print Voltage (in mV)
  delay(100);
  resistance = wheatstone_resistance(Voltage);
  Serial.println(resistance);

  /*
  resistance2 = wheatstone_resistance(voltage);
  Serial.println(resistance);
  Serial.println(resistance2);
  */
  temperature = calculateTemperature(resistance, "PT1000");
  Serial.println(temperature);
  delay(5000);
}


float ReadVoltage(byte ADC_Pin) {
  float calibration  = 1.000; // Adjust for ultimate accuracy when input is measured using an accurate DVM, if reading too high then use e.g. 0.99, too low use 1.01
  float vref = 1100;
  esp_adc_cal_characteristics_t adc_chars;
  esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 1100, &adc_chars);
  vref = adc_chars.vref; // Obtain the device ADC reference voltage
  return (analogRead(ADC_Pin) / 4095.0) * 3.3 * voltage_divider_offset * (1100 / vref) * calibration;  // ESP by design reference voltage in mV
}


uint32_t readADC_Cal(int ADC_Raw){
  esp_adc_cal_characteristics_t adc1_chars;

  esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 0, &adc1_chars);
  adc1_config_width(ADC_WIDTH_BIT_12);
  adc1_config_channel_atten(ADC1_CHANNEL_5, ADC_ATTEN_DB_11);


  int adc_value = adc1_get_raw(ADC1_CHANNEL_5);
  uint32_t mV = esp_adc_cal_raw_to_voltage(adc1_get_raw(ADC1_CHANNEL_5), &adc1_chars);
  printf("Voltage: %d mV", mV);
  return mV;
}

// The esp_adc_cal/include/esp_adc_cal.h API provides functions to correct for differences
// in measured voltages caused by variation of ADC reference voltages (Vref) between chips.
// Per design the ADC reference voltage is 1100 mV, however the true reference voltage can
// range from 1000 mV to 1200 mV amongst different ESP32's

#endif