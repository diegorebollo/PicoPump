from machine import ADC, Pin
import utime

SECONDS_PUMPING = 3
SECONDS_READOUT = 5
SENSOR = ADC(26)
RELAY = Pin(2, Pin.OUT)
RELAY_STATUS = None

def water_sensor_readout():
    
    sensor_read = SENSOR.read_u16()
    return sensor_read


def relay_off():
    
    global RELAY_STATUS
    RELAY.value(1)
    RELAY_STATUS = False
    return "Relay Off"
    


def relay_on():
    
    global RELAY_STATUS
    RELAY.value(0)
    RELAY_STATUS = True
    return "Relay On"

    
def main():
    
    while True:    
        relay_off()
        print(water_sensor_readout())
        if water_sensor_readout() < 21400:
            relay_on()
            utime.sleep(SECONDS_PUMPING)
        else:
            utime.sleep(SECONDS_READOUT)
