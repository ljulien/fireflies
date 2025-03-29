"""
Mimic a set of fireflies with MCP23017 chips
"""
# Copyright 2025 Linda Julien
#
# This code is licensed under MIT license (see LICENSE for details)
#
# Mimicking fireflies with MCP23017 boards
# Author: Linda Julien
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017

from firefly import Firefly

# MCP23017 expanders and pins in use
#
# Configure addresses for your MCP23017 expanders
# Valie addresses are 0x20...0x27
# Set the addresses on your MCP23017s by grounding pins A0, A1, A2.
#
# Configure pins 0 to 15 (i.e. GPIOA0...GPIOA7 and GPIOB0...GPIOB7)
#
MCPS = {
  0x27: [
      0, # GPIOA0
      1, # GPIOA1
      2, # GPIOA2
      3, # GPIOA3
      4, # GPIOA4
      5, # GPIOA5
      6, # GPIOA6
      7, # GPIOA7
      8, # GPIOB0
      9, # GPIOB1
      10, # GPIOB2
      11, # GPIOB3
      12, # GPIOB4
      13, # GPIOB5
      14, # GPIOB6
      15, # GPIOB7
  ]
}

PINS = {}

fireflies = []

# Initialize I2C
# Some boards use SCL and SDA pins
# i2c = busio.I2C(board.SCL, board.SDA)
# Raspberry Pi Pico uses GP1 and GP0 for SCL and SDA
i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

# Create an instance of the MCP23017 class for each chip
# and call get_pin to get an instance of each pin on the chip
for address, pins in MCPS.items():
    PINS[address] = []
    for pin in pins:
        mcp = MCP23017(i2c, address=address)
        io = mcp.get_pin(pin)
        io.switch_to_output()
        PINS[address].append(io)

# Create an instance of the Firefly class for each pin
for address, pins in PINS.items():
    for index, pin in enumerate(pins):
        fireflies.append(Firefly(pin=pin, name=f"{hex(address)}-{index}"))

# Loop through the fireflies and toggle them
try:
    while True:
        for firefly in fireflies:
            firefly.toggle_if_ready()
except KeyboardInterrupt:
    # If the user types Ctrl-C, darken all fireflies before exiting
    for firefly in fireflies:
        firefly.flash(False)

