from machine import Pin, Timer, ADC, I2C
import math
import time
import onewire, ds18x20
import bme280



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

def read_temp_probe_ds1820(sensor, roms):
    sensor.convert_temp()
    temperature = round(sensor.read_temp(roms[0]),2)
    return(temperature)


led = Pin(25, Pin.OUT)
timer = Timer(freq=10, callback = blinc_led)

#data logging in data.txt - data saved on the board
start_time = time.ticks_ms()/1000


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
    f.write("Time\ttemp_C\n")


sensor, roms = init_probe_ds1820()
while True:
    temperature = read_temp_probe_ds1820(sensor, roms)
    time_i = time.ticks_ms()/1000 - start_time
    data_string_out = "%0.1f\t%0.2f\n" %(time_i, temperature)
    print(temperature)
    
    with open(filename, "a") as f:
        f.write(data_string_out)
        
    time.sleep(0.5)
