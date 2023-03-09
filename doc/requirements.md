Digital Encrypted Keypad lock (wifi)
Features:
• Keypad which takes input from user, then determines if it should unlock or not (and showing that on the lcd)

• Password.txt file should be encrypted with SHA512, one way encryption. Password is NEVER stored on the device in plain text.

• You should be able to change the password with a mqtt app for phones

• You have a "Master key" which always unlocks the door (can be changed with the app)

• You also have a "Guest key" which upon activation (through app) sets a different code that a guest can
use to unlock the door (onetime use only!) both master and guest codes should work in this state.

• All actions (incorrect inputs, correct inputs) will be logged and published to the mqtt server

• Adafruit will be our mqtt server.

• We wont implement the actual lock (will be hard to do) but it will show correct or wrong and 
beep with a buzzer if you input the correct combination.

• If the digital keypad loses wifi, it will be in offline mode. It will try to reconnect every 20 minutes or so.

• When it is doing a reconnect, it will show up on the LCD. (it wont be operatable for 5 seconds until wifi times out or    
reconnects)

• When you enter a code, it will be encrypted and compared to the stored password. 

• It will of course remember the password even after a reboot.

• It can't be brute-forced (due to a 6 second delay with each attempt.) At this rate, it would take approx 17 hours to bruteforce. We will add a 60 second delay after 5 failed attempts (making it approx 166 hours to bruteforce.) Also, it should store cooldowns in a file so that it can't be reset and then bruteforced 

## Server Requirments:
* .NET Core SDK v6.0
* Cloud Server or Computer on the same network of the pycom.
* Compiled source code of the server.
* If the Web-app is hosted in the cloud it need a SSL Certifect.