import ujson
import datetime

DATE_FILE = 'date_history.json'
MAX_RECORDS = 5

def read_file(file):
    with open(file) as f:
        test = ujson.load(f)
        return test

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
    my_timezone = datetime.timezone(datetime.timedelta(hours=2))
    current_time = datetime.datetime.now(my_timezone)
    return current_time

# Just keeps last (MAX_RECORDS) records
def save_date():    
    fdate = str(get_date()).split('+')[0]
    try:
        list_in_file = read_file(DATE_FILE)
    except:
        save_file(DATE_FILE, [fdate])
    else:        
        if len(list_in_file) >= MAX_RECORDS:
            list_in_file.pop(0)
        list_in_file.append(fdate)        
        save_file(DATE_FILE, list_in_file)
