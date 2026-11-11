# seven-segment module Timer (countdown) mode

from math import ceil
from re import compile
from time import monotonic

from .display import clock_displays, set_colon, set_led, get_button_pressed

TIMER_PATTERN = compile(r"(\d{1,2}):([0-5]\d)")


def parse_timer(value):
    """Return the number of seconds in a 'MM:SS' string, or raise ValueError"""
    if value is None:
        raise ValueError("ERROR: 'timer' mode needs a start time: use -t MM:SS (e.g. -t 01:30)")
    m = TIMER_PATTERN.fullmatch(value)
    if m is None:
        raise ValueError(f"ERROR: Invalid timer argument '{value}'. Must be 'MM:SS'")
    seconds = int(m.group(1)) * 60 + int(m.group(2))
    if seconds == 0:
        raise ValueError("ERROR: Timer start must be greater than 00:00")
    return seconds


def run_timer(seconds):
    """Count down on the display, then blink the LED until the button is pressed"""
    start = monotonic()
    while True:
        elapsed = monotonic() - start
        remaining = ceil(seconds - elapsed)
        if remaining <= 0:
            break
        set_colon(int(elapsed * 2) % 2 == 0)        # colon blinks once a second
        clock_displays(f"{remaining // 60:02d}{remaining % 60:02d}")

    # Time is up: blink the LED until the button is pressed
    set_colon(True)
    alarm_start = monotonic()
    while not get_button_pressed():
        set_led(int((monotonic() - alarm_start) * 2) % 2 == 0)
        clock_displays("0000")
    set_led(False)
