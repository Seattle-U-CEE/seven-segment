from threading import Timer, Thread
import math
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time
from .display import *
from .constants import *

class Stopwatch(Thread):
    #Initialize all variables
    def __init__(self):
        super().__init__()
        self.led_blink = False
        self.blink_on = True
        self.led_on = True
        self.time = ""
        self.time_in_seconds = 0.0
        self.got_interrupted = False
        self.timer_is_off = False
        self.stopwatch_on = False
        self.reset_pause = False
        
    def run(self):
        self.update_time()
        self.blink_led()
        inputs[BUTTON_IN].when_released = self.monitor_button
        while not self.got_interrupted:
            clock_displays(self.timenorm(self.time_in_seconds), True)
        clear_displays()
    
    
    def update_time(self):
        if not self.got_interrupted and self.stopwatch_on and not self.reset_pause:
            self.time_in_seconds += .1
        Timer(0.1, self.update_time).start()
            
    def timenorm(self, seconds):
        t = str(round(seconds, 1)).strip().replace(".", "")
        
        if len(t)<4:
            for i in range(4-len(t)):
                t = "0" + t
        print(t)
        return t
                
    def blink_led(self):
        if not self.got_interrupted and not self.timer_is_off and self.stopwatch_on:
            set_led(self.led_on)
            self.led_on = not self.led_on
        Timer(0.5, self.blink_led).start()
    
    def monitor_button(self):
        self.reset_pause = False
        print("released")
        self.stopwatch_on = not self.stopwatch_on
        if not self.stopwatch_on:
            set_led(True)
        if self.stopwatch_on and (self.time_in_seconds > 0.0):
            self.stopwatch_on = False
            self.reset_pause = True
            self.time_in_seconds = 0.0
            set_led(False)
        
    def stop(self):
        self.got_interrupted = True
        clear_displays()

