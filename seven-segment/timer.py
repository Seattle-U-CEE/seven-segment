from threading import Timer, Thread
import math
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time
from .display import *

class ClockTimer(Thread):
    #Initialize all variables
    def __init__(self):
        super().__init__()
        self.led_blink = False
        self.blink_on = True
        self.led_on = True
        self.time = ""
        self.time_in_seconds = 0
        self.got_interrupted = False
        self.timer_finished = False
        self.timer_is_off = False
        
    def run(self):
        self.blink_colon()
        self.update_time()
        self.monitor_button()
        while not self.got_interrupted:
            clock_displays(self.time, False)
        clear_displays()
        # Continuously display current time
        
    def set_timer(self, t1): #assumes that t is a string in the format MSS.
        t = t1.strip()
        if len(t)<4:
            self.time = "0" + t
        else:
            self.time = t
        self.time_in_seconds = (int(self.time)//100 * 60) + int(self.time)%100 +1
    
    def blink_colon(self):
        if not self.got_interrupted and not self.timer_finished:
            self.blink_on = not self.blink_on
            set_colon(self.blink_on)
            Timer(0.5, self.blink_colon).start()
            
    def update_time(self):
        if not self.got_interrupted and not self.timer_finished:
            if self.time_in_seconds != 0:
                self.time_in_seconds -= 1
                self.time = self.timenorm(self.time_in_seconds)
                Timer(1.0, self.update_time).start()
            else:
                self.blink_led()
                self.timer_finished = True
                
    def blink_led(self):
        if not self.got_interrupted and not self.timer_is_off:
            set_led(self.led_on)
            self.led_on = not self.led_on
            Timer(0.5, self.blink_led).start()
    
    def monitor_button(self):
        if not self.got_interrupted and self.timer_finished:
            if get_button_pressed():
                print("button pressed")
                set_led(False)
                self.timer_is_off = True
        Timer(0.5, self.monitor_button).start()
    
    def timenorm(self, seconds):
        mm=str(seconds//60)
        ss=str(seconds%60)
        if len(mm) <2:
            mm = "0" + mm
        if len(ss) < 2:
            ss = "0" + ss
        return mm+ss
        
    def stop(self):
        self.got_interrupted = True
        clear_displays()

