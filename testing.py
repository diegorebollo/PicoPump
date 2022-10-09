import secrets
import utime
import _thread
import control
import ntptime
from mm_wlan import mm_wlan
from date_to_file import get_last_record
from microdot.microdot import Microdot, Response, redirect
from microdot.microdot_utemplate import render_template
from microdot.microdot_session import set_session_secret_key, with_session, update_session, delete_session

# Run main function in core0
_thread.start_new_thread(control.main, ())

# Connect to WIFI
try:
    mm_wlan.connect_to_network(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
except:    
    utime.sleep(180)
    mm_wlan.connect_to_network(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    
# Set Time    
try:
    ntptime.settime()
except:
    utime.sleep(10)
    ntptime.settime()

# Web Server  
app = Microdot()
set_session_secret_key(secrets.SECRET_KEY)
Response.default_content_type = 'text/html'


@app.route('', methods=['GET', 'POST'])
@with_session
def index(request, session):
    
    session_status = session.get('status')
    water_sensor_readout = control.water_sensor_readout()
    last_run_date = get_last_record()
    realy_status = control.RELAY_STATUS
    threshold = control.THRESHOLD
        
    if session_status is not 'authorized':
        return render_template('home.html', session_status=session_status, water_sensor_readout=water_sensor_readout, last_run_date=last_run_date, threshold=threshold, realy_status=realy_status)
    else:
        if request.method == 'POST':        
            if request.form['relay'] == 'off':
                control.relay_off()
                return redirect('/')
            elif request.form['relay'] == 'on':
                control.relay_on()
                return redirect('/')             
        else:
            return render_template('manage.html', session_status=session_status, water_sensor_readout=water_sensor_readout, last_run_date=last_run_date, threshold=threshold, realy_status=realy_status)       

@app.route('/login', methods=['GET', 'POST'])
@with_session
def login(request, session):    
    session_status = session.get('status')    
    if request.method == 'POST':        
        if request.form['user'] == secrets.USER and request.form['pwd'] == secrets.PASSWORD:
            update_session(request, {'status': 'authorized'})
            return redirect('/')
        else:
            return render_template('login.html', session_status=session_status, msg="Incorrect username or password.")
    elif session_status is not 'authorized':            
        return render_template('login.html', session_status=session_status, msg="")
    else:
        return redirect('/')

@app.route('/logout', methods=['GET'])
def logout(request):
    delete_session(request)
    return redirect('/')

app.run(port=80)
