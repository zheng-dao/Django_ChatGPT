#import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'ptdata.settings'
#import django
#django.setup()
from django.conf import settings
import datetime
from datetime import datetime, date, timedelta
import time
import calendar
from calendar import monthrange
from dateutil.relativedelta import relativedelta
import pytz
from pytz import utc
from dateutil import tz
import numpy as np
import pandas as pd

local = pytz.timezone (settings.TIME_ZONE)

FIRST = 0
SECOND = 1
THIRD = 2
FOURTH = FORTH = 3  # for people who have finger trouble
FIFTH = 4
LAST = -1
SECONDLAST = -2
THIRDLAST = -3

MONDAY = MON = 0
TUESDAY = TUE = TUES = 1
WEDNESDAY = WED = 2
THURSDAY = THU = THUR = 3
FRIDAY = FRI = 4
SATURDAY = SAT = 5
SUNDAY = SUN = 6

JANUARY = JAN = 1
FEBRUARY = FEB = 2
MARCH = MAR = 3
APRIL = APR = 4
MAY = 5
JUNE = JUN = 6
JULY = JUL = 7
AUGUST = AUG = 8
SEPTEMBER = SEP = 9
OCTOBER = OCT = 10
NOVEMBER = NOV = 11
DECEMBER = DEC = 12

QUARTERS = {'q1':['03',3,1,2], 'q2':['06',4,5,6], 'q3':['09',7,8,9], 'q4':['12',10,11,12]}
MONTHS = {1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}

def get_qtr(month, return_int=False):
    if isinstance(month, (date, datetime)):
        month = month.month
    for k, v in QUARTERS.items():
        if isinstance(month, str) and 'q' in month.lower():
            if return_int:
                return int(QUARTERS[month.lower()][0])
            return QUARTERS[month.lower()][0]
        if month in v:
            if return_int:
                return int(k[-1])
            return k

def get_friendly_month(mo_int, return_short_name=True):
    mo = MONTHS[mo_int]
    if return_short_name:
        mo = mo[:3]
    return mo

def get_month(month, return_user_friendly=True, return_short_name=True):
    mo = month
    if not isinstance(mo, int) and mo[:1] == 'm':
        mo = int(mo[1:])
    if return_user_friendly:
        mo = get_friendly_month(int(mo), return_short_name)
    return mo

def get_ts(dt_str='now', format='%Y-%m-%d', stagger_start=0, stagger_end=0):
    if dt_str == 'now':
        dt = datetime.now()
    else:
        #print(type(dt_str)
        if type(dt_str) is str:
            dt = datetime.strptime(dt_str, format)
        elif type(dt_str) is date:
            dt = datetime.combine(dt_str, datetime.min.time())
        else:
            dt = dt_str

    start_date = dt
    end_date = start_date
    start_date = datetime.combine(start_date, datetime.min.time())
    #start_date = start_date.replace(tzinfo=local)
    start_dateR = start_date + timedelta(0,stagger_start)
    start_dateR = start_dateR.replace(tzinfo=utc)
    end_date = datetime.combine(end_date, datetime.min.time())
    #end_date = end_date.replace(tzinfo=local)
    end_date = end_date + timedelta(1, stagger_end)
    end_dateR = end_date.replace(tzinfo=utc)
    dt_now = datetime.now()
    now_dateR = dt_now.replace(tzinfo=utc)
    input_dtR = dt.replace(tzinfo=utc)

    start_dateR_unix = int(calendar.timegm(start_dateR.timetuple()))
    end_dateR_unix = int(calendar.timegm(end_dateR.timetuple()))
    now_dateR_unix = int(calendar.timegm(now_dateR.timetuple()))
    input_dateR_unix = int(calendar.timegm(input_dtR.timetuple()))

    start_date_unix = int(time.mktime(start_date.timetuple()))
    end_date_unix = int(time.mktime(end_date.timetuple()))
    now_date_unix = int(time.mktime(dt_now.timetuple()))
    input_date_unix = int(time.mktime(dt.timetuple()))

    local_day = {'start':start_dateR_unix, 'end':end_dateR_unix, 'now':now_dateR_unix, 'input':input_dateR_unix}
    utc_day = {'start':start_date_unix, 'end':end_date_unix, 'now':now_date_unix, 'input':input_date_unix}
    data = {'local':local_day, 'utc':utc_day}
    return data

