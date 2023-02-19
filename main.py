import secrets
import utime
import control
import uasyncio
from mm_wlan import mm_wlan
from file_manager import get_last_record, read_file, save_file, get_date
from microdot.microdot_utemplate import render_template
from microdot.microdot_asyncio import Microdot, Response, redirect, send_file
from microdot.microdot_session import set_session_secret_key, with_session, update_session, delete_session


# Connect to WIFI
try:
    mm_wlan.connect_to_network(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
except:
    while not mm_wlan.is_connected():
        utime.sleep(300)
        mm_wlan.connect_to_network(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
    
# Web Server
app = Microdot()
Response.default_content_type = 'text/html'
set_session_secret_key(secrets.SECRET_KEY)

@app.route('', methods=['GET', 'POST'])
@with_session
async def index(request, session):

    session_status = session.get('status')
    water_sensor_readout = control.sensor_readout()
    last_run_date = get_last_record()
    realy_status = control.RELAY_STATUS
    threshold = control.SENSOR_THRESHOLD
    vars_file = read_file('variables.json')
    date = str(get_date())

    if session_status is not 'authorized':
        return render_template('home.html', vars_file=vars_file, session_status=session_status, water_sensor_readout=water_sensor_readout, last_run_date=last_run_date, threshold=threshold, realy_status=realy_status, date=date)
    else:
        if request.method == 'POST':
            var_name = request.form['var_name']
            new_value = request.form['new_value']
            vars_file[var_name] = int(new_value)
            save_file('variables.json', vars_file)
            uasyncio.create_task(control.update_vars())
            return redirect('/')
        else:
            return render_template('home.html', vars_file=vars_file, session_status=session_status, water_sensor_readout=water_sensor_readout, last_run_date=last_run_date, threshold=threshold, realy_status=realy_status, date=date)

@app.route('/login', methods=['GET', 'POST'])
@with_session
async def login(request, session):
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
    
@app.errorhandler(404)
async def not_found(request):
    return render_template('404.html')


@app.route('/relayon', methods=['GET'])
@with_session
async def relay_on(request, session):
    session_status = session.get('status')
    if session_status is not 'authorized':
        return redirect('/404')
    else:
        control.force_relay_on()
        return redirect('/')


@app.route('/relayoff', methods=['GET'])
@with_session
async def relay_off(request, session):
    session_status = session.get('status')
    if session_status is not 'authorized':
        return redirect('/404')
    else:
        control.relay_off()
        return redirect('/')


@app.get('/logout')
async def logout(request):
    delete_session(request)    
    return redirect('/')


@app.get('/history')
async def history_json(request):
    date_file = read_file('date_history.json')
    return date_file

@app.get('/readout')
async def readout(request):
    water_sensor_readout = control.sensor_readout()
    return str(water_sensor_readout)

async def main():
    uasyncio.create_task(control.main())
    await app.run(debug=True, port=80)
    
uasyncio.run(main())