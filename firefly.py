"""
Mimic a firefly.
"""
# Copyright 2025 Linda Julien
#
# This code is licensed under MIT license (see LICENSE for details)
#
# Mimicking fireflies with MCP23017 boards
# Author: Linda Julien
import random
import time

# Add additional logging
DEBUG = True

# Parameters for flashing
# These times are consistent with male Photinus pyralis
LIGHT_TIME = 0.75
MIN_DARK_TIME = 5.0
MAX_DARK_TIME = 7.0

class Firefly:
    """
    Class to mimic a firefly.
    """
    def __init__(self, pin, name="Unknown", flash_delay=None):
        current_time = time.monotonic()

        self.pin = pin
        self.pin.switch_to_output(value=False)
        self.name = name

        # Initialize the times flash started and ended
        self.flash_start = current_time
        self.flash_end = current_time

        # Firefly is dark by default
        self.pin.value = False

        # How long between flashes
        self.set_flash_delay(flash_delay=flash_delay)

    def toggle_if_ready(self):
        """
        Toggle the state of this firefly if it's time to do so
        """
        if self.is_ready_to_toggle():
            self.toggle()

    def toggle(self):
        """
        Toggle the state of this firefly
        """
        if DEBUG:
            print(f"Firefly: {self}")
            print(f"  Turning firefly {self.name} {'off' if self.is_lit() else 'on'}.")
        self.flash(not self.is_lit())

    def flash(self, value=True):
        """
        Turn this firefly on or off, as requested
        """
        current_time = time.monotonic()

        # Set the requested value
        self.pin.value = value

        # Note when the current state started
        if value:
            self.flash_start = current_time
        else:
            self.flash_end = current_time

        # Set a new random flash delay
        self.set_flash_delay()

    def is_lit(self):
        """
        Returns whether this firefly is currently lit
        """
        return self.pin.value

    def time_lit(self):
        """
        Returns the amount of time this firefly has been lit
        """
        current_time = time.monotonic()
        if self.is_lit():
            return current_time - self.flash_start
        return 0

    def time_dark(self):
        """
        Returns the amount of time this firefly has been dark
        """
        current_time = time.monotonic()
        if self.is_lit():
            return 0
        return current_time - self.flash_end

    def is_ready_to_toggle(self):
        """
        Returns whether this firefly is ready to switch to the next state
        """
        if self.is_lit():
            return self.time_lit() >= LIGHT_TIME
        return self.time_dark() >= self.flash_delay

    def set_flash_delay(self, flash_delay=None):
        """
        Set the amount of time to delay between flashes
        If no flash_delay value is provided, a random delay is chosen
        """
        if flash_delay is None:
            self.flash_delay = random.uniform(MIN_DARK_TIME, MAX_DARK_TIME)
        else:
            self.flash_delay = flash_delay

    def __str__(self):
        return f"flash_start = {self.flash_start}, flash_end = {self.flash_end}, " +\
            f"flash_delay = {self.flash_delay}, name = {self.name}, is_lit = {self.is_lit()}"
