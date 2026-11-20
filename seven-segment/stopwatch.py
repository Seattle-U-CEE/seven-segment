# seven-segment module Stopwatch mode

from time import monotonic

from .display import activate_displays, set_led, get_button_pressed

DECIMAL_POINT = [False, False, True, False]     # the '.' goes after the 3rd digit


def run_stopwatch():
    """Each button press-and-release moves: idle -> running -> stopped -> idle"""
    state = "idle"
    start = 0.0         # when it started running
    frozen = 0.0        # the time shown while stopped
    was_pressed = False

    while True:
        # A press followed by a release moves on to the next state
        pressed = get_button_pressed()
        if was_pressed and not pressed:
            if state == "idle":
                state, start = "running", monotonic()
            elif state == "running":
                state, frozen = "stopped", monotonic() - start
            else:
                state = "idle"
        was_pressed = pressed

        if state == "idle":
            elapsed, led = 0, False                  # 000.0, LED off
        elif state == "running":
            elapsed = monotonic() - start
            led = int(elapsed * 2) % 2 == 0          # LED blinks
        else:
            elapsed, led = frozen, True              # time frozen, LED on

        set_led(led)
        tenths = min(int(elapsed * 10), 9999)        # display tops out at 999.9
        activate_displays(f"{tenths:04d}", decimal_point=DECIMAL_POINT)