def get_dt(ts, dt_type='datetime', naive=True):
    try:
        int(ts)
        dt = datetime.fromtimestamp(ts)
        dtu = datetime.utcfromtimestamp(ts)
        if dt_type == 'date':
            dt = date(dt.year, dt.month, dt.day)
            dtu = date(dtu.year, dtu.month, dtu.day)
    except:
        try:
            if len(ts) == 19:
                dt_format = '%Y/%m/%d %H:%M:%S'
            else:
                dt_format = '%Y/%m/%d'
            tsdata = get_ts(ts, dt_format)['utc']['now']
            dt = get_dt(tsdata)['local']
            dtu = get_dt(tsdata)['utc']
        except:
            dt = 'error in get_dt format for strptime'
            dtu = 'error in get_dt format for strptime'
    if naive == False and dt_type == 'datetime' and not type(dt) == str:
        dtu = pytz.utc.localize(dtu)
        dt = dtu.replace(tzinfo=local)
    data = {'local':dt, 'utc':dtu}
    return data

def get_last_month(year, month, return_dt=True):
    dt = datetime(year, month, 1)
    last_month = dt - relativedelta(months=1)
    if return_dt:
        return last_month
    return last_month.month

def get_next_month(year, month, return_dt=True, prev_month=False):
    dt = datetime(year, month, 1)
    delta = 1
    if prev_month:
        delta = -1
    next_month = dt + relativedelta(months=delta)
    if return_dt:
        return next_month
    return next_month.month

def get_last_day_of_month(year, month):
    last_day = monthrange(year, month)[1]
    return last_day

def get_year_start_end(year):
    yr_start = get_ts(date(year, 1, 1))['utc']['start']
    yr_end = get_ts(date(year, 12, 31))['utc']['end']
    return (yr_start, yr_end)

def get_month_start_end(year, month, timestamps=False):
    year = int(year); month = int(month)
    month_start = date(year, month, 1)
    month_end = date(year, month, get_last_day_of_month(year, month))
    if timestamps:
        month_start, dummy = get_day_start_end(month_start)
        dummy, month_end = get_day_start_end(month_end)
    return (month_start, month_end)

def get_day_start_end(dt_d_str=None):
    d = dt_d_str
    if isinstance(dt_d_str, str):
        d = datetime.strptime(dt_d_str,'%Y-%m-%d').date()
    elif isinstance(dt_d_str, datetime):
        d = dt_d_str.date()
    if not dt_d_str:
        d = date.today()
    tss = get_ts(d)['utc']['start']
    tse = get_ts(d)['utc']['end']
    return (tss, tse)

def get_zulu_time(input):
    if type(input) == int:
        dt_raw = get_dt(input)['local']
        zdt = dt_raw.strftime('%Y-%m-%dT%H:%M:%SZ')
    elif type(input) == str:
        if len(input) == 19:
            dt_raw = datetime.strptime(input, '%Y-%m-%d %H:%M:%S')
        else:
            dt_raw = datetime.strptime(input, '%Y-%m-%d')
        zdt = dt_raw.strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        zdt = input.strftime('%Y-%m-%dT%H:%M:%SZ')
    return zdt

def is_leapyear(year):
    diff = int(year)-2016
    a, remainder = divmod(diff,4)
    if remainder == 0:
        return True
    else:
        return False

def get_days_in_months_array(year=None, rolling=False, tss=None, tse=None):
    dt_start = dt_end = None
    leaps = []
    days_in_months = []
    leap_mos = [31,29,31,30,31,30,31,31,30,31,30,31]
    noleap_mos = [31,28,31,30,31,30,31,31,30,31,30,31]
    if not year:
        if tss:
            dt_start = get_dt(tss)['local']
            year = dt_start.year
            if dt_start.day != 1:
                print('Warning: starting day is NOT on the first of a month!!! ')
        if tse:
            dt_end = get_dt(tse)['local']
            if not tss:
                year = dt_end.year
            if get_last_day_of_month(dt_end.year, dt_end.month) != dt_end.day:
                print('Warning: ending day is NOT on the last day of a month!!! ')
        if dt_start.year != dt_end.year:
            year = range(dt_start.year, dt_end.year + 1)
    if not isinstance(year, list):
        year = [int(year)]
    for yr in year:
        leaps.append(is_leapyear(yr))
    for i, leap in enumerate(leaps):
        mos_index = 0
        moe_index = 11
        if i == 0 and dt_start and dt_start.month != 1:
            mos_index = dt_start.month - 1
        elif dt_end and i == (len(year) -1) and dt_end.month != 12:
            moe_index = dt_end.month
        if leap:
            days_in_months += leap_mos[mos_index:]
        else:
            days_in_months += noleap_mos[:moe_index]
    if rolling:
        rolling_days =  []
        tempsum = 0
        for mo in days_in_months:
            tempsum += mo
            rolling_days.append(tempsum)
        days_in_months = rolling_days
    return days_in_months

