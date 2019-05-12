import os
import gpiozero

def gardener_init():
    print("Solar Pi Gardener")
    print("Background daemon")
    print("(C) Steve Verhagen 2019")

    # init i2c adc interface:
    print ("init i2c adc interface...")
    init_adc();
    
    if os.getuid() !=0:
        print("This program must run as root!")
        return 1;

    # init wiringPi (gpio library)
    print("init wiringPi GPIO library...")
    wiringPiSetup();

    # tick functionality:
    tick_sec = 0;
    tick_min = 0;
    
    # init_settings:
    gardener_settings.load_settings();
    gardener_settings.init_params();
    
    # init sections:
    init_battery()
    init_fan()
    init_water_pump()
    init_moisture_sensor()

    # create /tmp-gardener tmpfs mount point:
    os.system("mkdir -p /tmp-gardener")
    os.system("umount /tmp-gardener")
    os.system("mount -t tmpfs -o size=32M,mode=777 tmpfs /tmp-gardener")

    # set permissions:
    os.system("chmod -R 0777 /tmp-gardener")
    os.system("chmod 0775 /var/log/syslog")
    
    # clear left-over files:
    os.system("rm /tmp-gardener/*")
    
    # init daemon cmd functionality:
    gardener_cmd_clear()

    # make all params 777
    os.system("chmod -R 777 /tmp-gardener")

    print("init routine complete.")


def gardener_loop():
    gc = gardener_command()

    while (1):
        #update params:
        update_params_battery();
        if ( tick_min == 0 and tick_sec == 0 ):
            update_params_moisture_sensor()
        
        gardener_settings.update_params()
        
	    #ongoing loop logic:
	    #do_battery_loop_checks()
        
        #scheduler:
        gardener_check_schedule()
        
	    #get user command (if exists) and process it:
        gc = gardener_cmd_get()
        if ( gc != None ):
            print("Process command:  " + gc.command)
            print("Arg count: " + gc.argcount)
            process_gardener_command(gc)

def process_gardener_command(gc):
    args = gc.split()
    largs = gc.lower().split()
    
    if largs[0] == 'water_pump_on':
        gardener_water_pump_on( args[1] )
    elif largs[0] == "system_reboot":
        print('Rebooting system...')
        os.system("reboot")
    elif largs[0] == "system_poweroff":
        print('Powering system OFF...')
        os.system("poweroff");
    elif largs[0] == "ping":
        print('ping')
    elif largs[0] == "check_moisture":
        update_params_moisture_sensor()
        print("Moisture param updated.")
    elif largs[0] == 'do_maint':
        print("Forcing maintenance.")
        gardener_do_maint();
    elif largs[0] == "kill_process":
        print("Killing Process.")
        return 1

if __name__ == '__main__':
    if gardener_init() == 0:
        gardener_loop();
    else:
        print('Init failed.  Daemon not started.')