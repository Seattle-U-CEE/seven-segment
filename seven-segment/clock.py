# seven-segment module Clock class file
# Author: Eddy Ferre - ferree@seattleu.edu

from threading import Timer, Thread
from datetime import datetime

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

from .display import *


class Clock(Thread):
    # Initialize all variables
    def __init__(self):
        super().__init__()
        self.blink_on = True
        self.led_on = True
        self.got_interrupted = False
        self.alarm_is_off = True
        self.alarm_locked = False
        self.now = ""
        self.alarm = ""
        self.music_file = None

    # Overload Thread.run
    def run(self):
        self.blink_colon()     # Start blink_colon periodic event
        self.get_time()        # Start time capture periodic event
        self.monitor_button()  # Monitor the push button
        while not self.got_interrupted:
            clock_displays(self.now, False)   # Continuously display current time
        clear_displays()       # Turn off all LEDs

    # Event function to toggle the colon LED, blink period of 1 second
    def blink_colon(self):
        if not self.got_interrupted:
            self.blink_on = not self.blink_on
            set_colon(self.blink_on)
            Timer(0.5, self.blink_colon).start()

    # Event function to capture current time and check alarm status, every 500ms
    def get_time(self):
        if not self.got_interrupted:
            tmp = f"{datetime.now():%H%M}"
            if tmp[0] == '0':
                tmp = ' ' + tmp[1:]
            self.now = tmp
            if self.alarm == self.now and self.alarm_is_off and not self.alarm_locked:
                self.alarm_locked = True
                self.alarm_is_off = False
                self.blink_led()
                self.start_music()
            if self.alarm != self.now and self.alarm_is_off:
                self.alarm_locked = False
            Timer(0.5, self.get_time).start()

    # Setter function to set the alarm string value
    def set_alarm(self, alarm):
        self.alarm = alarm

    # Event function to monitor the push button state, every 500ms
    def monitor_button(self):
        if not self.got_interrupted:
            if get_button_pressed():
                print("button pressed")
                self.alarm_is_off = True
                self.stop_music()
                set_led(False)
            Timer(0.5, self.monitor_button).start()

    # Event function to toggle the LED, blink period of 1 second
    def blink_led(self):
        if not self.got_interrupted and not self.alarm_is_off:
            set_led(self.led_on)
            self.led_on = not self.led_on
            Timer(0.5, self.blink_led).start()

    # Configure the music file to play
    def set_music(self, music_file):
        self.music_file = music_file
        if self.music_file is not None:
            mixer.init()
            mixer.music.load(self.music_file)

    # Start playing the music
    def start_music(self):
        if self.music_file is not None:
            mixer.music.play()

    # Stop playing the music
    def stop_music(self):
        if self.music_file is not None:
            mixer.music.stop()

    # Stop all event Timer functions by setting self.got_interrupted flag to True
    def stop(self):
        self.got_interrupted = True
        clear_displays()
        try:
            mixer.music.stop()
        except:
            pass

    def __str__(self):
        return f"Clock Thread {self.name}, display digits:'{self.now}'"
