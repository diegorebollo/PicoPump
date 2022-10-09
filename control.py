from machine import ADC, Pin
from date_to_file import save_date
import utime 

SENSOR = ADC(26)
RELAY = Pin(7, Pin.OUT)
SECONDS_PUMPING = 3 
SECONDS_READOUT = 3
THRESHOLD = 22600
RELAY_STATUS = None

def water_sensor_readout():
    
    sensor_read = SENSOR.read_u16()
    return sensor_read


def relay_off():
    
    global RELAY_STATUS
    RELAY.value(0)
    RELAY_STATUS = False
    return "Relay Off"
    


def relay_on():
    
    global RELAY_STATUS    
    RELAY.value(1)
    RELAY_STATUS = True
    save_date()
    return "Relay On"


def main():      
    while True:
        print(water_sensor_readout())
        relay_off()        
        if water_sensor_readout() < THRESHOLD:            
            relay_on()
            utime.sleep(SECONDS_PUMPING)            
        else:
            utime.sleep(SECONDS_READOUT)
