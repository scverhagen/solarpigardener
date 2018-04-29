#pragma once

#include "gardener_fan.h"

#define pin_water_pump 2
#define gardener_water_duration 5

void init_water_pump(void);
void gardener_water_pump_on(int duration);
void gardener_water_pump_off();

void init_water_pump(void)
{
    pinMode(pin_water_pump, OUTPUT);
    digitalWrite(pin_water_pump, LOW);
}

void gardener_water_pump_on(int duration)
{
    //cout << "Pumping water for " << duration << " second(s)...";
    //cout.flush();
    
    // turn fan off before pumping water:
    gardener_fan_off();
    usleep(1000 * 1000 * .5);
            
    digitalWrite(pin_water_pump, HIGH);
    usleep(1000 * 1000 * duration);
    gardener_water_pump_off();
    cout << "done.\n";
}

void gardener_water_pump_off()
{
    digitalWrite(pin_water_pump, LOW);
}