def doy_to_month(doy, year):
    dt = datetime(year, 1, 1) + timedelta(doy - 1)
    mo = dt.month
    return mo

def doy_to_day(doy, year):
    dt = datetime(year, 1, 1) + timedelta(doy - 1)
    d = dt.day
    return d

def doy_to_dt(doy_in, year, dtype='datetime'):
    doy = int(doy_in)
    d = date(year, doy_to_month(doy, year), doy_to_day(doy, year))
    if dtype in ['datetime', 'dt', None]:
        d = datetime(year, doy_to_month(doy, year), doy_to_day(doy, year))
    return d

def dt_to_d(dt):
    d = date(dt.year, dt.month, dt.day)
    return d

def d_to_dt(d, datetype='min'):
    if datetype == 'min':
        d = datetime.combine(d, datetime.min.time())
    else:
        d = datetime.combine(d, datetime.max.time())
    return d

def dt_snip(ts_min, ts_max, snip=['start', 'end']):
    dt_min = get_dt(ts_min)['local']
    print('tss', ts_min, dt_min)
    dt_max = get_dt(ts_max)['local']
    print('tse', ts_max, dt_max)
    if not(dt_min.hour == 0 and dt_min.minute == 0 and dt_min.second == 0):
        dt_min = dt_min + timedelta(1)
    if not(dt_max.hour == 0 and dt_max.minute == 0 and dt_max.second == 0):
        dt_max = dt_max + timedelta(-1)
    dts = dt_to_d(dt_min)
    dte = dt_to_d(dt_max)
    tss = ts_min
    tse = ts_max
    if 'start' in snip:
        tss = get_ts(dts)['utc']['start']
    if 'end' in snip:
        tse = get_ts(dte)['utc']['end']
    return tss, tse

def snip_times(ts_min, ts_max, interval=3600):
    year_start_ts_list = get_year_start_ts()
    tss, tse = dt_snip(ts_min, ts_max)
    check_yr_start = ts_min - interval
    snip = []
    if not check_yr_start in year_start_ts_list: #if start of year
        snip.append(['start'])
        print('snip start')
    if not tse in year_start_ts_list:
        snip.append(['end'])
        print('snip end')
    if snip:
        tss, tse = dt_snip(ts_min, ts_max, snip)
    return tss, tse

def get_ts_start_end(start_date=None, end_date=None, days_prior=365, end_date_delta = 0, get_ts_start='start', get_ts_end='end', return_type='timestamps'):
    if not end_date:
        end_date = date.today() + timedelta(end_date_delta)
    tse = get_ts(end_date)['utc'][get_ts_end]
    if not start_date:
        start_date = end_date - timedelta(days_prior)
    tss = get_ts(start_date)['utc'][get_ts_start]
    if return_type == 'dates':
        return start_date, end_date
    elif return_type == 'timestamps':
        return tss, tse

def get_ts_month(year, month, stagger_start=0, stagger_end=0, return_values=False):
    print(year, month)
    dts = datetime(year, month, 1)
    tss = get_ts(dts)['utc']['start']
    ld = get_last_day_of_month(year, month)
    dte = datetime(year, month, ld)
    tse = get_ts(dte)['utc']['end']
    data = {'start':tss, 'end':tse}
    if return_values:
        return (tss, tse)
    return data

def get_year_start_ts(start_year=2000, num_years=50):
    year_start_ts_list = []
    for i in range(0,num_years+1):
        d = date(2000+i,1,1)
        ts = get_ts(d)['utc']['start']
        year_start_ts_list.append(ts)
    return year_start_ts_list

def get_year_start_end(yr=date.today().year):
    d = date(int(yr), 1, 1)
    tss = get_ts(d)['utc']['start']
    tse = get_ts(date(int(yr),12,31))['utc']['end']
    return tss, tse

