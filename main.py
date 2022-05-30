'''
NES Shortcut Keyboard
main.py
Wing-Sum Law

Resources:
- Please see Adafruit's various guides to CircuitPython (https://learn.adafruit.com/intro-to-rp2040-pio-with-circuitpython/overview)
- Check the libraries (https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases)

Usage:
- Update programs & associated shortucts in the programs.py file
'''

''' ******** IMPORTS ******** '''

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
import programs
import keypad_helper
import encoder_helper
import state_classes


''' ******** BOARD IO ******** '''

# LEDs under keys, IN goes to D4 on Feather
# lights = neopixel.NeoPixel(board.D4, 10, brightness = 0.5)

# The keypad
keys = keypad.KeyMatrix(
    row_pins = (board.D12, board.D13),
    column_pins = (board.D5, board.D6, board.D9, board.D10, board.D11),
    columns_to_anodes=False
)

# The buttons on the rotary knobs
btns = keypad.Keys((board.A0, board.A1, board.D24), value_when_pressed=False, pull=True)

# The rotary knobs
encoder_inputs = [rotaryio.IncrementalEncoder(board.A2, board.A3),
                  rotaryio.IncrementalEncoder(board.MOSI, board.MISO),
                  rotaryio.IncrementalEncoder(board.D0, board.D1)
]

last_encoder_pos = [None, None, None]

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


''' ******** STATES ******** '''

# State describes whether currently in a program running shortcuts or choosing a program
STATE = state_classes.States()
current_state = STATE.RUNNING_SHORTCUTS

# Default to first program in list of programs
current_program = 0


''' ******** STATE FUNCTIONS ******** '''

def run_shortcuts():
    '''
    A program is active and shortcuts are running
    Check for button and key events
    First resolve encoder button presses -- if encoder 0 is pressed the return state will be different
    Then check for keypad events and execute any associated shortcuts
    Then check for encoder movement and execute any associated shortcuts
    '''

    # Assume no state change
    return_state = current_state
    return_program = current_program

    # Check for encoder button or keypad presses
    btn_event = btns.events.get()
    key_event = keys.events.get()

    # If an encoder has been pressed, determine which one
    # If that encoder was encoder 0, switch states
    if btn_event:
        return_state = encoder_helper.check_encoder_btns(btn_event, current_state, current_program)
    
    # Check if keypad has been pressed
    if key_event:
        keypad_helper.press_keys(key_event, current_program)

    # Check if each encoder has moved
    for i, encoder in enumerate(encoder_inputs):
        position = encoder.position
        encoder_helper.run_encoder_changes(i, position, last_encoder_pos[i], current_program)
        last_encoder_pos[i] = position

    return return_state, return_program


def choose_program():
    '''
    No program is active and one must be chosen
    Check to see if encoder 0 has moved and determine which program corresponds to that movement
    Then check to see if encoder 0 has been pressed, indicating return to running shortcuts
    '''

    # Assume no state change
    return_state = current_state
    return_program = current_program

    # If encoder has moved, change to correct program
    position = encoder_inputs[0].position
    return_program = encoder_helper.change_program(position, last_encoder_pos[0], current_program)
    last_encoder_pos[0] = position
    print(return_program)

    # Check to see if program is locked in
    btn_event = btns.events.get()
    if btn_event:
        return_state = encoder_helper.check_encoder_btns(btn_event, current_state, current_program)

    return return_state, return_program


STATE_FUNCTIONS = {
    0: run_shortcuts,
    1: choose_program
}


# MAIN LOOP
while True:
    # Run appropriate state function
    current_state, current_program = STATE_FUNCTIONS[current_state]()
