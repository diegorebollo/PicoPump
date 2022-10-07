import ujson

FILE = 'date_history.json'
MAX_RECORDS = 5

def read_file():
    with open(FILE) as f:
        test = ujson.load(f)
        return test

def save_file(date_list):
    with open(FILE, 'w') as f:
        ujson.dump(date_list, f)
    
def get_last_record():    
    date = read_file()[-1]
    return date
       
# Just keeps last (MAX_RECORDS) records
def save_date(date):
    fdate_list = [f'{date[0]}-{date[1]}-{date[2]} {date[3]}:{date[4]}:{date[5]} (GTM)']
    try:
        read_file()
    except:
        save_file(fdate_list)
    else:
        list_in_file = read_file()
        if len(list_in_file) >= MAX_RECORDS:
            list_in_file.pop(0)
        list_in_file.append(fdate_list)        
        save_file(list_in_file)
        