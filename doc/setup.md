Software:
You will need to change wifi ssid and password, this can be done in main.py where this information is input. 

If you use mqtt, you will also need to change the subscribe, topic and mqtt server to the one you use. 
If you use HTTP, (input info here nour : ) )

To change the master password on the pycom, input a password in SHA512 format into password.txt, then save the file and flash it to the pycom. You can also change the password using MQTT. To do this, input mxxxx where the x is the numbers you want to use. for example, for combination 1234, you would input m1234. If you want to change the "guest passcode" just input the passcode you want to use without the m in the beginning. You can also change the gpasscode.txt to change the guest passcode.

To setup the mqtt server, please use adafruit and create a feed named "pass" and push messages from that feed. You would need to change the passwords in the main.py for mqtt to work properly

Also, make a feed named "ddd" where all messages are sent from the pycom.

So, pass is for SENDING passwords to keylock, ddd is to RECIEVE messages from keypad.
