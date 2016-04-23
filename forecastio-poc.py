import datetime
from forecastiopy import *


apikey = '25d0250f9473af8e0adc83af349b9787'

pcopa = [40.81212, -79.942693]

fio = ForecastIO.ForecastIO(apikey,
                            units=ForecastIO.ForecastIO.UNITS_AUTO,
                            lang=ForecastIO.ForecastIO.LANG_ENGLISH,
                            latitude=pcopa[0], longitude=pcopa[1])

UTC_OFFSET = 5
time = datetime.datetime.now()

print 'Latitude', fio.latitude, 'Longitude', fio.longitude
print 'Timezone', fio.timezone, 'Offset', fio.offset
print fio.get_url()
print

if fio.has_currently() is True:
    currently = FIOCurrently.FIOCurrently(fio)
    time = datetime.datetime.fromtimestamp(int(currently.time)).strftime('%Y-%m-%d %H:%M:%S')
    print 'Currently'
    for item in currently.get().keys():
        print item + ' : ' + unicode(currently.get()[item])
    print
    # or access attibutes directly
    print 'Current Temp:', currently.temperature
    print 'Current Humidity:', currently.humidity
    print 'Current Visibility:', currently.visibility
    print 'unix time:', currently.time
    print 'time:', time
    print
else:
    print 'No Currently data'

# if fio.has_minutely() is True:
#     minutely = FIOMinutely.FIOMinutely(fio)
#     print 'Minutely'
#     print 'Summary:', minutely.summary
#     print 'Icon:', minutely.icon
#     print
#     for minute in xrange(0, minutely.minutes()):
#         print 'Minute', minute+1
#         for item in minutely.get_minute(minute).keys():
#             print item + ' : ' + unicode(minutely.get_minute(minute)[item])
#         print
#         # or access attributes directly for a given minute.
#         # minutely.minute_3_time would also work
#         print 'Direct attibute:', minutely.minute_3_time
#         print
#     print
# else:
#     print 'No Minutely data'

if fio.has_daily() is True:
    daily = FIODaily.FIODaily(fio)
    print 'Daily'
    print 'Summary:', daily.summary
    print 'Icon:', daily.icon
    print
    for day in xrange(0, daily.days()):
        print 'Day', day+1
        for item in daily.get_day(day).keys():
            print item + ' : ' + unicode(daily.get_day(day)[item])
        print
        # or access attributes directly for a given day.
        # daily.day_7_time would also work
#        print 'Direct attibute:', daily.day_5_time
        print
    print
else:
    print 'No Daily data'

# if fio.has_flags() is True:
#     from pprint import pprint
#     flags = FIOFlags.FIOFlags(fio)
#     pprint(vars(flags))
#     # Get units directly
#     print flags.units
# else:
#     print 'No Flags data'

if fio.has_alerts() is True:
    from pprint import pprint
    alerts = FIOAlerts.FIOAlerts(fio)
    pprint(vars(alerts))
    # Get units directly
    print alerts.units
else:
    print 'No Alert data'
