#Example of low pass filter using the pressure bme280

################################################################################
from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280


###################################################################################
###################################################################################
def low_pass(old, new, alpha):
    return old*alpha+new*(1-alpha)


###################################################################################
###################################################################################
def init_bme280():
    i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method
    time.sleep_ms(1000)
    bme = bme280.BME280(i2c=i2c, mode=4)        #BME280 object creation
    return bme

def read_temp_press_bme(bme_instance):
    temp, press, hum = bme_instance.read_compensated_data()
    temp = temp/100
    press=press/256/100 #hPa
    return temp, press


#init time 
start_time = time.ticks_ms()/1000

#init bme280
bme_inst = init_bme280()
temp_bme, pressure = read_temp_press_bme(bme_inst)
pressure_lpass = 10000

while True:
    pressure_old = pressure_lpass
    temp_bme, pressure = read_temp_press_bme(bme_inst)
    pressure_lpass = low_pass(pressure_old, pressure, 0.4)
    time_i = time.ticks_ms()/1000 - start_time
    data_string_out = "%0.1f\t%0.4f\n" %(time_i, pressure)
    print((pressure_low, pressure))
        
    time.sleep(0.05)
