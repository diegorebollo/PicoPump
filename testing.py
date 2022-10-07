import secrets
import utime
import _thread
import control
import ntptime
from date_to_file import get_last_record
from mm_wlan import mm_wlan
from microdot.microdot import Microdot, Response
from microdot.microdot_utemplate import render_template

ssid = secrets.WIFI_SSID
password = secrets.WIFI_PASSWORD
 
core = _thread.start_new_thread(control.main, ())

mm_wlan.connect_to_network(ssid, password)

ntptime.settime()

app = Microdot()
Response.default_content_type = 'text/html'


@app.route('/', methods=['GET', 'POST'])
def index(request):
    status = control.RELAY_STATUS
    sensor_readout = control.water_sensor_readout()
    threshold = control.THRESHOLD
    last_run_date = get_last_record() 
    if request.method == 'POST':
        control.relay_on()
    return render_template('index.html', sensor_readout=sensor_readout, latest = last_run_date, threshold=threshold, status=status)


app.run(port=80)
