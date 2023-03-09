from lcd_api import LcdApi
from gpio_lcd import GpioLcd
from machine import Pin
from machine import PWM
from network import WLAN
import time
import keypad as k
import network
import time
import utime
import pycom
import lib.server as server


def init():
    global wlan,lcd,pc,p2,tim,ch,beep,t,t2,gcount,count,pc2,apikey
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
    with open ("apikey.txt") as datafile: # Reads the apikey from the file
        j = (datafile.read())
    datafile.close()
    if j is not None:
        apikey = j
    with open ("cooldown.txt") as datafile: # Checks if there is any cooldown stored, and if there is, it will trigger it on startup!
        x = (datafile.read())
    datafile.close()
    if int(x) > 0:
        incorrect(int(x))
        count = int(x) + 3 # This restores count to its original (3 + 1 attempt for 60 seconds, where 3 is the attempts without cooldown)


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
        wlan.connect("Ajfån 11 Pro", auth=(WLAN.WPA2, "12345678"), timeout=0)
        for x in range(5): # My Own timeout, because the timeout above gets stuck in a loop sometimes.
            if wlan.isconnected():
                break
            time.sleep(1)
        server.check(apikey, "1111") # This is NEEDED to get an exception..
        lcd.clear()
        lcd.putstr("Connected!")
        time.sleep(1)
        lcd.clear()
        ent_pass()
        pycom.heartbeat(True)
    except Exception:
        lcd.clear()
        lcd.putstr("Failed!")
        time.sleep(1)
        lcd.clear()
        ent_pass()
        t = utime.ticks_ms()

def get_stored():
    with open ("passcode.txt") as datafile:
        x = (datafile.read())
    datafile.close()
    return x



def save(pin): # Save cached pin

    with open("passcode.txt","w") as datafile:
        datafile.write(pin)
    datafile.close()


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
                    if utime.ticks_ms() - t2 > 240000:
                        server.heartbeat(apikey) # Ping to keep connection alive!
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


def idle():
    global gcount,count
    time.sleep(0.5)
    value = passcode() # Get the input code/pin
    response = None
    if wlan.isconnected():
        response = server.check(apikey, value) # send request to the server
    if response is None: # Server or wifi is down!
        stored = get_stored()
        authorized = stored == value # if the stored code == written value then authorize
    else: # else if we got the code/pin from server
        authorized = response["authorized"]
    if authorized:
        currentpin = response["currentPin"]  # get the current pin from the request and save it
        save(currentpin)
        correct()
    elif count < 3: # Three attempts before adding cooldowns
        if response is not None: # save the current pin
            currentpin = response["currentPin"] # get the current pin from the request and save it
            save(currentpin)
        incorrect(0)
        count = count + 1
    else:
        incorrect(count-2) # This is so that the cooldown is correctly processed (where number is one "cooldown period" which is 60 seconds)
        count = count + 1


init()
connect()
while True:
    idle()
