#include "gui.h"
#include "adapters.h"
#include <iostream>
int main()
{
    //Get info
    std::vector<NetworkAdapter> adapters = getNetworkAdapters();
    for(const auto& adapter : adapters) {
        std::cout << "Adapter: " << adapter.name 
                  << ", Description: " << adapter.description 
                  << ", IP: " << adapter.ipAddress << std::endl;
    }
    //Start GUI
    GUI window = GUI();
    window.setAdapters(adapters);
    window.run();

    return 0;
}
