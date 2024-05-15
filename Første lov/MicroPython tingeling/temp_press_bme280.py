################################################################################
from machine import Pin, Timer, ADC, I2C
import os
import math
import time
import onewire, ds18x20
import bme280

# Intialize temperature sensor
def init_probe_ds1820():
    #init the sensor,
    #red Vcc
    #black GND
    #yellow pin15 data
    SensorPin = Pin(15, Pin.IN)
    sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))
    roms = sensor.scan()
    print(roms)
    time.sleep(2)
    return sensor, roms

# Read temperature
def read_temp_probe_ds1820(sensor, roms):
    sensor.convert_temp()
    temperature = round(sensor.read_temp(roms[0]),2)
    return(temperature)

# Initialize pressure sensor
def init_bme280():
    i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method
    bme = bme280.BME280(i2c=i2c, mode=4)        #BME280 object creation
    return bme

# Read pressure
def read_temp_press_bme(bme_instance):
    temp, press, hum = bme_instance.read_compensated_data()
    temp = temp/100
    press=press/256/100 #hPa
    return temp, press

# Blink LED UwU
def blinc_led(timer):
    led.toggle()
    return

led = Pin(25, Pin.OUT)
timer = Timer(freq=10, callback = blinc_led)

# Check if we have taken any previous measurements
# If we have, loop through all existing filenames
# until we find one that isn't taken
a = 1
filename = 'datafile_termouge20' + str(a) + '.txt'
while True:
    if filename in os.listdir("./"):
        a += 1
        filename = 'datafile' + str(a) + '.txt'
    else:
        break
    
with open(filename, "w") as f:
    f.write("Time\ttemp_C\tpressure\n")

# Get the current time
# (time after initializing pico? idk)
start_time = time.ticks_ms()/1000

# Load temperature sensor
sensor, roms = init_probe_ds1820()
# Load pressure sensor
bme = init_bme280()

while True:
    temperature = read_temp_probe_ds1820(sensor, roms)
    pressure = read_temp_press_bme(bme)
    # Get time of measurement
    time_i = time.ticks_ms()/1000 - start_time
    # Save ALL of that good good data
    data_string_out = "%0.1f\t%0.2f\n%0.2f\n" %(time_i, temperature, pressure)
    print(time_i, temperature, pressure)
    
    with open(filename, "a") as f:
        f.write(data_string_out)
        
    time.sleep(0.5)


