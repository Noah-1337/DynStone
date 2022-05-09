# DynStone
DynStone is a project created around the idea of dynamic Eddystone BLE Beacons

This project was developed during an internship at BBR Verkehrstechnik GmbH. The goal was the create a system, in which we can use the functionality of originally static Eddystone Beacons for dynamic transmitting of information in the case of railway systems. The hardware used for the beacons in this project is the affordable ESP32.  

Provided are multiple files. Two of those are .ino files which can be directly uploaded to an ESP32 and one python script (or the compiled .exe) that is used for communicating to the ESP32 via the serial port in an easy to understand GUI (partly written in german).

The image below shows my setup with two ESP32. In this case i marked the receiving end with [E] and the sending end with [S].
![IMG_9056](https://user-images.githubusercontent.com/97415279/167385777-ca7d9648-0d2d-475d-bc3a-cab13ee58706.jpg)

Once both ESP32 were configured with the provided .ino files you can start communicating with them via the python GUI.
The first window will ask you to choose between sending (Senden) and receiving (Empfangen) information.

![unknownchoose](https://user-images.githubusercontent.com/97415279/167387829-ada9340b-13f7-4980-809f-1886ee295b83.png)

When picking the first one you will be prompted with a new window, which let's you pick the relevant port for the ESP32 as well as define the information that should be send over. This application is written for a very specific function, which is why you are only allowed to send specific values in a specific range. 

Zielgeschwindigkeit:  (Int) from 0 to 120

Zielentfernung:       (Int) from 0 to 1000

GKS(Signal)Nummer:    (Int) from 0 to 1023

![unknown](https://user-images.githubusercontent.com/97415279/167387963-275c86b9-d724-4136-a670-9e60f4c5d334.png)

After sending the desired information we can create a second instance of the program or simple relaunch it but we will choose (Empfangen) this time. This prompts us with this window which simply requires a port to be selected and with the press of a button and if everything worked out you should receive the information you send before exactly as you send it in the three labels of the window.

![unknownr](https://user-images.githubusercontent.com/97415279/167388670-7036ee44-a66d-4560-a0cc-b3c3b79df099.png)

Now, this code is very simple but quite restrictive. If you plan on changing it i would advice to have a good look into the .ino files in which you will be able to see that this program has a maximum transfer limit of 17 bytes. The content of those bytes can be chosen as you wish and will be stored in a simple char array until the ESP32 reboots or gets new information.
