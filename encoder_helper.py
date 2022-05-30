'''
NES Shortcut Keyboard
encoder_helper.py
Wing-Sum Law

Helper for checking encoder buttons and movement
Executes any corresponding shortcuts using keypad_helper
'''

import state_classes
import programs

STATE = state_classes.States()

def check_encoder_btns(btn_event, current_state, current_program):
    '''
    Checks for encoder button press events
    If encoder 0 is pressed, swaps current state
    Otherwise, executes associated shortcut
    '''

    # Default to no state change
    return_state = current_state

    # If event is a down press
    if btn_event.pressed:

        # If encoder 0 button has been pressed, switch states
        if btn_event.key_number == 0:
            if current_state == STATE.RUNNING_SHORTCUTS:
                return_state = STATE.CHOOSING_PROGRAM
            elif current_state == STATE.CHOOSING_PROGRAM:
                return_state = STATE.RUNNING_SHORTCUTS

        # Only check other encoder buttons if currently running shortcuts
        elif current_state == STATE.RUNNING_SHORTCUTS:
            print(list(programs.dicts[current_program].items())[btn_event.key_number + 15])

    return return_state


def run_encoder_changes(encoder_number, position, last_position, current_program):
    '''
    A program is active and shortcuts are running
    Determine position change and execute corresponding shortcut
    '''

    # Determine position change
    position_change = check_encoder_rotation(position, last_position)

    # Determine what function position change corresponds to
    if position_change < 0:
        print(list(programs.dicts[current_program].items())[encoder_number*2 + 11])
    elif position_change > 0:
        print(list(programs.dicts[current_program].items())[encoder_number*2 + 10])


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
