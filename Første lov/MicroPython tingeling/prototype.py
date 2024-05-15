from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280
import os

led = Pin(25, Pin.OUT)
def blinc_led(timer):
    led.toggle()
    return

#led = Pin(25, Pin.OUT)
#timer = Timer(freq=10, callback = blinc_led)
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


def init_probe_ds1820():
    #init the sensor,
    #red Vcc
    #black GND
    #yellow pin15 data
    SensorPin = Pin(16, Pin.IN)
    sensor = ds18x20.DS18X20(onewire.OneWire(SensorPin))
    roms = sensor.scan()
    print(roms)
    time.sleep(2)
    return sensor, roms

def read_temp_probe_ds1820(sensor, roms):
    sensor.convert_temp()
    temperature = round(sensor.read_temp(roms[0]),2)
    return(temperature)



#init time 
start_time = time.ticks_ms()/1000

#init bme280
bme_inst = init_bme280()
temp_bme, pressure = read_temp_press_bme(bme_inst)
pressure_lpass = 10000

#data logging in data.txt - data saved on the board
start_time = time.ticks_ms()/1000
led = Pin(25, Pin.OUT)
timer = Timer(freq=10, callback = blinc_led)

## to check if file exist
a = 1
filename = 'datafile' + str(a) + '.txt'
while True:
    if filename in os.listdir("./"):
        a += 1
        filename = 'datafile' + str(a) + '.txt'
    else:
        break
        



with open(filename, "w") as f:
    f.write("Time\tpressure\tpressure_low\ttemp_C\n")


sensor, roms = init_probe_ds1820()




while True:
    blinc_led(timer)
    temperature = read_temp_probe_ds1820(sensor, roms)
    time_i = time.ticks_ms()/1000 - start_time
    
    
    #######
    pressure_old = pressure_lpass
    temp_bme, pressure = read_temp_press_bme(bme_inst)
    pressure_lpass = low_pass(pressure_old, pressure, 0.4)
    time_i = time.ticks_ms()/1000 - start_time
    data_string_out = "%0.1f\t%0.4f\t%0.4f\t%0.3f\n" %(time_i, pressure, pressure_lpass,temperature)
    
    
    
    print(pressure_lpass, pressure, temp_bme, temperature)
    #######
    
    
    
    
    with open(filename, "a") as f:
        f.write(data_string_out)
        
    time.sleep(0.25)
