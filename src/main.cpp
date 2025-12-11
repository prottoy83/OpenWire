#include "gui.h"
#include "adapters.h"
#include "process.h"
#include <iostream>

int main()
{
    // Gather data
    std::vector<NetworkAdapter> adapters = getNetworkAdapters();
    std::vector<processInfo> processes = processList();

    // Start GUI
    GUI window = GUI();
    window.setAdapters(adapters);
    window.setProcesses(processes);
    window.run();

    return 0;
}
