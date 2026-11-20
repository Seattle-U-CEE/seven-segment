#!/usr/bin/python

# seven-segment module Main function
# Author: Eddy Ferre - ferree@seattleu.edu

from traceback import print_exc
from sys import stdout
from os import path
from re import compile
from argparse import ArgumentParser

from .display import *
from .clock import Clock
from .timer import CountdownTimer, parse_timer
from .stopwatch import Stopwatch

CLOCK_PATTERN = compile(r"([12]?)(\d):([0-5])(\d)")


def validate_arguments(args):
    """Check the arguments of the chosen mode before touching the GPIO pins.

    Raises ValueError if they are invalid. Returns the timer length in seconds
    for 'timer' mode, otherwise None.
    """
    if args.mode == 'timer':
        return parse_timer(args.timerstart)

    # The other modes do not use -t
    if args.timerstart is not None:
        print(f"WARNING: --timerstart is ignored in '{args.mode}' mode")

    if args.mode == 'clock':
        if args.alarm is not None and CLOCK_PATTERN.match(args.alarm) is None:
            raise ValueError(f"ERROR: Invalid alarm argument '{args.alarm}'. Must be 'H:MM'")
        if args.music is not None and not path.isfile(args.music):
            raise ValueError(f"ERROR: Cannot find '{args.music}' file")
    return None


def run_until_done(worker):
    """Start a Thread and wait for it to finish (Ctrl+c still works)"""
    worker.start()
    while worker.is_alive():
        worker.join(0.2)


def main():
    clock = None
    worker = None
    channels_set = False
    clock_pattern = compile(r"([12]?)(\d):([0-5])(\d)")

    try:
        parser = ArgumentParser(description='Seven-Segment Clock Display')
        parser.add_argument('mode',
                            default='clock',
                            const='clock',
                            nargs='?',
                            choices=['clock', 'timer', 'stopwatch', 'freeform'],
                            help='list of modes (default: %(default)s)')
        parser.add_argument('-a',
                            '--alarm',
                            action='store',
                            help="Alarm time, H:MM format (24hr)")
        parser.add_argument('-m',
                            '--music',
                            action='store',
                            help="Music to play as alarm")
        parser.add_argument('-t',
                            '--timerstart',
                            action='store',
                            help="Timer start, MM:SS format")

        args = parser.parse_args()

        # Validate the arguments of the chosen mode before touching the GPIO pins
        timer_seconds = validate_arguments(args)

        # Setup and Initialize the GPIO pins
        init_display(channels_set)

        if args.mode == 'clock':
            alarm = None
            music_file = None
            if args.alarm is not None:
                m = clock_pattern.match(args.alarm)
                if m is None:
                    print(f"ERROR: Invalid alarm argument '{args.alarm}'. Must be 'H:MM'")
                else:
                    print(f"Alarm set to {args.alarm}")
                    alarm = args.alarm.replace(":", "")
                    if m.group(1) == '':
                        alarm = " " + alarm
                    if args.music is not None:
                        if path.isfile(args.music):
                            music_file = args.music
                        else:
                            print(f"ERROR: Cannot find '{args.music}' file")

            print("Running 'clock' mode ...")
            clock = Clock()
            clock.set_alarm(alarm)
            clock.set_music(music_file)
            clock.start()
            # Stay in 'clock' mode until Ctrl+c
            while True:
                sleep(1.0)

        elif args.mode == 'stopwatch':
            print("Running 'stopwatch' mode ...")
            worker = Stopwatch()
            run_until_done(worker)      # Stay in 'stopwatch' mode until Ctrl+c

        elif args.mode == 'timer':
            print(f"Running 'timer' mode, counting down from {args.timerstart} ...")
            worker = CountdownTimer(timer_seconds)
            run_until_done(worker)      # Returns when the button is pressed at 00:00

        else:   # args.mode == 'freeform'

            # Let user enter 4 characters
            string = input("Enter what you want the clock display to print: ")

            # Parse Clock entry
            m = clock_pattern.match(string)
            if m is None:
                pass
            elif m.group(1) == '2' and m.group(2) not in "0123":
                raise ValueError("Clock - Invalid entry")
            else:
                print("Valid clock entry")
                # Sets the Digits
                if m.group(1) == '':
                    digits = " "
                else:
                    digits = m.group(1)
                for i in range(2, 5):
                    digits += m.group(i)
                while True:
                    activate_displays(digits, set_colon=True)
            print("not a clock entry")

            # Parse number
            try:
                # noinspection PyUnusedLocal
                value = float(string)
                print("Valid number")
                # TODO: write your code here!
                # Watch for negative values, floating points...
            except ValueError:
                pass
                print("not a number")

            # Parse anything else
            valid_char = ''.join(list(SEGS_FOR_CHAR.keys())).replace("-", "\\-").replace("[","\[").replace("]","\]")
            print(valid_char)
            pattern = compile(
                rf"([{valid_char}])?(\.)?([{valid_char}])?(\.)?(:)?([{valid_char}])?(\.)?(')?([{valid_char}])?(\.)?")
            m = pattern.match(string)
            if m is None:
                pass
            elif m.groups() != (None, None, None, None, None, None, None, None, None, None):
                digit_group_indexes = [1, 3, 6, 9]
                dp_group_indexes = [2, 4, 7, 10]
                print(m.groups())
                digits = ""
                dp = [False] * 4
                for i in digit_group_indexes:
                    if m.group(i) is None:
                        digits += " "
                    else:
                        digits += m.group(i)
                dp_idx = 0
                for i in dp_group_indexes:
                    dp[dp_idx] = m.group(i) is not None
                    dp_idx += 1
                set_colon = m.group(5) is not None
                set_thousand = m.group(8) is not None
                while True:
                    activate_displays(digits, decimal_point=dp, set_colon=set_colon, set_thousand=set_thousand)

            digits = "-Err"
            print(f"Could not parse entry, showing: '{digits}'")
            while True:
                activate_displays(digits)

    except KeyboardInterrupt:
        if clock is not None:
            clock.stop()
        if worker is not None:
            worker.stop()
            worker.join(1.0)    # let it stop driving the pins before cleanup()
        print("\b\b  \nCtrl+c pressed, exiting")
    except ValueError as e:
        print(e)
    except Exception:
        print("-" * 60)
        print_exc(file=stdout)
        print("-" * 60)
    finally:
        cleanup()


if __name__ == "__main__":
    main()
