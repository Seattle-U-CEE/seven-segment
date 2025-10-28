"""Module for displaying time on a seven segment display.

This __init__.py file provides some basic documentation and
ensures the python interpreter recognizes the folder containing
the file as a python module whose contents that can be imported
and used in your code.  The module includes this __init__.py
file, a __main__.py file runs a clock when the seven_segment
module is executed from the command line, a constants.py file
for defining GPIO pins, a clock.py file for defining the
Clock class, and a display.py file for controlling the
seven-segment display.

Note that to be able to import this module, you cannot use the
default folder name seven-segment that was used in the Git
repository for holding the .py files.  You  must change this to
something else--here, it has been changed to seven_segment.

Example:
    To use at the level of a Python REPL, you need to be in the
    correct folder, so in the same folder as the README.md file.
    Then you can import the modules and use them:

        >>> from seven_segment import constants as constants
        >>> from seven_segment import display as display
        >>> from seven_segment import clock as clock
        >>> c = clock.Clock()
        >>> display.init_display(True)
        >>> c.run()

    This will create an instance of the clock that prints time to the
    seven segment display. Main functions for controlling the screen
    are in display.py. Methods for getting user input from button push
    events and for creating events that periodically update the
    clock display are provided in clock.py and are accessible in the
    clock.Clock() class definition.
    
    To use the clock functionality from the command line, execute
    the file using the -m option, which runs a module as though
    it were a script.
    
        $ python -m seven_segment clock
    
    Here, the module is run using the clock argument.  

Todo:
    * The clock needs a stop-watch method. This can be implemented
      directly in the clock class or, better yet, in a child
      class defined in a stopwatch.py file that extends the
      functionality of the basic Clock class.  However, it is also
      OK to simply define this method as a run_stopwatch
      method in the Clock class itself.
    * The clock needs a timer method.  Similarly, this can be
      implemented either in a timer.py file that defines
      a child timer class that inherits from the Clock class or
      simply by adding a run_timer method to the Clock class
      itself.
    * The __main__.py file needs to be modified so that the
      timer and stopwatch modes can be started from the command
      line. This will require parsing arguments that are used
      to pass parameters that would be required by these modes.
"""