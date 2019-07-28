from datetime import datetime
from datetime import timedelta
import time
import numpy as np

from app import config

DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
DAYS_IN_WEEK = 7

def get_today():
    now = datetime.now()
    return now.strftime("%A")    

def get_schedule():
    g_settings = config.loadSettings()
    num_days_to_water = int(g_settings.water_days_per_week)
    total_inches = int(g_settings.water_inches_per_week)
    water_mins_per_day = get_water_mins_per_day(g_settings)
    
    if num_days_to_water < 1 or num_days_to_water > DAYS_IN_WEEK:
        num_days_to_water = 7
        total_inches = 0
    
    water_per_day = round((total_inches / num_days_to_water),2)
    
    days_to_water = []
    for n in list(np.linspace(0, (DAYS_IN_WEEK - 1), num_days_to_water)):
        days_to_water.append(int(round(n)))
    
    routine = []
    for n in range(0,(DAYS_IN_WEEK)):
        thisday = DAY_NAMES[n]
        if n in days_to_water:
            routine.append([thisday, water_per_day, water_mins_per_day])
        else:
            routine.append([thisday, 0, 0])
    
    return routine
    
def get_water_mins_per_day(g_settings):
    mins_per_week = (float(g_settings.water_inches_per_week) / int(g_settings.water_days_per_week)) / float(g_settings.sprinkler_inches_per_minute)

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
    print(get_schedule())
   
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second
    dayname = get_today()
        
    while(1):
        old_year = year
        old_month = month
        old_day = day
        old_hour = hour
        old_minute = minute
        old_second = second
        
        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        dayname = get_today()
        
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
            on_time = datetime(year, month, day, int(g_settings.water_time_hour), 0)
            duration_mins = get_water_mins_per_day(g_settings)
            
            off_time = on_time + timedelta(minutes=duration_mins)
            print(on_time)
            print(duration_mins)
            print(off_time)
            #check_schedule(schedule=schedule, g_settings=g_settings, now=now)
        