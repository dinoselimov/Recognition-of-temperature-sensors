import math

class Temperature_Reading:
    def __init__(self):
        self.alfa = 0.00385
        self.delta = 1.5
        self.sensor_type = " "

    # Function which returns temperature depended on sensor type
    def temperature_read(self, resistance): 
        if self.sensor_type == "PT100":
            A = self.alfa*(1 + self.delta/100)
            B = -self.alfa*self.delta*0.0001
            PT100T = (-A + math.sqrt(A*A -4*B*(1-resistance/100)))/(2*B)
            print(PT100T)
        elif self.sensor_type == "PT1000":
            A = self.alfa*(1 + self.delta/100)
            B = -self.alfa*self.delta*0.0001
            PT1000T = (-A + math.sqrt(A*A -4*B*(1-resistance/1000)))/(2*B)
            print(PT1000T)
        elif self.sensorType == "TH5K":
            '''
            T1 = 273.15 + 26
            T2 = 273.15 + 56.3
            T3 = 273.15 + 85.5
            TR1 = 6118
            TR2 = 1647
            TR3 = 546
            '''     
            T1 = 273.15+2.88
            T2 = 273.15+87.4
            T3 = 273.15+22.31
            TR1 = 14738.46
            TR2 = 502.4
            TR3 = 5686.3
            
            gamma2 = (1 / T2 - 1 / T1) / (math.log(TR2) - math.log(TR1))
            gamma3 = (1 / T3 - 1 / T1) / (math.log(TR3) - math.log(TR1))
            thC = (gamma3 - gamma2) / (math.log(TR3) - math.log(TR2)) * (math.log(TR1) + math.log(TR2) + math.log(TR3))
            thB = gamma2 - thC * (math.log(TR1) * math.log(TR1) + math.log(TR1) * math.log(TR2) + math.log(TR2) * math.log(TR2))
            thA = 1 / T1 - (thB + math.log(TR1) * math.log(TR1) * thC) * math.log(TR1)
            T_th = math.abs(1 / (thA + thB * math.log(resistance) + thC * math.log(resistance) * math.log(resistance) * math.log(resistance)) - 273.15)

            return T_th   
        elif self.sensor_type == "TH10K":
            T1 = 273.15+0
            T2 = 273.15+100
            T3 = 273.15+50
            TR1 = 32650
            TR2 = 678.3
            TR3 = 3603
            
            gamma2 = (1 / T2 - 1 / T1) / (math.log(TR2) - math.log(TR1))
            gamma3 = (1 / T3 - 1 / T1) / (math.log(TR3) - math.log(TR1))
            thC = (gamma3 - gamma2) / (math.log(TR3) - math.log(TR2)) * (math.log(TR1) + math.log(TR2) + math.log(TR3))
            thB = gamma2 - thC * (math.log(TR1) * math.log(TR1) + math.log(TR1) * math.log(TR2) + math.log(TR2) * math.log(TR2))
            thA = 1 / T1 - (thB + math.log(TR1) * math.log(TR1) * thC) * math.log(TR1)
        
            thA = 0.001125308852122
            thB = 0.000234711863267
            thC = 0.000000085663516
            T_th = math.abs(1 / (thA + thB * math.log(resistance) + thC * math.log(resistance) * math.log(resistance) * math.log(resistance)) - 273.15)

            return T_th   
