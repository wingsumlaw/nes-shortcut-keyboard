'''
NES Shortcut Keyboard
keypad_helper.py
Wing-Sum Law

Helper for executing actual shortcut sequences
'''

import usb_hid
from adafruit_hid.keyboard import Keyboard

import programs

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

def press_keys(key_event, current_program):
    '''
    Takes pressed key from keypad
    Executes corresponding shortcut key sequence
    '''
    
    # If event is key press, then press all keys
    if key_event.pressed:
        key_sequence = list(programs.dicts[current_program].items())[key_event.key_number]
        execute_shortcut(key_sequence)
        

def execute_shortcut(key_sequence):
    '''
    Execute shortcut key sequence
    '''
    
    kbd.press(*key_sequence[1])
    kbd.release_all()
