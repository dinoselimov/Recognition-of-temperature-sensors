#include <Arduino.h>
#include <Wire.h>
#include "ADS1X15.h"
#include <iostream>
using namespace ADS1X15;

//ADS1015<TwoWire> ads(Wire); /* Use this for the 12-bit version */
ADS1115<TwoWire> ads(Wire); /* Use this for the 16-bit version */  


float wheatstone_resistance(float output_voltage){
  float R_0 = 980;
  float Rth = R_0*((3.268/output_voltage) - 1);
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

void setup(void)
{
  Serial.begin(9600);
  Serial.println("Hello!");

  Serial.println("Getting single-ended readings from AIN0..3");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV/ADS1015, 0.1875mV/ADS1115)");

  // The ADC input range (or gain) can be changed via the following
  // functions, but be careful never to exceed VDD +0.3V max, or to
  // exceed the upper and lower limits if you adjust the input range!
  // Setting these values incorrectly may destroy your ADC!
  //                                                                ADS1015  ADS1115
  //                                                                -------  -------
  // ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV (default)
  // ads.setGain(GAIN_ONE);        // 1x gain   +/- 4.096V  1 bit = 2mV      0.125mV
  // ads.setGain(GAIN_TWO);        // 2x gain   +/- 2.048V  1 bit = 1mV      0.0625mV
  // ads.setGain(GAIN_FOUR);       // 4x gain   +/- 1.024V  1 bit = 0.5mV    0.03125mV
  // ads.setGain(GAIN_EIGHT);      // 8x gain   +/- 0.512V  1 bit = 0.25mV   0.015625mV
  // ads.setGain(GAIN_SIXTEEN);    // 16x gain  +/- 0.256V  1 bit = 0.125mV  0.0078125mV

  ads.begin();
  ads.setGain(Gain::TWOTHIRDS_6144MV);
  ads.setDataRate(Rate::ADS1015_250SPS);
}

void temp(int channel, const char* sensor_type){
  int16_t adc;
  float volt, res, temp;
  adc = ads.readADCSingleEnded(channel);
  volt = ads.computeVolts(adc);
  res = wheatstone_resistance(volt);
  temp = calculateTemperature(res, sensor_type);

  Serial.print("AIN"); Serial.print(channel); Serial.print("  "); Serial.print(volt, 3); Serial.println("V"); // Print with 3 decimal places
  Serial.print(" "); Serial.print(temp, 3);  Serial.println("T");Serial.println(); // Print with 3 decimal places
}

void loop(void)
{
  
  Serial.println("-----------------------------------------------------------");
  temp(0, "PT1000");
  temp(1, "TH10K");
  temp(2, "TH5K");
  temp(3, "PT100");

  delay(1000);
}

