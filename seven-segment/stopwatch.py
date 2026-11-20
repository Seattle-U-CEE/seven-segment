# seven-segment module Stopwatch mode
#
# Stopwatch is a Thread: run() moves through states A, B, C and D. Each button
# press-and-release moves to the next state:
#   A: display 000.0, LED off          (stopped)
#   B: count up (100 ms), LED blinks   (running)
#   C: display elapsed time, LED on    (stopped)
#   D: reset, display 000.0, LED off   (then back to A)

from threading import Thread
from time import monotonic

from .display import activate_displays, set_led, get_button_pressed

DECIMAL_POINT = [False, False, True, False]     # the '.' goes after the 3rd digit
MAX_TENTHS = 9999                               # display tops out at 999.9


class Stopwatch(Thread):
    def __init__(self):
        super().__init__()
        self.state = "A"                    # current state: A, B, C or D
        self.got_interrupted = False        # set to True by stop()

    # Overload Thread.run
    def run(self):
        start = 0.0             # when the stopwatch started counting
        elapsed = 0.0           # the time shown on the display
        led = False
        was_pressed = False

        while not self.got_interrupted:
            # A press followed by a release is what moves to the next state
            pressed = get_button_pressed()
            released = was_pressed and not pressed
            was_pressed = pressed

            if self.state == "A":
                # Display 000.0, LED off, stopwatch stopped
                elapsed, led = 0.0, False
                if released:
                    self.state = "B"
                    start = monotonic()
            elif self.state == "B":
                # Count up, LED blinks every 0.5 s
                elapsed = monotonic() - start
                led = int(elapsed * 2) % 2 == 0
                if released:
                    self.state = "C"
            elif self.state == "C":
                # Stopwatch stopped: keep showing the elapsed time, LED on
                led = True
                if released:
                    self.state = "D"
            else:
                # State D: reset the stopwatch, display 000.0, LED off, back to A
                elapsed, led = 0.0, False
                self.state = "A"

            set_led(led)
            tenths = min(int(elapsed * 10), MAX_TENTHS)
            activate_displays(f"{tenths:04d}", decimal_point=DECIMAL_POINT)

        set_led(False)

    # Ask the thread to stop
    def stop(self):
        self.got_interrupted = True