def convert(dt_d_ts_str, output='all', d_min_now_max='now'):
    dt = dt_d_ts_str
    if type(dt_d_ts_str) == str:
        dt = datetime.strptime(dt_d_ts_str, '%Y-%m-%d')
    elif type(dt_d_ts_str) in [int, float]:
        dt = get_dt(dt_d_ts_str)['local']
    elif type(dt_d_ts_str) == date:
        if d_min_now_max == 'min':
            dt = datetime.combine(dt_d_ts_str, datetime.min.time())
        elif d_min_now_max == 'max':
            dt = datetime.combine(dt_d_ts_str, datetime.max.time())
        else:
            dt = datetime.combine(dt_d_ts_str, datetime.now().time())

    dt2ts = get_ts(dt)['utc']['input']
    dt2d = dt.date()
    d2str = str(dt2d)
    dt2str = str(dt)
    doy = get_day_of_year(dt)
    dow = get_day_of_week(dt)
    if output == 'all':
        return {'dt':dt, 'd':dt2d, 'ts':dt2ts, 'dt_str':dt2str, 'd_str':d2str, 'doy':doy, 'dow':dow}
    elif output in ['ts', 'time']:
        out = dt2ts
    elif output in ['d', 'date']:
        out = dt2d
    elif output in ['d_str', 'date_string']:
        out = d2str
    elif output in ['dt_str', 'datetime_string']:
        out = dt2str
    out = dt
    return out

def tdelta_to_hours(tdelta):
    days2hours = tdelta.days * 24
    secs2hours = tdelta.seconds/60/60
    total_hours = days2hours + secs2hours
    return total_hours

def get_day_of_year(dt_d_ts, return_str=True):
    day_of_year = None
    if type(dt_d_ts) in [datetime, date]:
        day_of_year = str(dt_d_ts.timetuple().tm_yday)
    elif type(dt_d_ts) == str:
        dt = datetime.strptime(dt_d_ts, '%Y-%m-%d')
        day_of_year = str(dt.timetuple().tm_yday)
    elif type(dt_d_ts) in [int, float]:
        dt = get_dt(dt_d_ts)['local']
        day_of_year = str(dt.timetuple().tm_yday)
    if not return_str:
        return int(day_of_year)
    return day_of_year

def get_day_of_week(dt_d_ts, return_str=True):
    day_of_week = None
    dt = dt_d_ts
    if type(dt_d_ts) == str:
        dt = datetime.strptime(dt_d_ts, '%Y-%m-%d')
    elif type(dt_d_ts) in [int, float]:
        dt = get_dt(dt_d_ts)['local']
    day_of_week = dt.weekday()
    if return_str:
        day_of_week
    return int(day_of_week)

def get_woy(dt_d_ts, return_str=False):
    doy = get_day_of_year(dt_d_ts, return_str)
    return divmod(doy-1, 7)[0] + 1

def get_doy(dt_d_ts, return_str=True):
    doy = get_day_of_year(dt_d_ts, return_str)
    return doy

def get_dow(dt_d_ts, return_str=True):
    dow = get_day_of_week(dt_d_ts, return_str)
    return dow

def get_dates_list(start_date=None, end_date=None):
    dl = []
    if not start_date:
        start_date = end_date - timedelta(364)
    elif not end_date:
        end_date = start_date + timedelta(364)
    current_date = start_date
    while current_date != end_date + timedelta(1):
        dl.append(current_date)
        current_date += timedelta(1)
    return dl

def doy_is_hw(doy, yr=date.today().year):
    dt = doy_to_dt(int(doy), yr)
    if is_weekend(dt):
        return True
    elif is_holiday(dt):
        return True
    else:
        return False

def is_weekend(dt_d_ts):
    is_weekend = False
    dt = dt_d_ts
    if type(dt_d_ts) == str:
        dt = datetime.strptime(dt_d_ts, '%Y-%m-%d')
    elif type(dt_d_ts) in [int, float]:
        dt = get_dt(dt_d_ts)['local']
    if dt.isoweekday() in [6,7]:
        is_weekend=True
    return is_weekend

def is_holiday(dt_d_ts, holiday_qs=None):
    is_weekend = False
    dt = None
    d = dt_d_ts
    holidays = holiday_qs
    #if not holiday_qs:
    #    holidays = Dates_key.objects.values_list('key_date', flat=True).filter(holiday_flag=True)
    if isinstance(dt_d_ts, str):
        dt = datetime.strptime(dt_d_ts, '%Y-%m-%d')
    elif isinstance(dt_d_ts, [int, float]):
        dt = get_dt(dt_d_ts)['local']
    else:
        dt = dt_d_ts
    if dt:
        d = date(dt.year, dt.month, dt.day)
    if d in holidays:
        is_weekend=True
    return is_weekend

