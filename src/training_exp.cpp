#if 0
#include <Arduino.h>
#include <Wire.h>
#include "ADS1X15.h"
#include <iostream>
using namespace ADS1X15;

//ADS1015<TwoWire> ads(Wire); /* Use this for the 12-bit version */
ADS1115<TwoWire> ads(Wire); /* Use this for the 16-bit version */ 

float get_temperature(int channel, const char* sensor_type);
float calculateTemperature(float resistance, std::string sensorType);


float wheatstone_resistance(float output_voltage){
  float R_0 = 980;
  float Rth = R_0*((3.266/output_voltage) - 1);
  return Rth;
}


float get_temperature(int channel, const char* sensor_type){
  int16_t adc;
  float volt, res, get_temperature;
  adc = ads.readADCSingleEnded(channel);
  volt = ads.computeVolts(adc);
  res = wheatstone_resistance(volt);
  get_temperature = calculateTemperature(res, sensor_type);

  Serial.print("AIN"); Serial.print(channel); Serial.print("  "); Serial.print(volt, 3); Serial.println("V"); // Print with 3 decimal places
  Serial.print(" "); Serial.print(get_temperature, 3);  Serial.println("T");Serial.println(); // Print with 3 decimal places
  return get_temperature;
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
        
        T1 = 273.15 + 25;
        T2 = 273.15 + 0;
        T3 = 273.15 + 90;
        TR1 = 5000;
        TR2 = 13730;
        TR3 = 601;
             
        /*
        float T1 = 273.15+2.88;
        float T2 = 273.15+87.4;
        float T3 = 273.15+22.31;
        float TR1 = 14738.46;
        float TR2 = 502.4;
        float TR3 = 5686.3;
        */
        gamma2 = (1 / T2 - 1 / T1) / (std::log(TR2) - std::log(TR1));
        gamma3 = (1 / T3 - 1 / T1) / (std::log(TR3) - std::log(TR1));
        thC = (gamma3 - gamma2) / (std::log(TR3) - std::log(TR2)) * (std::log(TR1) + std::log(TR2) + std::log(TR3));
        thB = gamma2 - thC * (std::log(TR1) * std::log(TR1) + std::log(TR1) * std::log(TR2) + std::log(TR2) * std::log(TR2));
        thA = 1 / T1 - (thB + std::log(TR1) * std::log(TR1) * thC) * std::log(TR1);
        thA = 0.0012874;
        thB = 0.00023573;
        thC = 0.000000095052;

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

  int16_t adc_0; int16_t adc_1; int16_t adc_2; int16_t adc_3;
  float volt_0; float volt_1; float volt_2; float volt_3;

  float temp0[100]; float temp1[100]; float temp2[100]; float temp3[100];
  float res0[100]; float res1[100]; float res2[100]; float res3[100];

  float res0_av = 0; float res1_av = 0; float res2_av = 0; float res3_av = 0;
  float temp0_av = 0; float temp1_av = 0; float temp2_av = 0; float temp3_av = 0;
  for(int i = 0; i < 100; i++){      
      
    adc_0 = ads.readADCSingleEnded(0);
    volt_0 = ads.computeVolts(adc_0);

    adc_1 = ads.readADCSingleEnded(1);
    volt_1 = ads.computeVolts(adc_1);
    
    adc_2 = ads.readADCSingleEnded(2);
    volt_2 = ads.computeVolts(adc_2);

    adc_3 = ads.readADCSingleEnded(3);
    volt_3 = ads.computeVolts(adc_3);

    temp0[i] = get_temperature(0, "PT1000");
    temp1[i] = get_temperature(1, "TH5K");
    temp2[i] = get_temperature(2, "PT100");
    temp3[i] = get_temperature(3, "TH10K");
    
    res0[i] = wheatstone_resistance(volt_0);
    res1[i] = wheatstone_resistance(volt_1);
    res2[i] = wheatstone_resistance(volt_2);
    res3[i] = wheatstone_resistance(volt_3);
    

  }
  for(int i = 0; i < 100; i++){
    temp0_av = temp0_av + temp0[i];
    temp1_av = temp1_av + temp1[i];
    temp2_av = temp2_av + temp2[i];
    temp3_av = temp3_av + temp3[i];
    
    res0_av = res0_av + res0[i];
    res1_av = res1_av + res1[i];
    res2_av = res2_av + res2[i];
    res3_av = res3_av + res3[i];
  }
  temp0_av = temp0_av / 100;
  temp1_av = temp1_av / 100;
  temp2_av = temp2_av / 100;
  temp3_av = temp3_av / 100;

  res0_av = res0_av / 100;
  res1_av = res1_av / 100;
  res2_av = res2_av / 100;
  res3_av = res3_av / 100;

  Serial.print("PT1000"); Serial.print(" "); Serial.println(temp0_av); Serial.print(" "); Serial.print(res0_av); Serial.println(" ");   
  Serial.print("TH10K"); Serial.print(" "); Serial.println(temp1_av); Serial.print(" "); Serial.print(res1_av); Serial.println(" "); 
  Serial.print("PT100"); Serial.print(" "); Serial.println(temp2_av); Serial.print(" "); Serial.print(res2_av); Serial.println(" "); 
  Serial.print("TH5K"); Serial.print(" "); Serial.println(temp3_av); Serial.print(" "); Serial.print(res3_av); Serial.println(" "); 

  delay(100);
}

void loop(void)
{
  /*
  Serial.println("-----------------------------------------------------------");
  get_temperature(0, "PT1000");
  get_temperature(1, "TH10K");
  get_temperature(2, "PT100");
  get_temperature(3, "TH5K");

  delay(1000);
  */
}

#endif