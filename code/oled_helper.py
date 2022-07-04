'''
NES Shortcut Keyboard
oled_helper.py
Wing-Sum Law

Helper for updating OLED display
Formats text, appends to display splash, returns splash
'''

from adafruit_display_text import label
import displayio
import terminalio
import programs

WIDTH = 128
HEIGHT = 64

def format_text(line, scale, text_content):
    '''
    Given text_content, format text such that it shows up...
    - on line given
    - centered
    - at scale given (scale must be an integer)
    '''

    formatted_text = label.Label(terminalio.FONT, text=text_content)

    # Place text centered
    formatted_text.x = int(WIDTH/2 - scale*formatted_text.bounding_box[2]/2)

    # Place text at correct height
    formatted_text.y = line * 10

    # Scale to desired size
    formatted_text.scale = scale

    return formatted_text


def display_current_program(current_program_name):
    '''
    Receives current program name and formats it for display
    '''

    # Create display splash
    splash = displayio.Group()

    # Format text to show Current Program: [Current Program Name]
    splash.append(format_text(2, 1, "Current Program:"))
    splash.append(format_text(4, 2, current_program_name))

    return splash
    

def display_choose_program(current_program, program_names):
    '''
    Displays all program names as a list
    Indicates currently selected program using >> <<
    '''

    # Create display splash
    splash = displayio.Group()
    splash.append(format_text(1, 1, "Choose Program:"))

    # For each program, display name
    for i, name in enumerate(program_names):

        # If program is currently selected, indicate with >> <<
        if i == current_program:
            splash.append(format_text(i+2, 1, ">>  " + name + "  <<"))
        else:
            splash.append(format_text(i+2, 1, name))

    return splash
