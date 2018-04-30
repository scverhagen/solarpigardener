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
    .soil_min_moisture_percentage = 20,
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
    float moisture_sensor_percentage = 0.00;

    if ( orig_moisture_sensor_percentage < thisplant->soil_min_moisture_percentage )
    {
        // soil moisture percentage is below minimum for specified plant--turn water on for set duration:
        cout    << "Soil moisture percentage (" << moisture_sensor_percentage 
                << "%) is below plants minimum soil percentage (" << thisplant->soil_min_moisture_percentage
                << "%).  Watering for " << gardener_water_duration << " seconds.  Will make up to 3 attempts.\n";
        cout.flush();
    
        int i = 0;
        for ( int i = 0; i < 3; ++i )
        {
            cout << "Attempt #" << (i + 1) <<  ":  Watering...;";
            cout.flush();
            gardener_water_pump_on(gardener_water_duration);
            cout << "done.\n";
            cout << "Waiting 5 seconds...";
            cout.flush();
            // wait 10 seconds for water to settle:
            usleep(1000 * ( (10) * 1000 ) );
            cout << "done.\n";
            cout.flush();
            // get new moisture reading
            moisture_sensor_percentage = gardener_get_moisture_sensor_percentage();
            if ( moisture_sensor_percentage > (orig_moisture_sensor_percentage + 5) )
            {
                cout << "Soil has been adequately watered.\n";
                cout.flush();
                return;
            } else {
                cout << "Soil is still DRY.  Will need another watering.\n";
                cout.flush();
            }
        }   
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