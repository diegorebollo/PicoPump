import secrets
import utime
import _thread
import control
from mm_wlan import mm_wlan
from microdot.microdot import Microdot, Response
from microdot.microdot_utemplate import render_template

ssid = secrets.WIFI_SSID
password = secrets.WIFI_PASSWORD

 
core = _thread.start_new_thread(control.main, ())

mm_wlan.connect_to_network(ssid, password)
app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
def index(request):    
    sensor_readout = control.water_sensor_readout()
    if request.method == 'POST':
        control.relay_on()
    return render_template('index.html', sensor_readout=sensor_readout)



app.run(port=80)
