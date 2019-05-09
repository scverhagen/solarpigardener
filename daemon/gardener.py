import gpiozero

gardener_tick_min_max = 60 // 1 hour (in minutes)

import os

// functions:
int main(void);
int gardener_init();
int gardener_loop();
int write_gardener_param(string param_name, string param_data);
void clear_gardener_param(string param_name);
void process_gardener_command( gardener_command gc );

// globals:
gardener_settings_provider gardener_settings;
//plant thisplant;
long tick_sec;
long tick_min;

int main(void)
{
    cout << "Solar Pi Gardener\n";
    cout << "Background daemon\n";
    cout << "(C) Steve Verhagen 2018\n\n";
    if ( getuid() !=0 )
    {
            cout << "ERROR:  This program must run as root!\n";
            return 1;
    }

    cout << flush;

    // init routine
    gardener_init();
    cout << flush;

    gardener_loop();
    return 0;
}

def gardener_init():
    # init i2c adc interface:
    print ("init i2c adc interface...")
    init_adc();

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
        gardener_check_schedule(gardener_settings)
        
	    #get user command (if exists) and process it:
        gc = gardener_cmd_get()
        if ( gc.command_isblank == False ):
            print("Process command:  " + gc.command)
            print("Arg count: " + gc.argcount)
            process_gardener_command(gc)
                
        #usleep(1000 * ( (1) * 1000 ) );
        
        tick_sec += 1
        if ( tick_sec == 59 ):
            tick_sec = 0;
            tick_min += 1
        if ( tick_min == gardener_tick_min_max ):
            tick_min = 0
        cout.flush()

void process_gardener_command( gardener_command gc )
{
    // check for 'water_pump_on' command:
    if ( gc.command == "water_pump_on" )
    {
        string arg1 = gc.args.front();
        gardener_water_pump_on( atoi(arg1.c_str() ) );
    }
    
    // check for 'system_reboot' command:
    if ( gc.command == "system_reboot" )
    {
        int dir_err;
        cout << "Rebooting system...\n";
        cout.flush();
        dir_err = system("reboot");
    }

    // check for 'system_poweroff' command:
    if ( gc.command == "system_poweroff" )
    {
        int dir_err;
        cout << "Powering system OFF...\n";
        cout.flush();
        dir_err = system("poweroff");
    }
 
    // check for 'ping' command:
    if ( gc.command == "ping" )
    {
        int dir_err;
        cout << "ping\n";
    }
    
    // check for 'check_moisture' command:
    if ( gc.command == "check_moisture" )
    {
        int dir_err;
        update_params_moisture_sensor();
        cout << "Moisture param updated.\n";
    }

    // check for 'do_maint' command:
    if ( gc.command == "do_maint" )
    {
        cout << "Forcing maintenance.\n";
        cout.flush();
        gardener_do_maint(&gardener_settings);
    }

    
    // check for 'kill_process' command:
    if ( gc.command == "kill_process" )
    {
        int dir_err;
        cout << "Killing Process.\n";
        exit(1);
    }
}
