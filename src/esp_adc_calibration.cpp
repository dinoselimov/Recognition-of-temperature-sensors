#include <iostream>
#include <Arduino.h>
#include "esp_adc_cal.h"
#include "driver/adc.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include <cmath>
#include <float.h>
double ReadVoltage(byte pin);
float calculateTemperature(float resistance, std::string sensorType);

float wheatstone_resistance(float output_voltage){
  float R_0 = 980;
//  float Rth = R_0*((3.270/output_voltage) - 1);
  float Rth = R_0*((3.272/output_voltage) - 1);
  return Rth;
}

void setup() {
  Serial.begin(9600);
  
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);


  float napetost, upornost, temperatura;
  float napetost2, upornost2, temperatura2;
  float napetost3, upornost3, temperatura3;
  float napetost4, upornost4, temperatura4;
  float upornosti_povprecne1[100],upornosti_povprecne2[100], upornosti_povprecne3[100], upornosti_povprecne4[100];
  float napetosti_povprecne1[100],napetosti_povprecne2[100], napetosti_povprecne3[100], napetosti_povprecne4[100];
  float temperature_povprecne1[100], temperature_povprecne2[100], temperature_povprecne3[100], temperature_povprecne4[100];
  float upornosti_skupne1, upornosti_skupne2, upornosti_skupne3, upornosti_skupne4;
  float temperature_skupne1, temperature_skupne2, temperature_skupne3, temperature_skupne4;
  float napetosti_skupne1, napetosti_skupne2, napetosti_skupne3, napetosti_skupne4;
  float povprecje_r1, povprecje_t1, povprecje_r2, povprecje_t2, povprecje_r3, povprecje_t3, povprecje_r4, povprecje_t4;
  float povprecje_n1, povprecje_n2, povprecje_n3, povprecje_n4;
  
for(int i = 0; i < 100; i++){
  Serial.println("TH5K");
  napetost = ReadVoltage(32);
  napetosti_povprecne1[i] = napetost;
  upornost = wheatstone_resistance(napetost);
  upornosti_povprecne1[i] = upornost;
  Serial.println(upornost);
  temperatura = calculateTemperature(upornost, "TH5K");
  temperature_povprecne1[i] = temperatura;
  Serial.println(temperatura);

  Serial.println("PT1000");
  napetost2 = ReadVoltage(32);
  napetosti_povprecne2[i] = napetost2;
  upornost2 = wheatstone_resistance(napetost2);
  upornosti_povprecne2[i] = upornost2;
  Serial.println(upornost2);
  temperatura2 = calculateTemperature(upornost2, "PT1000");
  temperature_povprecne2[i] = temperatura2;
  Serial.println(temperatura2);
  
  Serial.println("PT100");
  napetost3 = ReadVoltage(33);
  napetosti_povprecne3[i] = napetost3;
  upornost3 = wheatstone_resistance(napetost3);
  upornosti_povprecne3[i] = upornost3;
  Serial.println(upornost3);
  temperatura3 = calculateTemperature(upornost3, "PT100");
  temperature_povprecne3[i] = temperatura3;
  Serial.println(temperatura3);
  
  Serial.println("TH10K");
  napetost4 = ReadVoltage(35);
  napetosti_povprecne4[i] = napetost4;
  upornost4 = wheatstone_resistance(napetost4);
  Serial.println(upornost4);
  upornosti_povprecne4[i] = upornost4;
  temperatura4 = calculateTemperature(upornost4, "TH10K");
  temperature_povprecne4[i] = temperatura4;
  Serial.println(temperatura4);
  
  delay(100);
}

    for(int j = 0; j < 100; j++){
      temperature_skupne1 += temperature_povprecne1[j];
      temperature_skupne2 += temperature_povprecne2[j];
      temperature_skupne3 += temperature_povprecne3[j];
      temperature_skupne4 += temperature_povprecne4[j];

      upornosti_skupne1 += upornosti_povprecne1[j];
      upornosti_skupne2 += upornosti_povprecne2[j];
      upornosti_skupne3 += upornosti_povprecne3[j];
      upornosti_skupne4 += upornosti_povprecne4[j];

      napetosti_skupne1 += napetosti_povprecne1[j];
      napetosti_skupne2 += napetosti_povprecne2[j];
      napetosti_skupne3 += napetosti_povprecne3[j];
      napetosti_skupne4 += napetosti_povprecne4[j];
    }
    povprecje_r1 = upornosti_skupne1/100;
    povprecje_r2 = upornosti_skupne2/100;
    povprecje_r3 = upornosti_skupne3/100;
    povprecje_r4 = upornosti_skupne4/100;

    povprecje_t1 = calculateTemperature(povprecje_r1, "TH5K");
    povprecje_t2 = calculateTemperature(povprecje_r2, "PT1000");
    povprecje_t3 = calculateTemperature(povprecje_r3, "PT100");
    povprecje_t4 = calculateTemperature(povprecje_r4, "TH10K");

    povprecje_n1 = napetosti_skupne1/100;
    povprecje_n2 = napetosti_skupne2/100;
    povprecje_n3 = napetosti_skupne3/100;
    povprecje_n4 = napetosti_skupne4/100;

    Serial.print("TH5K Povprečna R = ");
    Serial.println(povprecje_r1);
    Serial.print(" TH5K Povprečna T = ");
    Serial.println( povprecje_t1);
    
    Serial.print(" TH5K Povprečna N = ");
    Serial.println( povprecje_n1, 3);
    
    Serial.print("PT1000 Povprečna R =  ");
    Serial.println(povprecje_r2);
    Serial.print(" PT1000 Povprečna T = ");
    Serial.println(povprecje_t2);
    Serial.print(" PT1000 Povprečna N = ");
    Serial.println(povprecje_n2, 3);
    
    Serial.print("PT100 Povprečna R =  ");
    Serial.println(povprecje_r3);
    Serial.print(" PT100 Povprečna T = ");
    Serial.println(povprecje_t3);
    Serial.print(" PT100 Povprečna N = ");
    Serial.println(povprecje_n3,3);
    
    Serial.print("TH10K Povprečna R =  ");
    Serial.println(povprecje_r4);
    Serial.print(" TH10K Povprečna T = ");
    Serial.println(povprecje_t4);
    Serial.print(" TH10K Povprečna N = ");
    Serial.println(povprecje_n4, 3);
  delay(5000);
  
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

        float thA = 1.2874E-03;
        float thB = 2.3573E-04;
        float thC = 9.5052E-08;
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

