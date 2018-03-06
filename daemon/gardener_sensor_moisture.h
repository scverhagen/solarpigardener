#pragma once

#define adc_ch_moisture ch1

#include "gardener_param.h"

float gardener_get_moisture_sensor_value();
float gardener_get_moisture_sensor_percentage( float adcval );
float gardener_get_moisture_sensor_percentage();


void update_params_moisture_sensor();

float gardener_get_moisture_sensor_value()
{
	float moisture_avalue = 0.0;
	moisture_avalue = analogRead(adc_ch_moisture);
	
	return moisture_avalue;
}

float gardener_get_moisture_sensor_percentage( float adcval )
{
	return (adcval * 100 / 32767.0);
}

float gardener_get_moisture_sensor_percentage()
{
	float adcval = 0.0;
	adcval = gardener_get_moisture_sensor_value();
	return (adcval * 100 / 32767.0);
}


void update_params_moisture_sensor()
{
    //write moisture sensor value param:
    float moisture_sensor_value = gardener_get_moisture_sensor_value();
    write_gardener_param("moisture_sensor_value", std::to_string(moisture_sensor_value));

    //write moisture sensor percentage param:
    float moisture_sensor_percentage = gardener_get_moisture_sensor_percentage();
    write_gardener_param("moisture_sensor_percentage", std::to_string(moisture_sensor_percentage));
}

void init_moisture_sensor()
{
    // set up parameters:
    clear_gardener_param("moisture_sensor_value");
    clear_gardener_param("moisture_sensor_percentage");
}