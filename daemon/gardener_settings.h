#pragma once

#include <string>
#include <fstream>
#include <string>
#include <sstream>
#include <sys/stat.h>

#include "gardener_param.h"

using std::string;
using std::cout;

// Default setting values:
int def_soil_min_moisture_percentage = 30;
int def_sched_hour = 5;
int def_water_duration = 90;

class gardener_settings_provider
{
    private:
        string settings_dir;

    public:
        float soil_min_moisture_percentage;
        int sched_hour;
        int water_duration;
    
    void load_settings()
    {
        // check if /etc/gardener/settings dir exists:
        struct stat info;
        if( stat( "/etc/gardener/settings", &info ) != 0 )
        {
            // The settings dir does not exist.  Create it:
            system("mkdir -p /etc/gardener/settings");
        }
        
        cout << "(gardener_settings) Loading settings.\n";
        // Load settings:
        soil_min_moisture_percentage = read_setting_int("soil_min_moisture_percentage", def_soil_min_moisture_percentage);
        sched_hour = read_setting_int("sched_hour", def_sched_hour);
        water_duration = read_setting_int("water_duration", def_water_duration);
        
        return;
    }
    
    string read_setting_str(string settingname, string defvalue)
    {
        cout << "(gardener_settings) read_setting_str: " << settingname << " val: ";
        string settingfilename = "/etc/gardener/settings/" + settingname;
        std::ifstream f1(settingfilename);
        if(!f1.is_open())
        {
            // File does not exist.  Create it and write default value for it.
            write_setting_str(settingname, defvalue);
            return defvalue;
        }
        
        std::stringstream buf;
        buf << f1.rdbuf();
        f1.close();
        
        cout << buf.str() << "\n";
        
        return buf.str();
    }
    
    int read_setting_int(string settingname, int defvalue)
    {
        cout << "(gardener_settings) read_setting_int: " << settingname << " value: ";
        string settingfilename = "/etc/gardener/settings/" + settingname;
        std::ifstream f1(settingfilename);
        if(!f1.is_open())
        {
            // File does not exist.  Create it and write default value for it.
            write_setting_int(settingname, defvalue);
            return defvalue;
        }
        
        std::stringstream buf;
        buf << f1.rdbuf();
        f1.close();
        
        int thisint;
        buf >> thisint;
        
        cout << thisint << "\n";
        
        return thisint;
    }    
    
    void write_setting_str(string settingname, string settingvalue)
    {
        string settingfilename = "/etc/gardener/settings/" + settingname;
        std::ofstream of1(settingfilename);
        of1 << settingvalue;
        of1.close();
        return;
    }
    
    void write_setting_int(string settingname, int settingvalue)
    {
        string settingfilename = "/etc/gardener/settings/" + settingname;
        std::ofstream of1(settingfilename);
        of1 << settingvalue;
        of1.close();
        return;
    }
    
    void init_params()
    {
        clear_gardener_param("soil_min_moisture_percentage");
        clear_gardener_param("sched_hour");
        clear_gardener_param("water_duration");
    }
    
    void update_params()
    {
        write_gardener_param("soil_min_moisture_percentage", std::to_string(soil_min_moisture_percentage));
        write_gardener_param("sched_hour", std::to_string(sched_hour));
        write_gardener_param("water_duration", std::to_string(water_duration));
    }
};