double ReadVoltage(byte pin){
  float reading = analogRead(pin); // Reference voltage is 3v3 so maximum reading is 3v3 = 4095 in range 0 to 4095
  float calibrated, reading_analog, calibrated_4;
  Serial.println("Branje");
  Serial.println(reading);
  if(reading < 1 || reading > 4095) return 0;
  reading_analog = reading * 3.272/4095; // referenca je pomerjena 3.272, pretvorimo iz digitalnog v analogno
  return reading_analog;

  // nekaj poskusov kalibracije
  //return -0.000000000009824 * pow(reading,3) + 0.000000016557283 * pow(reading,2) + 0.000854596860691 * reading + 0.065440348345433;
  //return -0.000000000000016 * pow(reading,4) + 0.000000000118171 * pow(reading,3)- 0.000000301211691 * pow(reading,2)+ 0.001109019271794 * reading + 0.034143524634089;  
  // return  coeff1 * std::pow(reading, 2) + coeff2 * reading + coeff3;
  //return ((reading)/4095) * 3.3 * 1.114;
  //if(reading > 2800 || (reading < 700 && reading > 400))
  /*
  float internal_voltage = 1.114;
  float full_scale_digital = 1386;
  calibrated = (reading / full_scale_digital) * internal_voltage;
  return calibrated;
  */
  //calibrated = -0.03841 * pow(reading_analog,2) + 1.086 * reading_analog + 0.1052;
  //calibrated_4 = -0.01288*pow(reading_analog,4) + 0.05475*pow(reading_analog,3) - 0.08338*pow(reading_analog,2) + 1.064*reading_analog + 0.1165;
  //calibrated_4 = -0.03812*pow(reading_analog,2) + 1.083*reading_analog + 0.0996;
  //calibrated_4 = -0.03708 * pow(reading_analog,2) + 1.081*reading_analog + 0.1005;
  //calibrated_4 = -0.03761*pow(reading_analog,2) + 1.082*reading_analog + 0.1;
  // calibrated_4 = -0.02134*pow(reading_analog,4) + 0.102*pow(reading_analog,3)- 0.1659*pow(reading_analog,2) + 1.113*reading_analog+ 0.1074;
  //return -25.01*pow(reading,4) + 110.4*pow(reading,3) - 156.9*pow(reading,2) + 1397*reading + 87.94;
  //return reading * 3.272/4095;
  //else
  //return -0.000000000000016 * pow(reading,4) + 0.000000000118171 * pow(reading,3)- 0.000000301211691 * pow(reading,2)+ 0.001109019271794 * reading + 0.034143524634089;  
  
  /*

  Serial.println("KaliBranje");
  calibrated = (int)ADC_LUT[reading];    // get the calibrated value from LUT

  Serial.println(calibrated);
  return calibrated; 
  */
  // get the calibrated value from LUT
  
  /*
  if (reading>3000)
  {
  reading = 0.0005 * reading + 1.0874;
  }
  else
  {
  reading = 0.0008 * reading + 0.1372;
  }
  
  return reading;
  */
  
} // Added an improved polynomial, use either, comment out as required


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


void loop(){

}
