#pragma once

#include "gardener_plants.h"
#include "gardener_water.h"

class plant
{
public:
    string name;
    float soil_min_moisture_percentage;
};

static struct plant plant_tomato = {
    .name = "tomato",
    .soil_min_moisture_percentage = 25,
};

// functions:
void gardener_plant_do_maint(plant* thisplant);
void init_plants();
void update_params_plants();

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

void init_plants()
{
    // set up parameters:
    clear_gardener_param("plant_name");
    clear_gardener_param("plant_soil_min_moisture_percentage");
}

void update_params_plants(plant * thisplant)
{
    //write gardener_plant_name:
    write_gardener_param("plant_name", thisplant->name);

    //write gardener_plant_soil_min_moisture_percentage:
    write_gardener_param("plant_soil_min_moisture_percentage", std::to_string(thisplant->soil_min_moisture_percentage));
}