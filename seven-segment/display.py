# seven-segment module support functions
# Author: Eddy Ferre - ferree@seattleu.edu

import gpiozero as GPIO
from time import sleep
from .constants import *

# Global Variables
outputs = {}
inputs = {}


def output(pin, state):
    global outputs
    if pin not in OUT_PINS:
        print(f'ERROR: Pin {pin} is not allocated')
        return
    if state == HIGH:
        outputs[pin].on()
    else:
        outputs[pin].off()


# noinspection PyUnusedLocal
def init_display(channels_set):
    global outputs
    global inputs
    for pin in OUT_PINS:
        outputs[pin] = GPIO.LED(pin)
    for pin in IN_PINS:
        inputs[pin] = GPIO.Button(pin, bounce_time=0.08)
    clear_displays()


def activate_displays(digits, decimal_point=None, set_colon=False, set_thousand=False):
    if decimal_point is None:
        decimal_point = [False] * 4
    for d in range(4):
        # Set the display pins
        output(DISP_OUT_L[d - 1], HIGH)
        output(DISP_OUT_L[d - 2], HIGH)
        output(DISP_OUT_L[d - 3], HIGH)
        output(DISP_OUT_L[d], LOW)

        # Set the colon and thousand
        output(COLON_OUT_H, d == 1 and set_colon)
        output(THOUSAND_OUT_H, d == 2 and set_thousand)

        # Set decimal point
        output(DP_OUT_H, decimal_point[d])

        # Set the 7-segment
        for seg_index in range(7):
            output(SEGMENT_OUT_H[seg_index], SEGS_FOR_CHAR[digits[d]][seg_index])

        sleep(0.005)


def clock_displays(digits, dp):

        for d in range(4):
        # Set the display pins
            output(DISP_OUT_L[d - 1], HIGH)
            output(DISP_OUT_L[d - 2], HIGH)
            output(DISP_OUT_L[d - 3], HIGH)
            output(DISP_OUT_L[d], LOW)

        # Set the 7-segment
            for seg_index in range(7):
                output(SEGMENT_OUT_H[seg_index], SEGS_FOR_CHAR[digits[d]][seg_index])
            if d == 2 and dp:
                output(DP_OUT_H, True)
            else:
                output(DP_OUT_H, False)

            sleep(0.005)


def clear_displays():
    for pin in ACTIVE_HIGH_PINS:
        output(pin, LOW)
    for pin in ACTIVE_LOW_PINS:
        output(pin, HIGH)


def set_colon(state):
    output(COLON_OUT_H, state)


def set_led(state):
    output(LED_OUT_H, state)


def get_button_pressed():
    global inputs
    return inputs[BUTTON_IN].is_pressed



def cleanup():
    global outputs
    global inputs
    if outputs == {} or inputs == {}:
        return
    sleep(0.5)
    for pin in OUT_PINS:
        output(pin, LOW)
        outputs[pin].close()
        del outputs[pin]
    for pin in IN_PINS:
        inputs[pin].close()
        del inputs[pin]
