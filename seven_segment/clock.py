# seven-segment module Clock class file
# Author: Eddy Ferre - ferree@seattleu.edu

from threading import Timer, Thread
from datetime import datetime

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer

#from .display import *
from .display import *


class Clock(Thread):
    
    """A clock object.

    In this example, we are documenting attributes in an attributes section
    at the beginning of the class.  Attributes are defined in the __init__
    method but documented here.

    Attributes:
        blink_on (bool): state of the blinking colon.
        led_on (bool): state of the blinking LED.
        got_interrupted (bool): flag to determine if clock
            was interrupted.
        alarm_is_off (bool) = flag to determine if alarm is off
        alarm_locked (bool) = flag to determine if alarm is locked         
        now (str): current time, four digits, blank if first
            digit not one.
        alarm_time (str): current time, four digits, blank if
            first digit not one.
        music_file (str): file name for the mp3 to play when alarm sounds
        
    """
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
        """Runs the clock.

        This method iterates through the main display functions after
        getting the time and updating the now attribute of the class.  It also
        instatiates methods that are timed and thus continously updated. This is
        how get_time and monitor_button work.
        
        """
        self.blink_colon()     # Start blink_colon periodic event
        self.get_time()        # Start time capture periodic event
        self.monitor_button()  # Monitor the push button
        while not self.got_interrupted:
            clock_displays(self.now)   # Continuously display current time
        clear_displays()       # Turn off all LEDs

    
    def blink_colon(self):
        """Event method to toggle the colon LED, blink period of 1 second

        This method uses a timer to change the state of the colon LED at
        a regular interval.
        
        Todo:
            * Could add an argument to blink at user-specified rate, but for now,
            it blinks at a hard-coded rate.
        
        """
        if not self.got_interrupted:
            self.blink_on = not self.blink_on
            set_colon(self.blink_on)
            Timer(0.1, self.blink_colon).start()

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

    def monitor_button(self):
        """Event method to monitor the push button state, every 500ms.

        Method calls itself at 500 ms intervals and checks the state
        of the button. This can be thought of as a property that can
        be checked at any time to get the state of the button.  Like other
        event methods, it is stopped if there is an interrupt.
        
        """
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
