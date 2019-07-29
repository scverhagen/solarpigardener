import datetime
import time
import numpy as np

from app import config
from app import gardener_fx as fx

DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
DAYS_IN_WEEK = 7

date_epoch = datetime.date(1970,1,1)

def get_dn(dt=0):
    if dt == 0:
        dt = datetime.datetime.today().date()    
    
    return (dt-date_epoch).days
        
def dn_to_date(dn):
    return date_epoch + datetime.timedelta(days=dn)

def get_dn_list(num_days=14, start_dn = 0):
    # get a list time stamps for the next X days, starting with Y
    if start_dn == 0:
        start_dn = get_dn()
    
    dn_list = []
    for x in range(num_days):
        dn_list.append(start_dn + (1 * x))
    
    return dn_list

def water_on_day(day_num, days_to_water):
    nd = int((DAYS_IN_WEEK / days_to_water))
    
    return ((day_num % nd) == 0)

def get_schedule(dn_list=0):
    g_settings = config.loadSettings()
    num_days_to_water = int(g_settings.water_days_per_week)
    total_inches = int(g_settings.water_inches_per_week)
    water_mins_per_day = round(get_water_mins_per_day(g_settings),2)
    
    if num_days_to_water < 1 or num_days_to_water > DAYS_IN_WEEK:
        num_days_to_water = 7
        total_inches = 0
    
    water_per_day = round((total_inches / num_days_to_water),2)
    
    if dn_list == 0:
        dn_list = get_dn_list()
    
    schedule = []
    for dn in dn_list:
        thisdate = dn_to_date(dn)
        water = water_on_day(dn, num_days_to_water)
        if water == True:
            schedule.append( [dn, thisdate.strftime('%A'), thisdate.strftime('%m-%d-%Y'), water_per_day, water_mins_per_day, fx.time_to_text(water_mins_per_day * 60)] )
        else:
            schedule.append( [dn, thisdate.strftime('%A'), thisdate.strftime('%m-%d-%Y'), 0, 0, ''] )
    
    return schedule
    
def get_water_mins_per_day(g_settings):
    mins_per_week = float(g_settings.water_inches_per_week) / float(g_settings.sprinkler_inches_per_minute)

    mins_per_day = 0
    if int(g_settings.water_days_per_week) != 0:
        mins_per_day = mins_per_week / int(g_settings.water_days_per_week)

    return mins_per_day

def check_schedule(schedule, g_settings, now):
    #on_time = datetime.
    #off_time
    return
    
def start_daemon():
    print('Solar Pi Gardener Scheduler Daemon')

    g_settings = config.loadSettings()
    schedule = get_schedule()
    
    print('Current Schedule:')
    print(schedule)
   
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    daynum = get_dn()
        
    while(1):
        old_year = year
        old_month = month
        old_day = day
        old_hour = hour
        old_minute = minute
        old_second = second
        
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        daynum = get_dn()
        
        c_year = (old_year == year) == False
        c_month = (old_month == month) == False
        c_day = (old_day == day) == False
        c_hour = (old_hour == hour) == False
        c_minute = (old_minute == minute) == False
        c_second = (old_second == second) == False
        
        time.sleep(1)
        if c_minute:
            # reload settings every minute:
            g_settings = config.loadSettings()
            schedule = get_schedule()
        
        if int(g_settings.enable_auto_watering) == 1:
            on_time = datetime.datetime(year, month, day, int(g_settings.water_time_hour), 0)
            duration_mins = get_water_mins_per_day(g_settings)
            off_time = on_time + datetime.timedelta(minutes=duration_mins)

            #td = datetime.fromtimestamp(td)
            #
            

            #print(datetime.fromtimestamp(dn_to_ts(18105)))
            #print(currentDate)
            print(on_time)
            #print(duration_mins)
            print(off_time)
            #check_schedule(schedule=schedule, g_settings=g_settings, now=now)
        