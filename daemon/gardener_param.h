#pragma once

#include <string>

using std::string;

int write_gardener_param(string param_name, string param_data);
void clear_gardener_param(string param_name);

int write_gardener_param(string param_name, string param_data)
{
	std::ofstream ofs;
	ofs.open ("/tmp-gardener/gardener_" + param_name );

	ofs << param_data;
	ofs.close();
	return 0;
}

void clear_gardener_param(string param_name)
{
    write_gardener_param(param_name, std::to_string(0));
    string param_path = "/tmp-gardener/gardener_" + param_name;
    chmod(param_path.c_str(), 777);
    return;
}