def get_holidays_weekends(year=None, rtype='both', start_date=None, end_date=None, include_leap=False):
    holidays = []
    holiday_qs = None
    if year:
        is_leap = is_leapyear(year)
        days = range(1,366)
        if is_leap and include_leap:
            days = range(1,367)
    else:
        days = get_dates_list(start_date, end_date)
    for d in days:
        if year:
            dt = doy_to_dt(d, year)
        else:
            dt = d
        if not holiday_qs:
            holiday_list = dates_key.objects.values_list('key_date', flat=True).filter(holiday_flag=True)
        is_h = is_holiday(dt, holiday_qs)
        is_w = is_weekend(dt)
        h = 0
        if is_h or is_w:
            if rtype == 'both':
                h = 1
            elif is_h and rtype == 'holidays':
                h = 1
            elif is_w and rtype == 'weekends':
                h = 1
        holidays.append(h)
    return holidays

def shift_dict(dict_to_shift, shift):
    lp_day_index = {}
    for key, value in dict_to_shift.iteritems():
        temp_val = value
        lp_day_index[str(int(key) + shift)] = temp_val
    return lp_day_index

def get_shift(d_lp, d, dict_to_shift=None):
    #if you have a list with 20 days in it, the shift returned is the index of the list that should be cut off. If it is negative, then it should cut off the leading negative indices like day -1, day -2
    day1 = d
    day1_day = day1.weekday()
    day1_lp = d_lp
    day1_lp_day = day1_lp.weekday()
    equi_shift = 3
    day1_shift = day1_day - equi_shift
    day1_lp_shift = day1_lp_day - equi_shift
    shift_index = day1_shift - day1_lp_shift
    if shift_index == 0:
        shift = 0
    elif abs(shift_index) <= 3:
        shift = shift_index
    else:
        shift_equi = (day1_day - equi_shift) - (day1_lp_day - equi_shift)
        if shift_equi > 0:
            shift = -1*(7-shift_equi)
        else:
            shift = 7+shift_equi
    #if abs(shift_index) == 6:
    #    shift = 1 #if -6
    #    if shift_index == 6:
    #        shift = -1
    #else:
    #    if not day1_day == day1_lp_day:
    #        if abs(day1_day - day1_lp_day) <= 3:
    #            shift = day1_day - day1_lp_day
    #        else:
    #            shift = abs(day1_day) + abs(day1_lp_day) - 3
    #        #print('shift'
    #        #print(shift, day1_lp, day1_lp_day, day1, day1_day
    #    else:
    #        shift = 0
    #        #print('no shift'

    if dict_to_shift:
        lp_day_index = shift_dict(dict_to_shift, shift)
        return lp_day_index
    return shift

def split_time(hrmin):
    try:
        hr, min = hrmin.split(':')
    except:
        hr = hrmin
        min = 0
    return int(hr), int(min)

def convert_hr_min_to_dt(hr=0, min=0):
    dt = None
    hr = int(hr)
    min = int(min)
    dtn = datetime.now()
    dt_hrmin = datetime(dtn.year, dtn.month, dtn.day, hr, min)
    return dt_hrmin

def adjust_intervals(input_dt, start_dt, end_dt):
    start_dt = datetime(input_dt.year, input_dt.month, input_dt.day, start_dt.hour, start_dt.minute)
    end_dt = datetime(input_dt.year, input_dt.month, input_dt.day, end_dt.hour, end_dt.minute)
    if start_dt > end_dt:
        if input_dt > start_dt:
            end_dt += timedelta(1)
        if input_dt < end_dt:
            start_dt -= timedelta(1)
    return start_dt, end_dt

def is_in_time_interval(input_dt, start_dt=None, end_dt=None, return_dict=False):
    output = False
    if isinstance(input_dt, int):
        input_dt = get_dt(input_dt)['utc']
    start_dt, end_dt = adjust_intervals(input_dt, start_dt, end_dt)
    if start_dt <= input_dt <= end_dt:
        output = True
    if return_dict:
        seconds_after_start = (input_dt - start_dt).total_seconds()
        seconds_before_end = (end_dt - input_dt).total_seconds()
        length = (end_dt - start_dt).total_seconds()
        output = {'is_in_interval':output, 'seconds_after_start':seconds_after_start, 'seconds_before_end':seconds_before_end, 'length':length}
    return output

