# seven-segment module Timer (countdown) mode
#
# CountdownTimer is a Thread: run() counts down and shows MM:SS with a blinking
# colon, then blinks the LED at 00:00 until the button is pressed.

from re import compile
from threading import Thread
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


class CountdownTimer(Thread):
    def __init__(self, total_seconds):
        super().__init__()
        self.total = total_seconds          # seconds to count down from
        self.got_interrupted = False        # set to True by stop()

    # Overload Thread.run
    def run(self):
        remaining = self.total
        start = monotonic()
        next_tick = start + 1               # periodic event: every 1 second
        set_led(False)

        # Count down, showing MM:SS (the colon blinks every 0.5 s)
        while remaining > 0:
            if self.got_interrupted:
                return
            now = monotonic()
            if now >= next_tick:            # one second has passed
                remaining -= 1              # decrease by 1 s
                next_tick += 1
            set_colon(int((now - start) * 2) % 2 == 0)
            clock_displays(f"{remaining // 60:02d}{remaining % 60:02d}")

        # Time is up: show 00:00 and blink the LED until the button is pressed
        set_colon(True)
        alarm_start = monotonic()
        while not get_button_pressed() and not self.got_interrupted:
            set_led(int((monotonic() - alarm_start) * 2) % 2 == 0)
            clock_displays("0000")
        set_led(False)

    # Ask the thread to stop
    def stop(self):
        self.got_interrupted = True
