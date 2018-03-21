#include <iostream>
#include <fstream>
#include <unistd.h>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <wiringPi.h>

#include "gardener_param.h"
#include "gardener_cmd.h"
#include "gardener_battery.h"
#include "gardener_adc.h"
#include "gardener_water.h"
#include "gardener_fan.h"
#include "gardener_sensor_moisture.h"
#include "gardener_plants.h"
#include "gardener_sched.h"

#define gardener_loop_delay 900 // 15 mins
#define gardener_plant plant_tomato // set plant type here


using std::ifstream;
using std::ofstream;
using std::string;
using std::cout;
using std::flush;

// functions:
int main(void);
int gardener_init();
int gardener_loop();
int write_gardener_param(string param_name, string param_data);
void clear_gardener_param(string param_name);
void process_gardener_command( gardener_command gc );

// globals:
plant thisplant;

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

int gardener_init()
{
    // init i2c adc interface:
    cout << "init i2c adc interface...\n";
    init_adc();

    // init wiringPi (gpio library)
    cout << "init wiringPi GPIO library...\n";
    wiringPiSetup();

    // init sections:
    init_battery();
    init_fan();
    init_water_pump();
    init_moisture_sensor();
    init_plants();

    int dir_err;
    // create /tmp-gardener tmpfs mount point:
    dir_err = system("mkdir -p /tmp-gardener");
    dir_err = system("umount /tmp-gardener");
    dir_err = system("mount -t tmpfs -o size=32M,mode=777 tmpfs /tmp-gardener");

    // set permissions:
    dir_err = system("chmod -R 0777 /tmp-gardener");
    // clear left-over files:
    dir_err = system("rm /tmp-gardener/*");
    
    // init daemon cmd functionality:
    gardener_cmd_clear();

    // make all params 777
    dir_err = system("chmod -R 777 /tmp-gardener");

    // populate thisplant:
    thisplant = gardener_plant;
    
    cout << "init routine complete.\n";
    return 0;
}


int gardener_loop()
{
    gardener_command gc;

    while (1)
    {   

        // update params:
        update_params_battery();
        update_params_moisture_sensor();
        update_params_plants(&thisplant);
        
	//ongoing loop logic:
	do_battery_loop_checks();
        
        //scheduler:
        gardener_check_schedule(&thisplant);
        
	//get user command (if exists) and process it:
        gc = gardener_cmd_get();
        if ( gc.command_isblank == FALSE )
        {
            cout << "Process command:  " << gc.command << "\n";
            cout << "Arg count: " << gc.argcount << "\n";
            process_gardener_command(gc);
        }		
		
        cout << flush;
                
        usleep(1000 * ( gardener_loop_delay * 1000 ) );
    }
}

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
}
