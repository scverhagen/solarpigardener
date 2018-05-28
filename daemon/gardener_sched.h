#include <time.h>

#include "gardener_plants.h"

static int lastHour;

void gardener_check_schedule( plant * thisplant );

void gardener_check_schedule( plant * thisplant )
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
    if (thisHour == thisplant->sched_hour)
    {
        cout << "(gardener_check_schedule) It's " << thisHour << ":00.  Watering " << thisplant->name << " plant.\n";
        gardener_plant_do_maint(thisplant);
    }
    
    
}