"""
Mimic a set of fireflies with the GPIO pins of a Raspberry Pi Pico
"""
# Copyright 2025 Linda Julien
#
# This code is licensed under MIT license (see LICENSE for details)
#
# Mimicking fireflies with a Raspberry Pi Pico
# Author: Linda Julien
import board
import busio
from digitalio import DigitalInOut

from firefly import Firefly

#
# Configure pins for use
#

GPIOS = [
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP16,
    board.GP17,
    board.GP18,
    board.GP19,
    board.GP20,
    board.GP22,
    board.GP26,
    board.GP27,
    board.GP28,
    
]

fireflies = []

# Create a firefly for each configured pin
count = 1
for gpio in GPIOS:
    pin = DigitalInOut(gpio)
    pin.switch_to_output()
    fireflies.append(Firefly(pin=pin, name=f"{count}"))
    count += 1

# Loop through the fireflies and toggle them
try:
    while True:
        for firefly in fireflies:
            firefly.toggle_if_ready()
except KeyboardInterrupt:
    # If the user types Ctrl-C, darken all fireflies before exiting
    for firefly in fireflies:
        firefly.flash(False)

