from machine import ADC, Pin
from file_manager import save_date, read_file
import utime


SENSOR = None
RELAY = None
SECONDS_PUMPING = None
SECONDS_READOUT = None
THRESHOLD = None
RELAY_STATUS = None
MAIN_FUNC_WORKING = True
OVERRIDE = False
OVERRIDE_ACTION = None
VAR_FILE = 'variables.json'


def update_vars():
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


def force_relay_off():
    global OVERRIDE, OVERRIDE_ACTION

    OVERRIDE_ACTION = 'OFF'
    OVERRIDE = 'True'


def relay_on():
    global RELAY_STATUS

    RELAY.value(1)
    RELAY_STATUS = True
    save_date()
    return "Relay On"


def force_relay_on():
    global OVERRIDE, OVERRIDE_ACTION

    OVERRIDE_ACTION = 'ON'
    OVERRIDE = 'True'


def main():
    global OVERRIDE

    print('main func working')
    while MAIN_FUNC_WORKING:
        if not OVERRIDE:
            update_vars()
            relay_off()
            print(water_sensor_readout())
            if water_sensor_readout() < THRESHOLD:
                relay_on()
                utime.sleep(SECONDS_PUMPING)
            else:
                utime.sleep(SECONDS_READOUT)
        else:
            if OVERRIDE_ACTION == 'ON':
                relay_on()
            elif OVERRIDE_ACTION == 'OFF':
                relay_off()
            else:
                pass
            utime.sleep(SECONDS_PUMPING)
            OVERRIDE = False
