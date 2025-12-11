#include "process.h"
#include <vector>
#include <string>
#include <windows.h>
#include <iostream>
#include <tchar.h>
#include <psapi.h>

std::vector<processInfo>  processList(){
    std::vector<processInfo> list;

    DWORD aProcess[1024], cbNeeded, cProcess;

    if( !EnumProcesses( aProcess, sizeof(aProcess), &cbNeeded) ){
        std::cerr << "Error! Halting" << std::endl;
        return list;
    }

    cProcess = cbNeeded / sizeof(DWORD);

    for(unsigned int i=0;i<cProcess;i++){
        if(aProcess[i] != 0)
        {
            TCHAR szProcessName[MAX_PATH] = TEXT("<Unnamed Process>");

            HANDLE hProcess = OpenProcess( PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, false, aProcess[i]);

            if(hProcess != NULL){
                HMODULE hMod;
                DWORD cbNeeded;

                if(EnumProcessModules( hProcess, &hMod, sizeof(hMod), &cbNeeded)){
                    GetModuleBaseName( hProcess, hMod, szProcessName, sizeof(szProcessName)/ sizeof(TCHAR));
                } 

                
                #ifdef UNICODE
                    std::wstring ws(szProcessName);
                    std::string processName(ws.begin(), ws.end());
                #else
                    std::string processName(szProcessName);
                #endif

                list.push_back({processName, static_cast<int>(aProcess[i])});

                CloseHandle(hProcess);
            }
        }
    }

    return list;
}