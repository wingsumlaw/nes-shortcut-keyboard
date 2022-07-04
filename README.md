# Shortcut keyboard in an NES-style casing

While I put all this hardware into an NES-inspired case, this will work in any case with the screen, rotary encoder, and 10 keys.

## Setup

Use the programs.py document to customize the shortcut keyboard. For each program you'd like to have a custom set of shortcuts for, add an OrderedDict to the dicts list. Use the [Adafruit keycode library](https://docs.circuitpython.org/projects/hid/en/latest/_modules/adafruit_hid/keycode.html) to determine which codes to use.

```py
dicts = [
    OrderedDict(
        d_pad_left=[Keycode.COMMAND, Keycode.D],                # deselect
        d_pad_down=[Keycode.ALT, Keycode.LEFT_BRACKET],         # down layer
        bottom_left=[Keycode.COMMAND, Keycode.S],               # save
        bottom_right=[Keycode.COMMAND, Keycode.V],              # paste
        start=[Keycode.COMMAND, Keycode.Y],                     # redo
        d_pad_up=[Keycode.ALT, Keycode.RIGHT_BRACKET],          # up layer                  
        d_pad_right=[Keycode.COMMAND, Keycode.T],               # transform
        top_left=[Keycode.COMMAND, Keycode.C],                  # copy
        top_right=[Keycode.COMMAND, Keycode.X],                 # cut
        select=[Keycode.COMMAND, Keycode.Z],                    # undo
        encoder0_up=[Keycode.COMMAND, Keycode.KEYPAD_PLUS],     # zoom in
        encoder0_down=[Keycode.COMMAND, Keycode.KEYPAD_MINUS],  # zoom out
        encoder1_up=[Keycode.EQUALS],                           # rotate canvas right
        encoder1_down=[Keycode.MINUS],                          # rotate canvas left
        name="ClipStudio",                                      # program name
        light_color=(255,255,255)                               # light color
    )
]
```

While this software could potentially manage a great number of programs, keep in mind that the OLED screen in its current state will only show 4 programs.

## Links

See more info on the construction and design of the NES Shortcut Keyboard can be found at...

* [My Website](https://www.wingsumlaw.com)
* [Hackaday Post](https://hackaday.io/project/186123-nes-shortcut-keyboard)
