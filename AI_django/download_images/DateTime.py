import jdatetime
import pytz

localtz = pytz.timezone('Asia/Tehran')


def date_time():
    Date = str(jdatetime.datetime.now(tz=localtz).strftime("%Y%m"))
    Time = str(jdatetime.datetime.now(tz=localtz).strftime("%H:00"))

    return Date, Time


def detail_time():
    year = int(jdatetime.datetime.now(tz=localtz).strftime("%Y"))
    month = int(jdatetime.datetime.now(tz=localtz).strftime("%m"))
    day = int(jdatetime.datetime.now(tz=localtz).strftime("%d"))
    time = str(jdatetime.datetime.now(tz=localtz).strftime("%H:00"))

    return year, month, day, time

# year, month, day, time = detail_time()
# print(year, month, day, time)