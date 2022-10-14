from machine import ADC, Pin
from date_to_file import save_date, read_file
import utime


SENSOR = None
RELAY = None
SECONDS_PUMPING = None
SECONDS_READOUT = None
THRESHOLD = None
RELAY_STATUS = None
VAR_FILE = 'variables.json'


def update_var():
    
    global SENSOR, RELAY, SECONDS_PUMPING, SECONDS_READOUT, THRESHOLD
    vars_file = read_file(VAR_FILE)

    SENSOR = ADC(vars_file['sensor_pin'])
    RELAY = Pin(vars_file['relay_pin'], Pin.OUT)
    SECONDS_PUMPING = vars_file['seconds_pumping']
    SECONDS_READOUT = vars_file['seconds_readout']
    THRESHOLD = vars_file['threshold']


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
    
    update_var()
    print('main func working')
    while True:        
        relay_off()
        if water_sensor_readout() < THRESHOLD:
            relay_on()
            utime.sleep(SECONDS_PUMPING)
        else:
            utime.sleep(SECONDS_READOUT)
            
            
