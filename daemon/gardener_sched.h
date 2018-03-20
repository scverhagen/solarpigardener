#include <time.h>

#include "gardener_plants.h"

static int lastQ;

void gardener_check_schedule( plant * thisplant );

void gardener_check_schedule( plant * thisplant )
{
    time_t rawtime;
    struct tm * timeinfo;

    time (&rawtime);
    timeinfo = localtime (&rawtime);
    
    // check to see if the time is 00:00, 06:00, 12:00, or 18:00:
    bool isQD = ( (timeinfo->tm_hour % 6) == 0 );
    if ( isQD = FALSE )
        return;
    
    int thisQ = (timeinfo->tm_hour / 6) + 1;
    
    // make sure that this is a new quarter day:
    if ( thisQ == lastQ )
        return;

    // it is the first "tick" since the latest quarter hour
    // do plant maintenance task:
    cout << "New scheduling quarter entered:  "  << thisQ << " from " << lastQ << ".\n";
    lastQ = thisQ;
    gardener_plant_do_maint(thisplant);
    
}