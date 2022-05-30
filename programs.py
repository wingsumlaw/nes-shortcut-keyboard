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
        select=[Keycode.COMMAND, Keycode.Z],
        top_left="Top Left",
        top_right="Top Right",
        d_pad_up="d pad up",
        d_pad_right="d pad right",
        start=[Keycode.COMMAND, Keycode.S],
        bottom_left="Bottom Left",
        bottom_right="Bottom Right",
        d_pad_left="d pad left",
        d_pad_down="d pad down",
        encoder0_up="bigger brush",
        encoder0_down="smaller brush",
        encoder1_up="zoom in",
        encoder1_down="zoom out",
        encoder2_up="rotate right",
        encoder2_down="rotate left",
        encoder1_press="encoder 1 pressed",
        encoder2_press="encoder 2 pressed",
        name="program 1"
    ),
    OrderedDict(
        select="undo",
        top_left="Top Left",
        top_right="Top Right",
        d_pad_up="d pad up",
        d_pad_right="d pad right",
        start="save",
        bottom_left="Bottom Left",
        bottom_right="Bottom Right",
        d_pad_left="d pad left",
        d_pad_down="d pad down",
        encoder0_up="encoder 0 up",
        encoder0_down="encoder 0 down",
        encoder1_up="encoder 1 up",
        encoder1_down="encoder 1 down",
        encoder2_up="encoder 2 up",
        encoder2_down="encoder 2 down",
        encoder1_press="encoder 1 pressed",
        encoder2_press="encoder 2 pressed",
        name="program 2"
    )   
]

num = len(dicts)