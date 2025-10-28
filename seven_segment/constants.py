# seven-segment module constants file
# Author: Eddy Ferre - ferree@seattleu.edu

# Seven-segment display tester
#
#        A
#      =====
#   F #     # B
#     #  G  #
#      =====
#   E #     # C
#     #     #
#      =====  # DP
#        D
#

# Defines the segment active/inactive for each characters, numbers and symbols
#                        A  B  C  D  E  F  G
SEGS_FOR_CHAR = { '0': [ 1, 1, 1, 1, 1, 1, 0 ],
                  '1': [ 0, 1, 1, 0, 0, 0, 0 ],
                  '2': [ 1, 1, 0, 1, 1, 0, 1 ],
                  '3': [ 1, 1, 1, 1, 0, 0, 1 ],
                  '4': [ 0, 1, 1, 0, 0, 1, 1 ],
                  '5': [ 1, 0, 1, 1, 0, 1, 1 ],
                  '6': [ 1, 0, 1, 1, 1, 1, 1 ],
                  '7': [ 1, 1, 1, 0, 0, 0, 0 ],
                  '8': [ 1, 1, 1, 1, 1, 1, 1 ],
                  '9': [ 1, 1, 1, 1, 0, 1, 1 ],
                  'A': [ 1, 1, 1, 0, 1, 1, 1 ],
                  'C': [ 1, 0, 0, 1, 1, 1, 0 ],
                  'E': [ 1, 0, 0, 1, 1, 1, 1 ],
                  'F': [ 1, 0, 0, 0, 1, 1, 1 ],
                  'H': [ 0, 1, 1, 0, 1, 1, 1 ],
                  'I': [ 0, 1, 1, 0, 0, 0, 0 ],
                  'J': [ 0, 1, 1, 1, 0, 0, 0 ],
                  'L': [ 0, 0, 0, 1, 1, 1, 0 ],
                  'O': [ 1, 1, 1, 1, 1, 1, 0 ],
                  'P': [ 1, 1, 0, 0, 1, 1, 1 ],
                  'S': [ 1, 0, 1, 1, 0, 1, 1 ],
                  'U': [ 0, 1, 1, 1, 1, 1, 0 ],
                  'Y': [ 0, 1, 1, 0, 0, 1, 1 ],
                  'c': [ 0, 0, 0, 1, 1, 0, 1 ],
                  'd': [ 0, 0, 0, 1, 1, 0, 1 ],
                  'h': [ 0, 0, 1, 0, 1, 1, 1 ],
                  'i': [ 0, 0, 1, 0, 0, 0, 0 ],
                  'l': [ 0, 1, 1, 0, 0, 0, 0 ],
                  'n': [ 0, 0, 1, 0, 1, 0, 1 ],
                  'o': [ 0, 0, 1, 1, 1, 0, 1 ],
                  'r': [ 0, 0, 0, 0, 1, 0, 1 ],
                  't': [ 0, 0, 0, 1, 1, 1, 1 ],
                  'u': [ 0, 0, 1, 1, 1, 0, 0 ],
                  '[': [ 1, 0, 0, 1, 1, 1, 0 ],
                  ']': [ 1, 1, 1, 1, 0, 0, 0 ],
                  '-': [ 0, 0, 0, 0, 0, 0, 1 ],
                  '_': [ 0, 0, 0, 1, 0, 0, 0 ],
                  '=': [ 0, 0, 0, 1, 0, 0, 1 ],
                  ' ': [ 0, 0, 0, 0, 0, 0, 0 ],
                }

# Display Selector (cathode) GPIO Pin Allocation
#              D1  D2  D3  D4
DISP_OUT_L = [ 12, 16,  8,  7 ]

# Colon GPIO Allocation
COLON_OUT_H = 17

# Thousand mark GPIO Allocation
THOUSAND_OUT_H = 1

# Decimal Point
DP_OUT_H = 2

# 7-Segment anodes GPIO allocation
SEGMENT_OUT_H = [ 23,  # A
                  25,  # B
                  18,  # C
                   4,  # D
                   3,  # E
                  15,  # F
                  24,  # G
              ]

# LED Output pin
LED_OUT_H = 14

# Push button input pin
BUTTON_IN = 21

ACTIVE_LOW_PINS = DISP_OUT_L
ACTIVE_HIGH_PINS = [COLON_OUT_H] + [THOUSAND_OUT_H] + [DP_OUT_H] + SEGMENT_OUT_H + [LED_OUT_H]

OUT_PINS = ACTIVE_LOW_PINS + ACTIVE_HIGH_PINS
IN_PINS = [BUTTON_IN]

HIGH = True
LOW = False
