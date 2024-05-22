"""
Blinking the onboard LED with a certain frequency using the timer class
"""

from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280


led = Pin(25, Pin.OUT)

def blinc_led(timer):
    led.toggle()
    return

timer = Timer(freq=0.5, callback = blinc_led)
print(timer)