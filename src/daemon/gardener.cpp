#include <iostream>
#include <fstream>
#include <unistd.h>
#include <string>
#include <sys/stat.h>
#include <wiringPi.h>

// adc
#include <ads1115.h>
#define MY_PINBASE 2222
#define ch0 MY_PINBASE + 0
#define ch1 MY_PINBASE + 1
#define ch2 MY_PINBASE + 2
#define ch3 MY_PINBASE + 3

// gpio pin configuration
#define pin_fan 0
#define pin_waterpump 2

// other parameters:
#define voltage_shutdown 11.0
#define charging_voltage_max 14.4
#define battery_voltage_max 12.6

using std::ifstream;
using std::ofstream;
using std::string;
using std::cout;
using std::flush;

int main(void);
int gardener_init();
int gardener_loop();
float gardener_get_battery_voltage();
float gardener_get_battery_percentage();

int write_param(string param_name, string param_data);
void clear_param(string param_name);
string cmd_get();
void cmd_clear();
void process_command(string gardener_cmd);

int main(void)
{
	cout << "Solar Pi Gardener\n";
	cout << "Background daemon\n";
	cout << "(C) Steve Verhagen 2018\n\n";
	cout << flush;

	// init routine
	gardener_init();
	cout << flush;
	
	gardener_loop();
	return 0;
}

int gardener_init()
{
	int dir_err;
	// init i2c adc interface:
	cout << "init i2c adc interface...\n";
	ads1115Setup(MY_PINBASE, 0x48);

	// init wiringPi (gpio library)
	cout << "init wiringPi GPIO library...\n";
	wiringPiSetup();

	// fan:
	pinMode(pin_fan, OUTPUT);
	digitalWrite(pin_fan, LOW);
	
	// water pump:
	pinMode(pin_waterpump, OUTPUT);
	digitalWrite(pin_waterpump, LOW);

	// create /tmp-gardener directory:
	dir_err = system("mkdir -p /tmp-gardener");
	// set permissions:
	dir_err = system("chmod -R 0777 /tmp-gardener");
	// clear left-over files:
	dir_err = system("rm /tmp-gardener/*");
	
	// set up parameters:
	clear_param("battery_percentage");
	clear_param("battery_voltage");
	dir_err = system("chmod -R 0777 /tmp-gardener");
	
	// init daemon cmd functionality:
	cmd_clear();
	
	cout << "init routine complete.\n";
	return 0;
}


int gardener_loop()
{
	string currentcmd;
	float voltage;
	float voltage_percentage;
	
    while (1)
    {   

	usleep(1000 * 1000);
		
	//write voltage param:
	voltage = gardener_get_battery_voltage();
	write_param("battery_voltage", std::to_string(voltage));

	//write voltage percentage param:
	voltage_percentage = gardener_get_battery_percentage();
	write_param("battery_percentage", std::to_string(voltage_percentage));

	//ongoing logic:
	//turn fan on if battery percentage >= 100% (battery fully charged)
	if ( voltage_percentage >= 100 )
	{
		digitalWrite(pin_fan, HIGH);
	} else {
		digitalWrite(pin_fan, LOW);
	}

	//get user command (if exists) and process it:
        currentcmd = cmd_get();
        if ( currentcmd != "0" )
        {
            cout << "Process command:  " << currentcmd << "\n";
			process_command(currentcmd);
        }		
		
		cout << flush;
		
    }
}

int write_param(string param_name, string param_data)
{
	std::ofstream ofs;
	ofs.open ("/tmp-gardener/gardener_" + param_name );
	//cout << "writing: " << ROVERSHELL_COMMAND;
	ofs << param_data;
	ofs.close();
	return 0;
}

void clear_param(string param_name)
{
	write_param(param_name, std::to_string(0));
	string param_path = "/tmp-gardener/gardener_" + param_name;
	chmod(param_path.c_str(), 777);
	return;
}

float gardener_get_battery_voltage()
{
	// int avalue = 0;
	float vin = 0.0;
	// float vout = 0.0;
	// float R1 = 30000.0;
	// float R2 = 7500;
	
	// avalue = analogRead(ch0);
	// vout = (avalue * 5.0) / 32767;
	// vin = vout / (R2/(R1+R2));
	// vin -= 1.6; // misc adjustment

	vin = (analogRead(ch0) / 32767.0 * 24.0) - 2.4;
	// voltage = analogRead(ch0) / 4.092;

	return vin;
}

float gardener_get_battery_percentage()
{
	float voltage = 0.0;
	float total_percentage = 0.0;
	float capacity_remaining = 0.0;
	float capacity_percentage = 0.0;
	
	float usable_capacity = battery_voltage_max - voltage_shutdown;
	voltage = gardener_get_battery_voltage();
	
	capacity_remaining = voltage - voltage_shutdown;

	total_percentage = voltage / battery_voltage_max * 100;
	capacity_percentage = capacity_remaining / usable_capacity * 100;
	return capacity_percentage;
}

void cmd_clear()
{
    ofstream ofs;
    ofs.open ("/tmp-gardener/gardener.cmd", std::ofstream::out | std::ofstream::trunc);
    ofs << 0;
    ofs.close();
	chmod("/tmp-gardener/gardener.cmd", 0777);
}

string cmd_get()
{
    ifstream ifs("/tmp-gardener/gardener.cmd");
    std::string currentcmd( (std::istreambuf_iterator<char>(ifs) ), (std::istreambuf_iterator<char>()) );
    ifs.close();
    cmd_clear();    
    return currentcmd;
}

void process_command(string gardener_cmd)
{
	// check for 'fanon' command:
	if ( gardener_cmd == "fanon" )
		digitalWrite(pin_fan, HIGH);
	
	if ( gardener_cmd == "fanoff" )
		digitalWrite(pin_fan, LOW);
	
}
