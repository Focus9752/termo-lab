"""
Blinking the onboard LED with a certain frequency using the timer class
"""

from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280



def blinc_led(timer):
    led.toggle()
    return


led = Pin(25, Pin.OUT)
timer = Timer(freq=0.5, callback = blinc_led)
print(timer)