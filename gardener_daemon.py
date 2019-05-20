#!/usr/bin/python3

import os
import sys
import platform
import time

if os.getuid() !=0:
    print("This program must run as root!")
    exit()

import gardener_controls
import gardener_fifo # this needs root
import gardener_fx

is_pi = (platform.machine() == 'armv7l')

if is_pi:
    import gpiozero

command_fifo = gardener_fifo.command_fifo()
status_fifo = gardener_fifo.status_fifo()

control_waterpump = gardener_controls.water_pump()
#sensor_moisture = gardener_controls.moisture_sensor()

status_dict = {'bat_voltage': 0, 'bat_status':'na', 'moisture_reading': 0, 'uptime': 0}

start_time = time.time()

def gardener_init():
    print("Solar Pi Gardener")
    print("Background daemon")
    print("(C) Steve Verhagen 2019")

    # init i2c adc interface:
    #print ("init i2c adc interface...")
    #init_adc();
   
    # init_settings:
#    gardener_settings.load_settings();
#    gardener_settings.init_params();

    print("init routine complete.")
    return 0

last_time = 0
def gardener_loop():
    while (1):
        new_time = time.time()
    
        #get user command (if exists) and process it:        
        gc = command_fifo.checkforcommand()
        
        if ( gc != '' ):
            print("Process command:  " + gc)
            process_gardener_command(gc)
            
        # update status
        status_dict['uptime'] = round(new_time - start_time, 1)
        status_fifo.setstatusdict(status_dict)
        
        last_time = new_time
        time.sleep(1)

def process_gardener_command(gc):
    lcmd = gc.lower()
    args = gc.split()
    argc = len(args)
    largs = lcmd.split()
    
    if largs[0] == 'water_pump_on':
        control_waterpump.On()
    elif largs[0] == "system_reboot":
        print('Rebooting system...')
        os.system("reboot")
    elif largs[0] == "system_poweroff":
        print('Powering system OFF...')
        os.system("poweroff");
    elif largs[0] == "ping":
        print('ping')
    elif largs[0] == "check_moisture":
        #update_params_moisture_sensor()
        print("Moisture param updated.")
    elif largs[0] == 'force_water':
        print("Forcing maintenance.")
        #gardener_do_maint();
    elif largs[0] == "kill_process":
        print("Killing Process.")
        sys.exit(1)
    elif largs[0] == 'water_for':
        if argc > 1:
            duration = largs[1]
            control_waterpump.water_for(int(duration))

if __name__ == '__main__':
    if gardener_init() == 0:
        gardener_loop();
    else:
        print('Init failed.  Daemon not started.')