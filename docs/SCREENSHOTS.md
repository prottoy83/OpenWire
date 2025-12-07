# OpenWire Screenshots

This document will contain screenshots of OpenWire in action once the GUI is tested on a system with GTK3 support.

## Planned Screenshots

1. **Main Window Overview** - Full application window showing the network monitoring interface
2. **Active Connections Tab** - List of TCP/UDP connections with process details
3. **Bandwidth Usage Tab** - Real-time bandwidth usage per process
4. **Network Statistics Bar** - Overall network statistics display

## Testing on Windows

To test OpenWire on Windows with GTK3:

1. Install Python 3.7+ from python.org
2. Install GTK3 runtime:
   - Download MSYS2 from https://www.msys2.org/
   - Install GTK3: `pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python-gobject`
3. Install OpenWire: `pip install -e .`
4. Run: `openwire`

## Testing on Linux

On most modern Linux distributions:

```bash
# Install dependencies
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Install OpenWire
pip install -e .

# Run
openwire
```

---

*Screenshots will be added after testing on appropriate platforms with GUI support.*
