#define voltage_shutdown 11.0
#define charging_voltage_max 14.4
#define battery_voltage_max 12.6

#include "gardener_adc.h"
#include "gardener_param.h"
#include "gardener_fan.h"

float gardener_get_battery_voltage();
float gardener_get_battery_percentage();
void update_params_battery();
void do_battery_loop_checks();
void init_battery();

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

void update_params_battery()
{
    float voltage;
    float voltage_percentage;
    
    //write voltage param:
    voltage = gardener_get_battery_voltage();
    write_gardener_param("battery_voltage", std::to_string(voltage));

    //write voltage percentage param:
    voltage_percentage = gardener_get_battery_percentage();
    write_gardener_param("battery_percentage", std::to_string(voltage_percentage));
}

void do_battery_loop_checks()
{
    float voltage_percentage;
    voltage_percentage = gardener_get_battery_percentage();
    
    //turn fan on if battery percentage >= 100% (battery fully charged)
    if ( voltage_percentage >= 100 )
    {
            gardener_fan_on();
    } else {
            gardener_fan_off();
    }

}

void init_battery()
{
    // set up parameters:
    clear_gardener_param("battery_percentage");
    clear_gardener_param("battery_voltage");

}