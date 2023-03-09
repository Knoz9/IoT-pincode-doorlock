from lcd_api import LcdApi
from gpio_lcd import GpioLcd
from machine import Pin
from machine import PWM
from network import WLAN
from mqtt import MQTTClient_lib
import machine
import time
import os
import uhashlib
import keypad as k
import binascii
import network
import time
import utime
import pycom

def init():
    global wlan,lcd,pc,p2,tim,ch,beep,t,t2,gcount,count,pc2
    wlan = network.WLAN(mode=network.WLAN.STA)
    lcd = GpioLcd(rs_pin=Pin("P12"),enable_pin=Pin("P11"),d4_pin=Pin("P10"),d5_pin=Pin("P9"),d6_pin=Pin("P8"),d7_pin=Pin("P7"))
    pc = "Enter           Passcode:"
    pc2 = "Enter    OFFLINEPasscode:"
    lcd.putstr(pc2)
    p2 = Pin("P23")
    tim = PWM(0, frequency=0)
    ch = tim.channel(0, duty_cycle=0.5, pin=p2)
    beep = [1500,0] 
    t = utime.ticks_ms()
    t2 = utime.ticks_ms()
    count = 0
    gcount = 1
    with open ("cooldown.txt") as datafile: # Checks if there is any cooldown stored, and if there is, it will trigger it on startup!
        x = (datafile.read())
    datafile.close()
    if int(x) > 0:
        incorrect(int(x))
        count = int(x) + 3 # This restores count to its original (3 + 1 attempt for 60 seconds, where 3 is the attempts without cooldown)




def sub_cb(topic, msg):
    lcd.clear()
    lcd.putstr("Changing Password...")
    x = str(msg,"utf-8")
    if "m" in x:
        x = x[1:]
        encrypt(x, 1, "m") # encrypt is set to 1, so it WILL overwrite the old password in this case and encrypt it.
        time.sleep(0.5)
        client.publish(topic='kenozzz/feeds/ddd', msg="Changed Password!")
        lcd.clear()
        ent_pass()
    else:
        encrypt(x, 1, "g")
        time.sleep(0.5)
        client.publish(topic='kenozzz/feeds/ddd', msg="Changed Password!(g)")
        lcd.clear()
        ent_pass()

def ent_pass(): # Prints OFFLINE on screen if its in offline mode..
    if wlan.isconnected():
        lcd.putstr(pc)
    else:
        lcd.putstr(pc2)

def connect():
    global t,client
    pycom.heartbeat(False)
    pycom.rgbled(0x7f0000)
    time.sleep(1)
    wlan = WLAN(mode=WLAN.STA)
    lcd.clear()
    lcd.putstr("Connecting to   WiFi...") 
    try:                                      # This checks if wifi connection is possible, if not, it sets t variable to wait until next attempt (in order to not block the device from functioning offline.)
        wlan.connect("EAKER-guest", auth=(WLAN.WPA2, "skafiskafnjak"), timeout=0)
        for x in range(5): # My Own timeout, because the timeout above gets stuck in a loop sometimes.
            if wlan.isconnected():
                break
            else:
                time.sleep(1)
        client = MQTTClient_lib("1", "io.adafruit.com",user="kenozzz", password="aio_Tegc75Mo6o0AAdHRqNEfJB9gE2RP", port=1883)
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(topic='kenozzz/feeds/pass')
        pycom.heartbeat(True)
        lcd.clear()
        lcd.putstr("Connetced!")
        time.sleep(0.5)
        lcd.clear()
        ent_pass()

    except Exception:
        lcd.clear()
        lcd.putstr("Failed!")
        time.sleep(1)
        lcd.clear()
        ent_pass()
        t = utime.ticks_ms()

def get_stored(y):
    if y == "m":
        with open ("passcode.txt") as datafile:
            x = (datafile.read())
        datafile.close()
        return x
    else:
        with open ("gpasscode.txt") as datafile:
            x = (datafile.read())
        datafile.close()
        return x



def encrypt(code, x, y): # If x is set to 1, it will ALSO overwrite the stored passcode, if x is 0 it will simply just return the ecode. if y is set to m, its a master code change.
    global gcount
    codehash = uhashlib.sha256(code) # Hashes code in hexformat
    ecode = str(binascii.hexlify(codehash.digest()),"utf-8") # Digests the hash, and returns it reverting from hex
    if x == 1:
        if y == "m":
            with open("passcode.txt","w") as datafile:
                datafile.write(ecode)
            datafile.close()
        else:
            with open("gpasscode.txt","w") as datafile:
                datafile.write(ecode)
            datafile.close()
            gcount = 0
    else:
        return ecode


