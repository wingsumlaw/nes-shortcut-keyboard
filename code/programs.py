'''
NES Shortcut Keyboard
programs.py
Wing-Sum Law

In the dicts list below, please input relevant shortcut key sequences.
Make sure to use Adafruit's keycode library (https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html)

See the labeled image of the button layout for buttons
'''

from collections import OrderedDict
from adafruit_hid.keycode import Keycode 

''' ******** PROGRAM SHORTCUTS HERE ******** '''

dicts = [
    OrderedDict(
        d_pad_left=[],
        d_pad_down=[],
        bottom_left=[],
        bottom_right=[],
        start=[Keycode.COMMAND, Keycode.Y],                     # redo
        d_pad_up=[],
        d_pad_right=[],
        top_left=[],
        top_right=[],
        select=[Keycode.COMMAND, Keycode.Z],                    # undo
        encoder0_up=[Keycode.COMMAND, Keycode.KEYPAD_PLUS],     # zoom in
        encoder0_down=[Keycode.COMMAND, Keycode.KEYPAD_MINUS],  # zoom out
        encoder1_up=[Keycode.EQUALS],                           # rotate canvas right
        encoder1_down=[Keycode.MINUS],                          # rotate canvas left
        name="ClipStudio",
        light_color=(255,255,255)
    ),
    OrderedDict(
        d_pad_left=[],
        d_pad_down=[],
        bottom_left=[],
        bottom_right=[],
        start=[Keycode.COMMAND, Keycode.Y],                     # redo
        d_pad_up=[],
        d_pad_right=[],
        top_left=[],
        top_right=[],
        select=[Keycode.COMMAND, Keycode.Z],                    # undo
        encoder0_up=[Keycode.COMMAND, Keycode.KEYPAD_PLUS],     # zoom in
        encoder0_down=[Keycode.COMMAND, Keycode.KEYPAD_MINUS],  # zoom out
        encoder1_up=[Keycode.EQUALS],                           # rotate canvas right
        encoder1_down=[Keycode.MINUS],                          # rotate canvas left
        name="Powerpoint",
        light_color=(255,0,0)
    )   
]

num = len(dicts)