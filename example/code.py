################################################################################
# Example to demonstrate the text animations
#
# Author: DerBroader71 (Tudor Davies)
#
# This is an example running on the Waveshare 2.8inch Touch Display Module for
# Raspberry Pi Pico 
# https://www.waveshare.com/pico-restouch-lcd-2.8.htm
################################################################################
import terminalio
import displayio
from adafruit_st7789 import ST7789
import gc
import time
import board
from waveshare_res_touch import WaveshareResTouch, PORTRAIT, LANDSCAPE
from random import randint
import math
import adafruit_imageload
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from text_animations import TextAnimations

# Release any resources currently in use for the displays
displayio.release_displays()
TFT_WIDTH = 320
TFT_HEIGHT = 240
ORIENTATION = LANDSCAPE

tft_dc = board.GP8
tft_cs = board.GP9
spi_clk = board.GP10
spi_mosi = board.GP11
spi_miso = board.GP12
tft_rst = board.GP15
backlight = board.GP13

waveshare = WaveshareResTouch(width=TFT_WIDTH, height=TFT_HEIGHT, orientation=ORIENTATION)

display = waveshare.DISPLAY
spi = waveshare.spi

animations = TextAnimations(display, terminalio.FONT, color=0xFFFFFF)

# Create a text label
#text_area = animations.create_text("Fading Text!", x=10, y=30)
# Set up the fade effect
#fade_update = animations.fade(text_area, steps=50, delay=0.05, repeat=True)

# Create a text label
text_area = animations.create_text("Glitching Text!", x=10, y=30)
# Set up the glitch effect
glitch_update = animations.glitch(text_area, steps=50, delay=0.25, pause_cycles=20)

# Create a text label
#text_area = animations.create_text("Matrix Effect!", x=10, y=30)
# Set up the matrix effect
#matrix_update = animations.matrix(text_area, delay=0.2)

# Create a text label
#text_area = animations.create_text("Destroying Text!", x=10, y=30)
# Set up the destroy effect
#destroy_update = animations.destroy(text_area, delay=0.1, pause_cycles=20)

# Main loop
while True:
    #fade_update() 		# works perfectly
    glitch_update() 	# works perfectly
    #matrix_update() 	# works perfectly
    #destroy_update() 	# works perfectly