def beeping(t,s,t2):# Beeping with three variables. t = how many times to play, s = how fast, t2 = sleep time every loop
    for i in range(0,t):
        for i in beep:
            if i == 0:
                ch.duty_cycle(0)
                time.sleep(t2)
            else:
                tim = PWM(0, frequency=i)
                ch.duty_cycle(0.5)
            time.sleep(s)

def passcode(): # Matrix keypad nightmare : )
    global t2
    s = ""
    kcount = 0
    while True:
        if kcount < 4:  
            for row in range(4):
                for col in range(4):
                    key = k.scan(row, col)
                    if key == k.On:
                        lcd.putstr(k.keys[row][col])
                        time.sleep(0.5)
                        s = s + (k.keys[row][col])
                        kcount = kcount + 1
                if not wlan.isconnected(): # This is for timeouts, it waits 20 seconds before trying to reconnect again
                    if utime.ticks_ms() - t > 60000:
                        connect()
                if wlan.isconnected():
                    client.check_msg() # This is needed in order to see incoming callbacks
                    if utime.ticks_ms() - t2 > 240000:
                        client.publish(topic='kenozzz/feeds/ddd', msg="Still Connected!") # Ping to keep connection alive!
                        t2 = utime.ticks_ms()
                time.sleep(0.1)
        else:
            return s


def correct():
    global client,count
    lcd.clear()
    lcd.putstr("Correct!")
    beeping(2,0.05,0.05)
    time.sleep(5)
    lcd.clear()
    cooldown_write(0) # Only a correct input resets the cooldown. We want to implement it through mqtt, but that is a security issue if you could remove it remotely.
    ent_pass()
    count = 0
    if wlan.isconnected():
        client.publish(topic='kenozzz/feeds/ddd', msg="Sucessful Attempt")

def cooldown_write(cooldown): # This is used to store cooldown so that it can't be reset and bruteforced. Use cooldown_write(0) in REPL to bypass it.
    with open("cooldown.txt","w") as datafile:
        datafile.write(str(cooldown))
    datafile.close()


def incorrect(cooldown): # This is used to count the cooldown, and also to keep track of cooldown
    lcd.clear()
    lcd.putstr("Wrong!")
    beeping(1,1,0)
    if cooldown == 0:
        time.sleep(5)
    else:
        cooldown_write(cooldown) # This writes the cooldown to the flash
        cooldown = cooldown * 60
        if cooldown > 3600: # Lets not implement minutes on cooldown, so that the crackers will have a harder time knowing when next attempt is.: )
            cooldown = 3600
        for i in range(cooldown): # We dont have a client.check_msg() because we want a cooldown not be bypassable by any means (security)
            lcd.clear()
            disp = "Wrong! Try againin: " + str(cooldown-i) + " seconds"
            lcd.putstr(disp)
            time.sleep(1)
    lcd.clear()
    ent_pass()
    if wlan.isconnected():
        client.publish(topic='kenozzz/feeds/ddd', msg="Failed Attempt")


def idle():
    global gcount,count
    time.sleep(0.5)
    value = encrypt(passcode(), 0, 0) # This encrypt is set to 0, so it only encrypts the passcode input, and checks it with the stored one.
    if value == get_stored("m"):
        correct()
    elif value == get_stored("g"):
        if gcount < 1: # Here we can change the number of uses, we could implement a function to let the user choose, but if they want to reset uses they can just push the same password again.
            correct()
            print("g")
            gcount = gcount + 1
        else:
            lcd.clear()
            lcd.putstr("Error: Too Many Uses!") # We want the error message, so we need to overwrite it on 2nd attempt instead of overwriting as soon as its used. But gcount is set to 1 upon restart, so this isn't a security issue.
            beeping(1,1,0)
            encrypt("XXXX",1,"g") # Overwrites guest code with impossible combination. We could use randint, but this is safer since its impossible to input "x"
            time.sleep(5)
            lcd.clear()
            ent_pass()
    elif count < 3: # Three attempts before adding cooldowns
        incorrect(0)
        count = count + 1
    else:
        incorrect(count-2) # This is so that the cooldown is correctly processed (where number is one "cooldown period" which is 60 seconds)
        count = count + 1
        if wlan.isconnected():
            client.publish(topic='kenozzz/feeds/ddd', msg="BruteForce Alert! Cooldown Enabled!") # Cooldown cant be bypassed by resets


init()
connect()
while True:
    idle()
