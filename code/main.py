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
import digitalio
import displayio
import adafruit_displayio_ssd1306

# Imports of own modules
import programs
import keypad_helper
import encoder_helper
import oled_helper
import state_classes

# Program names
program_names = [p["name"] for p in programs.dicts]

''' ******** BOARD IO ******** '''

# LEDs under keys, IN goes to D4 on Feather, start LEDs in default color
lights = neopixel.NeoPixel(board.D4, 10, brightness = 0.1)
lights.fill(programs.dicts[0]["light_color"])

# The keypad
keys = keypad.KeyMatrix(
    row_pins = (board.D12, board.D13),
    column_pins = (board.D5, board.D6, board.D9, board.D10, board.D11),
    columns_to_anodes=False
)

# The buttons on the rotary knobs
encoder_btn = keypad.Keys((board.A1,), value_when_pressed=False, pull=True)

# The rotary knobs
encoder = rotaryio.IncrementalEncoder(board.A2, board.A3)

last_encoder_pos = None

# The slide switch
switch = digitalio.DigitalInOut(board.A0)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

''' ******** OLED SCREEN ******** '''

# I2C for OLED
displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3d)

WIDTH = 128
HEIGHT = 64
BORDER = 5

display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT)

# Initial program display
display.show(oled_helper.display_current_program(program_names[0]))


''' ******** STATES ******** '''

# State describes whether currently in a program running shortcuts or choosing a program
STATE = state_classes.States()
ENCODER_MODE = state_classes.EncoderMode()
current_state = STATE.RUNNING_SHORTCUTS
current_encoder_mode = ENCODER_MODE.MODE_1

# Default to first program in list of programs
current_program = 0


''' ******** STATE FUNCTIONS ******** '''

def run_shortcuts(current_state, current_program, current_encoder_mode):
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
    return_encoder_mode = current_encoder_mode

    # Use global var for last encoder position
    global last_encoder_pos

    # Check for keypad, encoder, and switch for events
    key_event = keys.events.get()
    btn_event = encoder_btn.events.get()

    # Check if selecting or running
    if switch.value:
        return_state = STATE.CHOOSING_PROGRAM
    else:
        return_state = STATE.RUNNING_SHORTCUTS
        
    # Switch encoder mode if button is pressed
    if btn_event:
        if btn_event.pressed:
            return_encoder_mode = abs(current_encoder_mode - 1)
    
    # Check if keypad has been pressed
    if key_event:
        keypad_helper.press_keys(key_event, current_program)

    # Check if  encoder has moved
    position = encoder.position
    encoder_helper.run_encoder_changes(current_encoder_mode, position, last_encoder_pos, current_program)
    last_encoder_pos = position

    return return_state, return_program, return_encoder_mode


def choose_program(current_state, current_program, current_encoder_mode):
    '''
    No program is active and one must be chosen
    Check to see if encoder 0 has moved and determine which program corresponds to that movement
    Then check to see if encoder 0 has been pressed, indicating return to running shortcuts
    '''

    # Assume no state change
    return_state = current_state
    return_program = current_program
    return_encoder_mode = current_encoder_mode

    # Use global var for last encoder position
    global last_encoder_pos

    # Display program selection screen
    display.show(oled_helper.display_choose_program(return_program, program_names))

    # If encoder has moved, change to correct program
    position = encoder.position
    return_program = encoder_helper.change_program(position, last_encoder_pos, current_program)
    last_encoder_pos = position
    
    # Switch lights
    lights.fill(programs.dicts[return_program]["light_color"])

    # Check to see if program is locked in
    if not switch.value:
        return_state = STATE.RUNNING_SHORTCUTS
        display.show(oled_helper.display_current_program(program_names[return_program]))

    return return_state, return_program, return_encoder_mode


STATE_FUNCTIONS = {
    0: run_shortcuts,
    1: choose_program
}


# MAIN LOOP
while True:
    # Run appropriate state function
    current_state, current_program, current_encoder_mode = STATE_FUNCTIONS[current_state](current_state, current_program, current_encoder_mode)
