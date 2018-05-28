#pragma once

#include "gardener_plants.h"
#include "gardener_water.h"
#include "gardener_sensor_moisture.h"

class plant
{
public:
    string name;
    float soil_min_moisture_percentage;
    int sched_hour;
    int water_duration;
};

static struct plant plant_tomato = {
    .name = "tomato",
    .soil_min_moisture_percentage = 35,
    .sched_hour = 5,
    .water_duration = 120,
};

// functions:
void gardener_plant_do_maint(plant* thisplant);
void init_plants();
void update_params_plants();

/*
void gardener_plant_do_maint(plant* thisplant)
{
    // check moisture percentage vs. min plant moisture param:
    float moisture_sensor_percentage = gardener_get_moisture_sensor_percentage();
    if ( moisture_sensor_percentage < thisplant->soil_min_moisture_percentage )
    {
        // soil moisture percentage is below minimum for specified plant--turn water on for set duration:
        cout    << "Soil moisture percentage (" << moisture_sensor_percentage 
                << "%) is below plants minimum soil percentage (" << thisplant->soil_min_moisture_percentage
                << "%).  Watering for " << gardener_water_duration << " seconds.\n";
        cout.flush();
        gardener_water_pump_on(gardener_water_duration);
    }
}
 */

void gardener_plant_do_maint(plant* thisplant)
{
    // check moisture percentage vs. min plant moisture param:
    float orig_moisture_sensor_percentage = gardener_get_moisture_sensor_percentage();
    
    if ( orig_moisture_sensor_percentage < thisplant->soil_min_moisture_percentage )
    {
        // soil moisture percentage is below minimum for specified plant--turn water on for set duration:
        cout    << "(gardener_plant_do_maint) Soil moisture percentage (" << orig_moisture_sensor_percentage 
                << "%) is below plant's minimum soil percentage (" << thisplant->soil_min_moisture_percentage
                << "%).  Watering for " << thisplant->water_duration << " seconds.\n";
        cout.flush();
    
        gardener_water_pump_on(gardener_water_duration);
        cout << "done.\n";
        cout.flush();
        update_params_moisture_sensor();
    }
    else {
        // moisture reading is too high for watering...skip:
        cout    << "(gardener_plant_do_maint) Soil moisture percentage (" << orig_moisture_sensor_percentage 
                << "%) is ABOVE the plant's minimum soil percentage (" << thisplant->soil_min_moisture_percentage
                << "%).  skipping...\n";
        cout.flush();
    }
}

void init_plants()
{
    // set up parameters:
    clear_gardener_param("plant_name");
    clear_gardener_param("plant_soil_min_moisture_percentage");
    clear_gardener_param("plant_sched_hour");
    clear_gardener_param("plant_water_duration");
}

void update_params_plants(plant * thisplant)
{
    //write gardener_plant_name:
    write_gardener_param("plant_name", thisplant->name);

    //write gardener_plant_soil_min_moisture_percentage:
    write_gardener_param("plant_soil_min_moisture_percentage", std::to_string(thisplant->soil_min_moisture_percentage));
 
    //write gardener_plant_sched_hour:
    write_gardener_param("plant_sched_hour", std::to_string(thisplant->sched_hour));
    
    //write gardener_plant_water_duration:
    write_gardener_param("plant_water_duration", std::to_string(thisplant->water_duration));
}