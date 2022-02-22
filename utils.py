import datetime
import pytz

tz = pytz.timezone('Europe/Kiev')


def get_current_datetime():
    datetime_str = datetime.datetime.now().astimezone(tz).strftime('%d-%m-%Y, %H:%M:%S')
    date = datetime.datetime.strptime(datetime_str, '%d-%m-%Y, %H:%M:%S')
    return date
