#include <time.h>

#include "gardener_settings.h"
void gardener_do_maint(gardener_settings_provider* gardener_settings);


static int lastHour;

void gardener_check_schedule( gardener_settings_provider * gardener_settings );

void gardener_check_schedule( gardener_settings_provider * gardener_settings )
{
    time_t rawtime;
    struct tm * timeinfo;

    time (&rawtime);
    timeinfo = localtime (&rawtime);
    
    int thisHour = timeinfo->tm_hour;
    
    // make sure that this is a new hour:
    if ( thisHour == lastHour )
        return;

    // it is the first "tick" since the latest quarter day
    // do plant maintenance task:
    cout << "(gardener_check_schedule) New hour entered:  "  << thisHour << ":00 from " << lastHour << ":00.\n";
    lastHour = thisHour;
    if (thisHour == gardener_settings->sched_hour)
    {
        cout << "(gardener_check_schedule) It's " << thisHour << ":00.  Watering.\n";
        gardener_do_maint(gardener_settings);
    }
    
}

void gardener_do_maint(gardener_settings_provider* gardener_settings)
{
    // check moisture percentage vs. min plant moisture param:
    float orig_moisture_sensor_percentage = gardener_get_moisture_sensor_percentage();
    
    if ( orig_moisture_sensor_percentage < gardener_settings->soil_min_moisture_percentage )
    {
        // soil moisture percentage is below minimum for specified plant--turn water on for set duration:
        cout    << "(gardener_do_maint) Soil moisture percentage (" << orig_moisture_sensor_percentage 
                << "%) is below plant's minimum soil percentage (" << gardener_settings->soil_min_moisture_percentage
                << "%).  Watering for " << gardener_settings->water_duration << " seconds.\n";
        cout.flush();
    
        gardener_water_pump_on(gardener_settings->water_duration);
        cout << "done.\n";
        cout.flush();
        update_params_moisture_sensor();
    }
    else {
        // moisture reading is too high for watering...skip:
        cout    << "(gardener_do_maint) Soil moisture percentage (" << orig_moisture_sensor_percentage 
                << "%) is ABOVE the minimum soil percentage (" << gardener_settings->soil_min_moisture_percentage
                << "%).  skipping...\n";
        cout.flush();
    }
}