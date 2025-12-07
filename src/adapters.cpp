#include "adapters.h"
#include <winsock2.h>
#include <iphlpapi.h>
#include <iostream>

#pragma comment(lib, "iphlpapi.lib")
#pragma comment(lib, "ws2_32.lib")

std::vector<NetworkAdapter> getNetworkAdapters() {
    std::vector<NetworkAdapter> adapters;
    
    DWORD dwSize = 0;
    DWORD dwRetVal = 0;

    if(GetAdaptersInfo(NULL, &dwSize) == ERROR_BUFFER_OVERFLOW) {
        PIP_ADAPTER_INFO pAdapterInfo = (IP_ADAPTER_INFO*)malloc(dwSize);
        if(pAdapterInfo == NULL) {
            std::cerr << "Memory allocation failed for IP_ADAPTER_INFO." << std::endl;
            return adapters;
        }

        if((dwRetVal = GetAdaptersInfo(pAdapterInfo, &dwSize)) == NO_ERROR) {
            PIP_ADAPTER_INFO pAdapter = pAdapterInfo;
            while (pAdapter) {
                NetworkAdapter adapter;
                adapter.name = pAdapter->AdapterName;
                adapter.description = pAdapter->Description;
                adapter.ipAddress = pAdapter->IpAddressList.IpAddress.String;
                adapters.push_back(adapter);
                pAdapter = pAdapter->Next;
            }
            free(pAdapterInfo);
            return adapters;
        }

        else{
            std::cerr << "GetAdaptersInfo failed with error: " << dwRetVal << std::endl;
        }

        free(pAdapterInfo);
    }
    else {
        std::cerr << "Failed to get adapter info size." << std::endl;
    }

    return adapters;
}