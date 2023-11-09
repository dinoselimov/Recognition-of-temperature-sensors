----ANG

This program implements algorithm to recognize one of four temperature sensors: PT100, PT1000 and thermistors 5k and 10k. Circuit is on circuit_image.png.
Code doesn't have to be run by PlatfromIO, it could be run with Arduino IDE. 

System consists of these components:
 
- main.cpp: The C++ file which runs code on ESP32 microcontroller, it handles communication with the broker, measuring sensor's resistances and sending 
the results via MQTT to the user.
- gui.py: main python file, which manages graphical interface, allowing users to interact with the system, and starts correctly receiving resistances, when communication is settled. Inside it we are calling other python functions like recognition_algorithm and temperature_reading
- recognition_algorithm: Here are training data and least squares regression algorithm which recognizes which sensor is connected.
- temperature_reading: This function runs after recognition of sensor, performs accurate temperature readings based on the recognized sensor
- run.py: file which runs whole program i.e. main.cpp and gui.py simultaneously

----SLO

Ta program implementira algoritem za prepoznavo enega od štirih temperaturnih senzorjev: PT100, PT1000 in termistorjev 5k in 10k. Shema vezja je na sliki circuit_image.png. 
Koda se ne mora izvajati prek PlatformIO, ampak jo je mogoče zagnati tudi z Arduino IDE.

Sistem vključuje naslednje komponente:
	
- main.cpp: C++ datoteka, ki se izvaja na mikrokrmilniku ESP32, vodi komunikacijo z brokerjem, meri upornosti senzorjev in rezultate pošilja uporabniku prek MQTT.
- gui.py: Glavna python datoteka, ki upravlja grafični vmesnik, omogoča uporabnikom interakcijo s sistemom in pravilno prejemanje upornosti, 
ko je vzpostavljena komunikacija. V tej datoteki kličemo druge python funkcije, kot sta recognition_algorithm in temperature_reading.
- recognition_algorithm: Tu se nahajajo podatki za učenje in algoritem najmanjših kvadratov, ki prepoznava povezan senzor.
- temperature_reading: Ta funkcija se izvaja po prepoznavi senzorja in izvaja branje temperature glede na ugotovljeni senzor.
- run.py: Datoteka, ki zagnane celoten program, torej main.cpp in gui.py hkrati.
