#pragma once
#include<vector>
#include<string>
struct processInfo{
    std::string processName;
    int pid;
};

std::vector<processInfo> processList();