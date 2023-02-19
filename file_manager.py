# File Manager & Get Date Function
import urequests
import ujson

TIME_API = 'http://worldtimeapi.org/api/ip'
DATE_FILE = 'date_history.json'
VAR_FILE = 'variables.json'
MAX_RECORDS = 10


def read_file(file):
    try:
        with open(file) as f:
            json_file = ujson.load(f)
    except:
        print(f'{file} not found. Returning dummy data')
        return ["1900-01-01 00:00:00"]
    else:
        return json_file


def save_file(file, data):
    with open(file, 'w') as f:
        ujson.dump(data, f)


def get_last_record():
    try:
        date = read_file(DATE_FILE)[-1]
    except:
        return None
    else:
        return date


def get_date():  
    try:
        current_time = urequests.get(TIME_API).json()['datetime'].split('T')
    except:
        print(f'Time API not working. Returning dummy data')
        return ["1900-01-01 00:00:00"]
    else:    
        date = current_time[0]
        time = current_time[1].split('.')[0]
        fdate = f'{date} {time}'    
        return fdate

# Keeps last MAX_RECORDS records
def save_date():
    date = get_date()
    try:
        list_in_file = read_file(DATE_FILE)
    except:
        save_file(DATE_FILE, [date])
    else:
        if len(list_in_file) >= MAX_RECORDS:
            list_in_file.pop(0)
        list_in_file.append(date)
        save_file(DATE_FILE, list_in_file)

