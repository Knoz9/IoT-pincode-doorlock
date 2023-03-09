from machine import Pin
keys = [["1", "2", "3", "A"], ["4", "5", "6", "B"], ["7", "8", "9", "C"], ["*", "0", "#", "D"]]
On = 1
Off = 0

# Row Pins
row_pin1 = Pin("P22", mode=Pin.OUT)
row_pin2 = Pin("P21", mode=Pin.OUT)
row_pin3 = Pin("P20", mode=Pin.OUT)
row_pin4 = Pin("P19", mode=Pin.OUT)
row_pins = [row_pin1, row_pin2, row_pin3, row_pin4]


# Column Pins
col_pin1 = Pin("P6", mode=Pin.IN, pull=Pin.PULL_DOWN)
col_pin2 = Pin("P3", mode=Pin.IN, pull=Pin.PULL_DOWN)
col_pin3 = Pin("P4", mode=Pin.IN, pull=Pin.PULL_DOWN)
col_pin4 = Pin("P5", mode=Pin.IN, pull=Pin.PULL_DOWN)
col_pins = [col_pin1, col_pin2, col_pin3, col_pin4]

def scan(row, col): # This scans for input, checks col pins value. It turns on the row, then checks for col value
                    # If both match, it means that we pinned down a keypress.
    row_pins[row].value(1)
    key = None
    if col_pins[col].value() == On:
        key = On
    if col_pins[col].value() == Off:
        key = Off
    row_pins[row].value(0)
    return key
