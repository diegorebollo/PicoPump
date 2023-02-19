from file_manager import save_date, read_file
from machine import ADC, Pin, reset
import micropython
import uasyncio
import time

SENSOR = None
RELAY = None
SECONDS_PUMPING = None
SECONDS_READOUT = None
SENSOR_THRESHOLD = None
RELAY_STATUS = None
MAIN_FUNC_WORKING = True
OVERRIDE = False
SAFETY_REBOOT = True
SAFETY_REBOOT_TIME = 24 # hours
VAR_FILE = 'variables.json'


async def update_vars():
    global SENSOR, RELAY, SECONDS_PUMPING, SECONDS_READOUT, SENSOR_THRESHOLD

    vars = read_file(VAR_FILE)

    SENSOR = ADC(vars['sensor_pin'])
    RELAY = Pin(vars['relay_pin'], Pin.OUT)
    SECONDS_PUMPING = vars['seconds_pumping']
    SECONDS_READOUT = vars['seconds_readout']
    SENSOR_THRESHOLD = vars['threshold']


def sensor_readout():

    sensor_read = SENSOR.read_u16()
    return sensor_read


def relay_off():
    global RELAY_STATUS

    RELAY.value(0)
    RELAY_STATUS = False
    return 'Relay Off'


def relay_on():
    global RELAY_STATUS

    RELAY.value(1)
    RELAY_STATUS = True
    save_date()
    return "Relay On"


def force_relay_on():
    global OVERRIDE

    OVERRIDE = 'True'
    

class LedStatus():
    def __init__(self):
        self.led = Pin("LED", Pin.OUT)
    
    def on(self):
        self.led.on()
        
    def turn_on(self, n):
        self.led.on()
        time.sleep(n)     
        self.led.off()
        
        
async def reboot():
    if SAFETY_REBOOT:
        await uasyncio.sleep_ms(SAFETY_REBOOT_TIME * 60 * 60 * 1000)

        if not RELAY_STATUS:
            print('rebooting')
            reset()
        else:
            await uasyncio.sleep_ms(SECONDS_PUMPING * 1000)
            print('rebooting')
            reset()
            

async def main():
    global OVERRIDE
    
    print('control func working')
    uasyncio.create_task(update_vars())
    await uasyncio.sleep_ms(2000) # needed for update_vars
    
    # Turn On Status LED
    led = LedStatus()
    led.turn_on(3)
    
    # Safety Reboot
    uasyncio.create_task(reboot())    
        
    while MAIN_FUNC_WORKING:
        if not OVERRIDE:
            relay_off()
            led.turn_on(1)
            print(sensor_readout())
            if sensor_readout() < SENSOR_THRESHOLD and sensor_readout() > 15000:
                led.on()
                relay_on()
                await uasyncio.sleep_ms(SECONDS_PUMPING * 1000)
            else:
                await uasyncio.sleep_ms(SECONDS_READOUT * 1000)
        else:
            relay_on()
            await uasyncio.sleep_ms(SECONDS_PUMPING * 1000)
            OVERRIDE = False

