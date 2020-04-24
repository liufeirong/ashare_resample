import datetime

def get_market_date():
    now_time = datetime.datetime.now()
    if now_time.strftime("%H:%M")<"09:30":
        now_time = now_time - datetime.timedelta(days=1)
    if now_time.weekday() > 4:
        now_time = now_time - datetime.timedelta(days=now_time.weekday() - 4)

    return now_time.strftime("%Y-%m-%d")

def get_first_date(freq='w'):
    now_time = datetime.datetime.now()
    if now_time.strftime("%H:%M")<"09:30":
        now_time = now_time - datetime.timedelta(days=1)
    if now_time.weekday() > 4:
        now_time = now_time - datetime.timedelta(days=now_time.weekday() - 4)
    if freq == 'd':
        fisrt_date = now_time
    elif freq == 'w':
        fisrt_date = now_time - datetime.timedelta(days=now_time.weekday())
    else:
        fisrt_date = now_time - datetime.timedelta(days=now_time.day-1)
    
    return fisrt_date.strftime('%Y-%m-%d')


def get_last_date(freq='d'):
    now_time = datetime.datetime.now()
    if now_time.strftime("%H:%M")<"15:00":
        now_time = now_time - datetime.timedelta(days=1)
    if now_time.weekday() > 4:
        now_time = now_time - datetime.timedelta(days=now_time.weekday() - 4)
    if freq == 'd':
        last_date = now_time
    elif freq == 'w':
        last_date = now_time - datetime.timedelta(days=now_time.weekday()+1)
    else:
        last_date = now_time - datetime.timedelta(days=now_time.day)
        
    return last_date.strftime("%Y-%m-%d")


def get_delta_days(start_date, end_date):
    d1 = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    d2 = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    days = (d2 - d1).days + 1
    return days


def get_delta_date(start_date, add_days):
    d1 = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    d2 = d1 + datetime.timedelta(days=add_days)
    return d2.strftime("%Y-%m-%d")


def get_update_time():
    now_time = datetime.datetime.now()
    return now_time.strftime("%Y-%m-%d %H:%M:%S")


def time_cut(str_time):
    if str_time < '09:30:00':
        return '09:30:00'
    if str_time > '11:30:00' and str_time < '12:00:00':
        return '11:30:00'
    if str_time > '12:30:00' and str_time < '13:00:00':
        return '13:00:00'
    if str_time > '15:00:00':
        return '15:00:00'
    return str_time