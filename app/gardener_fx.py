#!/usr/bin/python3

import math

def time_to_text(secs):
    
    secs = int(secs)
    
    s_min = 60
    s_hour = s_min * 60
    s_day = s_hour * 24
    
    ttt = ''
    
    num_days = math.floor(secs / s_day)
    if num_days == 1:
        ttt += str(num_days) + ' day'
        secs -= (num_days * s_day)
    elif num_days > 1:
        ttt += str(num_days) + ' days'
        secs -= (num_days * s_day)
        
    #print(secs)
    num_hours = math.floor(secs / s_hour)
    if num_hours > 0:
        if len(ttt) > 0:
            ttt += ', '
    if num_hours == 1:
        ttt += str(num_hours) + ' hour'
        secs -= (num_hours * s_hour)
    elif num_hours >= 2:
        ttt += str(num_hours) + ' hours'
        secs -= (num_hours * s_hour)        
        
    #print(secs)
    num_mins = math.floor(secs / s_min)
    if num_mins > 0:
        if len(ttt) > 0:
            ttt += ', '
    if num_mins == 1:
        ttt += str(num_mins) + ' minute'
        secs -= (num_mins * s_min)
    elif num_mins >= 2:
        ttt += str(num_mins) + ' minutes'
        secs -= (num_mins * s_min)     
        
    secs = round(secs, 0)
    if len(ttt) > 0:
        ttt += ', '
    if secs == 1:
        ttt += '1 second'
    else:
        ttt += str(secs) + ' seconds'

    return(ttt)

