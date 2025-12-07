// adapters.h
#pragma once
#include <string>
#include <vector>

struct NetworkAdapter {
    std::string name;
    std::string description;
    std::string ipAddress;
};

std::vector<NetworkAdapter> getNetworkAdapters();