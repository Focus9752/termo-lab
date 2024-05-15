################################################################################
from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280

def init_bme280():
    i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method
    bme = bme280.BME280(i2c=i2c, mode=4)        #BME280 object creation
    return bme

def read_temp_press_bme(bme_instance):
    temp, press, hum = bme_instance.read_compensated_data()
    temp = temp/100
    press=press/256/100 #hPa
    return temp, press
