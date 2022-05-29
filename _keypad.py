import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard

# Set up a keyboard device.
kbd = Keyboard(usb_hid.devices)

def keyMap(keynum, currentProgram):
    thisCommand = list(currentProgram.items())[keynum]

    # Press and release every key in shortcut sequence
    kbd.press(*thisCommand[1])
    kbd.release_all()
