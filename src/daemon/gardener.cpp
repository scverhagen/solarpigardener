#include <iostream>
#include <fstream>
#include <unistd.h>
#include <string>
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

using std::ifstream;
using std::string;
using std::cout;
using std::flush;

int main(void);
int gardener_init();
int gardener_loop();

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

	// init wiringPi (gpio library)
	cout << "init wiringPi GPIO library...\n";
	wiringPiSetup();
	
	// init i2c adc interface:
	cout << "init i2c adc interface...\n";
	ads1115Setup(MY_PINBASE, 0x48);

	// fan:
	pinMode(pin_fan, OUTPUT);
	digitalWrite(pin_fan, LOW);
	
	// water pump:
	pinMode(pin_waterpump, OUTPUT);
	digitalWrite(pin_waterpump, LOW);
	
	cout << "init routine complete.\n";
	return 0;
}


int gardener_loop()
{
    string currentcmd;
    ifstream ifs;
    int data1;
	
    while (1)
    {        
		// writefile("/tmp/gardener_battery_voltage", gardener_get_battery_voltage());
        delay(500);
		data1 = analogRead(ch0);
        cout << "." << data1;
		cout << flush;
		
    }
    
}