def hours_between_datetimes(start_date,end_date):
    diff = end_date-start_date
    return diff.days*24+ diff.seconds //3600

def get_day_digit_from_string(dow):
    for x in range(0,7):
        if calendar.day_name[x] == dow:
            return x
    return None

HOLIDAYS = {
    "New Year's Day":{'specific_date':True, 'month':1, 'day':1, 'if_weekend_use_next_day':True},
    "President's Day":{'specific_date':False, 'month':2, 'day':3, 'dow':'Monday', 'if_weekend_use_next_day':False},
    "Memorial Day":{'specific_date':False, 'month':5, 'day':'last', 'dow':'Monday', 'if_weekend_use_next_day':False},
    "Independence Day":{'specific_date':True, 'month':7, 'day':4, 'if_weekend_use_next_day':True},
    "Labor Day":{'specific_date':False, 'month':9, 'day':1, 'dow':'Monday', 'if_weekend_use_next_day':False},
    #"Columbus Day":{'specific_date':False, 'month':10, 'day':2, 'dow':'Monday', 'if_weekend_use_next_day':False},
    "Veteran's Day":{'specific_date':True, 'month':11, 'day':11, 'if_weekend_use_next_day':False},
    "Thanksgiving":{'specific_date':False, 'month':11, 'day':4, 'dow':'Thursday', 'if_weekend_use_next_day':False},
    "Christmas":{'specific_date':True, 'month':12, 'day':25, 'if_weekend_use_next_day':True},
}
def generate_holidays(start_year=None, all=True):
    all_holidays = dates_key.objects.values_list('key_date', flat=True).filter(holiday_flag=True)
    if not start_year:
        start_year = date.today().year
    end_year = start_year
    if all:
        end_year = start_year + 20
    yrs = range(start_year, end_year)
    for yr in yrs:
        for holiday, atts in HOLIDAYS.iteritems():
            dk = dates_key()
            if atts['specific_date']:
                d = date(yr, atts['month'], atts['day'])
                dk.key_date = d
                dk.holiday_flag = True
                dk.holiday_name = holiday
            else:
                day_digit = get_day_digit_from_string(atts['dow'])
                x = 1
                last_day_of_month = get_last_day_of_month(yr,atts['month'])
                for day in range(1, last_day_of_month + 1):
                    d = date(yr, atts['month'], day)
                    if isinstance(atts['day'], int):
                        if day_digit == d.weekday():
                            if x == atts['day']:
                                d = date(yr, atts['month'], day)
                                dk.key_date = d
                                dk.holiday_flag = True
                                dk.holiday_name = holiday
                            x += 1
                    else:
                        if atts['day'] == 'last':
                            if day_digit == d.weekday():
                                if last_day_of_month - d.day < 7:
                                    d = date(yr, atts['month'], day)
                                    dk.key_date = d
                                    dk.holiday_flag = True
                                    dk.holiday_name = holiday
                                x += 1
            if dk.key_date and dk.key_date.weekday() in [5,6] and atts['if_weekend_use_next_day']:
                if dk.key_date.weekday() == 5:
                    dk.key_date += timedelta(2)
                elif dk.key_date.weekday() == 6:
                    dk.key_date += timedelta(1)
            if dk.key_date and dk.key_date not in all_holidays:
                dk.save()
    print('holidays added to dB')

def dow_date_finder(which_weekday_in_month=FIRST,day=MONDAY,month=JANUARY,year=2000):
    bom, days = monthrange(int(year), int(month))
    firstmatch = (day - bom) % 7 + 1
    return xrange(firstmatch, days+1, 7)[which_weekday_in_month]                        

