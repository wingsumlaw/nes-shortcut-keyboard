'''
NES Shortcut Keyboard
encoder_helper.py
Wing-Sum Law

Helper for checking encoder buttons and movement
Executes any corresponding shortcuts using keypad_helper
'''

import state_classes
import programs
import keypad_helper

STATE = state_classes.States()
ENCODER_MODE = state_classes.EncoderMode()


def run_encoder_changes(encoder_mode, position, last_position, current_program):
    '''
    A program is active and shortcuts are running
    Determine position change and execute corresponding shortcut
    '''

    # Determine position change
    position_change = check_encoder_rotation(position, last_position)

    # Determine which encoder commands to use
    if encoder_mode == ENCODER_MODE.MODE_1:
        adj = 0
    else:
        adj = 2

    # Determine what function position change corresponds to
    if position_change < 0:
        key_sequence = list(programs.dicts[current_program].items())[10 + adj]
        keypad_helper.execute_shortcut(key_sequence)
    elif position_change > 0:
        key_sequence = list(programs.dicts[current_program].items())[11 + adj]
        keypad_helper.execute_shortcut(key_sequence)


def change_program(position, last_position, current_program):
    '''
    No program is active and one must be chosen
    Determine position change and map to new program
    '''
    # Assume no change
    return_program = current_program

    # Determine position change
    position_change = check_encoder_rotation(position, last_position)

    # Determine which program position_change corresponds to
    return_program = (current_program + position_change) % programs.num

    return return_program


def check_encoder_rotation(position, last_position):
    '''
    Using last position and current position, determine how much position of encoder has changed
    '''

    # Default to no position change
    position_change = 0

    # Determine if position has a non-zero change
    if last_position is None:
        position_change = position - 0
    elif last_position != position:
        position_change = position - last_position

    return position_change
