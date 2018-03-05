#include <iostream>
#include <fstream>
#include <unistd.h>
#include <string>
#include <vector>
#include <sys/stat.h>
#include <wiringPi.h>

#include "gardener_cmd.h"
#include "gardener_battery.h"
#include "gardener_adc.h"
#include "gardener_water.h"
#include "gardener_fan.h"

using std::ifstream;
using std::ofstream;
using std::string;
using std::cout;
using std::flush;

int main(void);
int gardener_init();
int gardener_loop();

int write_gardener_param(string param_name, string param_data);
void clear_gardener_param(string param_name);

void process_gardener_command( gardener_command gc );

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

        // fan:
	init_fan();
	
	// water pump:
        init_water_pump();

        int dir_err;
	// create /tmp-gardener tmpfs mount point:
	dir_err = system("mkdir -p /tmp-gardener");
        dir_err = system("mount -t tmpfs -o size=32M tmpfs /tmp-gardener");
        
	// set permissions:
	dir_err = system("chmod -R 0777 /tmp-gardener");
	// clear left-over files:
	dir_err = system("rm /tmp-gardener/*");
	
	// set up parameters:
	clear_gardener_param("battery_percentage");
	clear_gardener_param("battery_voltage");
	dir_err = system("chmod -R 0777 /tmp-gardener");
	
	// init daemon cmd functionality:
	gardener_cmd_clear();
	
	cout << "init routine complete.\n";
	return 0;
}


int gardener_loop()
{
	gardener_command gc;
	float voltage;
	float voltage_percentage;
	
    while (1)
    {   

	usleep(1000 * 1000);
		
	//write voltage param:
	voltage = gardener_get_battery_voltage();
	write_gardener_param("battery_voltage", std::to_string(voltage));

	//write voltage percentage param:
	voltage_percentage = gardener_get_battery_percentage();
	write_gardener_param("battery_percentage", std::to_string(voltage_percentage));

	//ongoing logic:
	//turn fan on if battery percentage >= 100% (battery fully charged)
	if ( voltage_percentage >= 100 )
	{
                gardener_fan_on();
	} else {
                gardener_fan_off();
	}

	//get user command (if exists) and process it:
        gc = gardener_cmd_get();
        if ( gc.command_isblank == FALSE )
        {
            cout << "Process command:  " << gc.command << "\n";
            cout << "Arg count: " << gc.argcount << "\n";
            process_gardener_command(gc);
        }		
		
		cout << flush;
		
    }
}

int write_gardener_param(string param_name, string param_data)
{
	std::ofstream ofs;
	ofs.open ("/tmp-gardener/gardener_" + param_name );
	//cout << "writing: " << ROVERSHELL_COMMAND;
	ofs << param_data;
	ofs.close();
	return 0;
}

void clear_gardener_param(string param_name)
{
	write_gardener_param(param_name, std::to_string(0));
	string param_path = "/tmp-gardener/gardener_" + param_name;
	chmod(param_path.c_str(), 777);
	return;
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
    	
}
