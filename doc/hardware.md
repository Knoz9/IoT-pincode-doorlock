# Hardware:
## Components list
|Component  |
|:---------------|
|Pycom Lopy 4|
|Pycom expansionboard 3.1|
|Breadboard|
|4x4 matrix membrane keypad|
|Display LCD 1602A|
|Buzzer|
|1kΩ resistor|
|200Ω resistor|
|331x241x104 mm box|
|Double-sided Velcro strap|
|Deltaco Powerbank|

![Circuit](/img/Skärmbild__309_.png "Circuit")


# Keypad: 
Hook up pin p22-p19 to the input of the keypad. These pins are not the same on all keypads, but if it does not 
work one way, it will work the other way around (pins to the left are always either output or input, and should be in the same order also.) Then, hook up pin p2-p5 to the output of the keypad. These pins are set to pull down internally, so no resistance is needed. No + or - connections are needed for the keypad

# LCD: 
Hook up rs_pin to P12, e_pin to p11, d4-d7(acending order) to p10-p7(decending order)
also, we will use the VIN port for the 5v needed to power it. The documentation to plug in the lcd to + and - is in IMG(this in img is if you want to power it all on a breadboard). Also, depending on your display (even if its a 1602A) you may need a resistance to the backlight. We used 1k ohm, but not all displays need this. Also, if you have an lcd with a backpack (I2C) you will need to use different libraries for the lcd. What we used is the lcd in 4bit mode.

# Buzzer: 
Hook up to p23, then a resistance in series with the buzzer, then to GND(either on the breadboard, or on the pycom)

Ideally, have it all on a breadboard, but this is not necessary (depending if you want to power it externally or from the pycom itself.)
#  
<img src="/img/271528041_3225245217705893_4015178971633209379_n.jpg" width="900"> <br>
