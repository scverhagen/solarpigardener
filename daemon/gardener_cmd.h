#pragma once

#include <string>
#include <iostream>
#include <fstream>
#include <sstream>
#include <sys/stat.h>
#include <vector>

using std::ifstream;
using std::ofstream;
using std::string;
using std::cout;
using std::vector;

class  gardener_command
{
public:
    bool command_isblank;
    string command;
    int argcount;
    vector<string> args;
    //string args[];
};

gardener_command gardener_cmd_get();
void gardener_cmd_clear();

void gardener_cmd_clear()
{
    ofstream ofs;
    
    // clear gardener.cmd:
    ofs.open ("/tmp-gardener/gardener.cmd", std::ofstream::out | std::ofstream::trunc);
    ofs << 0;
    ofs.close();
    chmod("/tmp-gardener/gardener.cmd", 777);
    
    // clear gardener.cmdargcount:
    ofs.open ("/tmp-gardener/gardener.cmdargcount", std::ofstream::out | std::ofstream::trunc);
    ofs << 0;
    ofs.close();
    chmod("/tmp-gardener/gardener.cmdargcount", 777);
    
    // clear gardener.cmdargs:
    ofs.open ("/tmp-gardener/gardener.cmdargs", std::ofstream::out | std::ofstream::trunc);
    ofs << 0;
    ofs.close();
    chmod("/tmp-gardener/gardener.cmdargs", 777);
    
}

gardener_command gardener_cmd_get()
{
    gardener_command gc;
    
    // define buffer stringstream (to be cleared and reused throughout function:
    std::stringstream buffer;
        
    // read next gardener command
    std::ifstream incmd("/tmp-gardener/gardener.cmd");
    buffer << incmd.rdbuf();
    std::string gardener_cmd_string(buffer.str());
    incmd.close();
    if ( gardener_cmd_string == "0" )
    {
        // gardener command is blank
        gc.command_isblank = true;
        return gc;
    }
    
    // a command exists.
    gc.command_isblank = false;
    gc.command = gardener_cmd_string;
    //cout << gc.command;
    
    // clear stringstream buffer
    buffer.str("");
    
    // get command argument count:
    std::ifstream inargc("/tmp-gardener/gardener.cmdargcount");
    buffer << inargc.rdbuf();
    std::string gardener_cmd_argcount_string(buffer.str());
    inargc.close();
    gc.argcount = atoi(gardener_cmd_argcount_string.c_str());


    if ( gc.argcount != 0 )
    {
        // read arguments and populate gc args array of strings
        string args[gc.argcount];
        std::ifstream inargs("/tmp-gardener/gardener.cmdargs");
        int i = 0;
        while ( i < gc.argcount )
        {
            getline(inargs, args[i]);
            gc.args.push_back( args[i] );
            i++;
        }
        inargs.close();

    }

    gardener_cmd_clear();
    
    return gc;
}