def find_dt_of_daylight_savings_time(yr=date.today().year, interval=300):
    dst = {}
    spring = dow_date_finder(SECOND, SUNDAY, MARCH, yr)
    spring_dt = datetime(int(yr), 3, spring, 3, 0)
    dst['spring'] = spring_dt
    dst['spring_ts'] = get_ts(spring_dt)['utc']['input']
    dst['spring_adj'] = spring_dt + timedelta(0, 3600)
    dst['spring_adj_ts'] = get_ts(dst['spring_adj'])['utc']['input']
    dst['spring_doy'] = get_doy(spring_dt, False)
    dst['spring_range'] = range(dst['spring_ts'], dst['spring_adj_ts'], interval)
    fall = dow_date_finder(FIRST, SUNDAY, NOVEMBER, yr)
    fall_dt = datetime(int(yr), 11, fall, 3, 0)
    dst['fall'] = fall_dt
    dst['fall_ts'] = get_ts(fall_dt)['utc']['input']
    dst['fall_adj'] = fall_dt - timedelta(0, 3600)
    dst['fall_adj_ts'] = get_ts(dst['fall_adj'])['utc']['input']
    dst['fall_doy'] = get_doy(fall_dt, False)
    dst['fall_range'] = range(dst['fall_adj_ts'], dst['fall_ts'], interval)
    return dst

def get_ts_lists(ts_list, interval=300):
    ts_d = {'hourly':{}}
    iph = 3600/interval
    days = (ts_list[-1] - ts_list[0] + interval)/(3600*24)
    ts_d['ts_list'] = ts_list
    ts_d['hourly']['hour_of_day'] = range(0,24)*days
    ts_d['hour_of_day'] = [[r]*12 for r in range(0,24)]
    ts_d['hour_of_day'] = [item for sublist in ts_d['hour_of_day'] for item in sublist]*days #flatten initial list and get for num of days
    ts_d['dow'] = [get_dow(dow-interval) for dow in ts_list]
    ts_d['dow_name'] = [calendar.day_name[dow][:3] for dow in ts_d['dow']]
    ts_d['wknd'] = [is_weekend(dow-interval) for dow in ts_list]
    ts_d['wknd_name'] = ['Wknd' if x==1 else 'Not' for x in ts_d['wknd']]
    ts_d['month'] = [get_dt(dow-interval)['local'].month for dow in ts_list]
    ts_d['month_name'] = [calendar.month_name[dow][:3] for dow in ts_d['month']]
    ts_d['season69'] = ['S' if dow in [6,7,8,9] else 'W' for dow in ts_d['month']]
    ts_d['season510'] = ['S' if dow in [5,6,7,8,9,10] else 'W' for dow in ts_d['month']]
    return ts_d

def get_ts_list(start, end, interval=300):
    ts_list = []
    if not str(start).isdigit():
        start = get_ts(start)['local']['input']
    if not str(end).isdigit():
        end = get_ts(end)['local']['input']
    for i in range(start, end + interval, interval):
        ts_list.append(i)
    return ts_list

def splice_dst(a, ts_list, interval=300, preserve_true_values=True):
    iph = 3600/interval
    anew = a.copy()
    for y in range(get_dt(ts_list[0])['local'].year, get_dt(ts_list[-1])['local'].year + 1):
        spring_index = fall_index = None; l1 = np.array([]); l2 = np.array([]); l3 = np.array([]); spring_splice = np.array([]); fall_splice = np.array([])
        dst = find_dt_of_daylight_savings_time(y, interval)
        spring = dst['spring_ts']
        fall = dst['fall_ts']
        if spring in ts_list:
            spring_index = ts_list.index(spring)
        if fall in ts_list:
            fall_index = ts_list.index(fall)
        if spring_index:
            l1 = anew[:spring_index]
            l2 = anew[spring_index:]
            if spring_index > iph:
                spring_splice = l1[-1*iph:]
                if preserve_true_values:
                    spring_splice = np.array(iph*[0])
            else:
                spring_splice = l2[:iph]
        if spring_index and fall_index:
            l2 = anew[spring_index:fall_index]
        if fall_index:
            if not spring_index:
                l1 = anew[:fall_index]
            l3 = anew[fall_index+iph:]
            if preserve_true_values:
                gap = np.concatenate((anew[fall_index:fall_index+iph], np.array((len(l3)-iph)*[0])))
                l3 += gap
        anew =  np.concatenate([l1, spring_splice, l2, l3])
    return anew

def get_workdays(date1_str, date2_str):
    from pandas.tseries.holiday import USFederalHolidayCalendar
    from pandas.tseries.offsets import CustomBusinessDay
    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    print(len(pd.DatetimeIndex(start=date1_str,end=date2_str, freq=us_bd)))
    return len(pd.DatetimeIndex(start=date1_str,end=date2_str, freq=us_bd))






