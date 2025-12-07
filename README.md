# OpenWire
Cross platform lightweight network monitor with real-time per-process connection &amp; bandwidth tracking.

# Prepare the environment
Use MSYS2 if on Windows, and install gcc stack
```bash
pacman -Syu
pacman -Su
pacman -S mingw-w64-x86_64-toolchain mingw-w64-x86_64-cmake pkg-config
pacman -S mingw-w64-x86_64-gtk4
```

# Building
Create Build Folder
```bash
 mkdir build
 cd build
```
Build OpenWire
```bash
 cmake -G "MinGW Makefiles" ..
 mingw32-make
```
For Windows
```bash
OpenWire.exe
```

## Authors

- [@prottoy83](https://github.com/prottoy83)

