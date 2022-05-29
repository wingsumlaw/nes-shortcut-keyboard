'''
NES-MacroPad
Wing-Sum Law

Resources:
- Please see Adafruit's various guides to CircuitPython (https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/overview)
- Check the libraries (https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)

Usage:
- 
'''

''' ******** PROGRAM SHORTCUTS HERE ******** '''

from collections import OrderedDict
from adafruit_hid.keycode import Keycode 

programs = [
    OrderedDict(
        select=[Keycode.COMMAND, Keycode.Z],
        topLeft="Top Left",
        topRight="Top Right",
        dPadUp="d pad up",
        dPadRight="d pad right",
        start=[Keycode.COMMAND, Keycode.S],
        bottomLeft="Bottom Left",
        bottomRight="Bottom Right",
        dPadLeft="d pad left",
        dPadDown="d pad down",
        encoder0up="bigger brush",
        encoder0down="smaller brush",
        encoder1up="zoom in",
        encoder1down="zoom out",
        encoder2up="rotate right",
        encoder2down="rotate left",
        encoder1press="encoder 1 pressed",
        encoder2press="encoder 2 pressed",
        name="program 1"
    ),
    OrderedDict(
        select="undo",
        topLeft="Top Left",
        topRight="Top Right",
        dPadUp="d pad up",
        dPadRight="d pad right",
        start="save",
        bottomLeft="Bottom Left",
        bottomRight="Bottom Right",
        dPadLeft="d pad left",
        dPadDown="d pad down",
        encoder0up="encoder 0 up",
        encoder0down="encoder 0 down",
        encoder1up="encoder 1 up",
        encoder1down="encoder 1 down",
        encoder2up="encoder 2 up",
        encoder2down="encoder 2 down",
        encoder1press="encoder 1 pressed",
        encoder2press="encoder 2 pressed",
        name="program 2"
    )   
]

''' ******** SOFTWARE ******** '''

# Imports from Adafruit
import board
import keypad
import neopixel
import rotaryio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306

# Imports of own modules
import _keypad
import _encoders

COLS = 5
ROWS = 2

# LEDs under keys, IN goes to D4 on Feather
lights = neopixel.NeoPixel(board.D4, 10, brightness = 0.5)

# The keypad
keys = keypad.KeyMatrix(
    row_pins = (board.D12, board.D13),
    column_pins = (board.D5, board.D6, board.D9, board.D10, board.D11),
    columns_to_anodes=False
)

# The buttons on the rotary knobs
btns = keypad.Keys((board.A0, board.A1, board.D24), value_when_pressed=False, pull=True)

# The rotary knobs
encoders = [rotaryio.IncrementalEncoder(board.A2, board.A3), rotaryio.IncrementalEncoder(board.MOSI, board.MISO), rotaryio.IncrementalEncoder(board.D0, board.D1)]
lastPosition = [None, None, None]

# I2C for OLED
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

splash = displayio.Group()
display.show(splash)

# STATES
numPrograms = len(programs)
currentProgram = 0

# State 0 = running, State 1 = choosing
RunningShortcuts = 0
ChoosingProgram = 1

# State functions
def RunShortcuts():
    # Assume no state change
    returnState = currentState

    # Check for encoder button or keypad presses
    btn_event = btns.events.get()
    key_event = keys.events.get()

    if btn_event:
        if btn_event.pressed:
            if btn_event.key_number == 0:
                returnState = ChoosingProgram
            else:
                _encoders.encoderBtnMap(btn_event.key_number, programs[currentProgram])
    
    # Check if keypad has been pressed
    if key_event:
        if key_event.pressed:
            _keypad.keyMap(key_event.key_number, programs[currentProgram])

    # Check if encoder has moved
    for i, encoder in enumerate(encoders):

        position = encoder.position

        if lastPosition[i] is None or position != lastPosition[i]:
            if lastPosition[i] is None:
                posChange = position - 0
            else:
                posChange = position - lastPosition[i]
            lastPosition[i] = position
            _encoders.encoderTurnMap(i, posChange, programs[currentProgram])

    return returnState

def ChooseProgram():
    # Assume no state change
    returnState = currentState

    # Relevant global variables
    global currentProgram

    # Check for encoder button events
    btn_event = btns.events.get()

    # Default to no position change
    posChange = 0

    # If encoder has moved, change to correct program
    position = encoders[0].position
    if lastPosition[0] is None or position != lastPosition[0]:
        if lastPosition[0] is None:
            posChange = position - 0
        else:
            posChange = position - lastPosition[0]
        lastPosition[0] = position

        currentProgram = (currentProgram + posChange) % numPrograms
        print(currentProgram)

    # Check to see if program is locked in
    if btn_event:
        if btn_event.pressed:
            if btn_event.key_number == 0:
                returnState = RunningShortcuts

    return returnState

stateFuncs = {
    0: RunShortcuts,
    1: ChooseProgram
}

currentState = RunningShortcuts

# MAIN LOOP
while True:

    # Run appropriate state function
    currentState = stateFuncs[currentState]()
