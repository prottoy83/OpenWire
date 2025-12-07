# OpenWire

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**OpenWire** is a lightweight, cross-platform open-source network monitoring tool for Windows, inspired by GlassWire. It allows you to view active TCP/UDP connections, track bandwidth usage per process, and monitor your network in real-time through a simple GTK3 GUI.

> 📸 GUI screenshots will be available after testing on platforms with GTK3 support. See [docs/SCREENSHOTS.md](docs/SCREENSHOTS.md) for details.

## Features

- 🔍 **Active Connection Monitoring**: View all active TCP and UDP connections in real-time
- 📊 **Per-Process Bandwidth Tracking**: Monitor upload/download bandwidth usage for each process
- 📈 **Network Statistics**: Track total bytes sent/received, packets, errors, and drops
- 🖥️ **Simple GTK3 Interface**: Clean, intuitive GUI for easy monitoring
- 🔄 **Real-Time Updates**: Automatic refresh every 2 seconds
- 🌐 **Cross-Platform**: Works on Windows, Linux, and macOS

## Installation

### Prerequisites

- Python 3.7 or higher
- GTK3 runtime (for GUI)

#### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Install GTK3 runtime:
   - Download from [GTK for Windows](https://www.gtk.org/docs/installations/windows)
   - Or use MSYS2: `pacman -S mingw-w64-x86_64-gtk3`

#### Linux

Most Linux distributions come with GTK3 pre-installed. If not:

```bash
# Ubuntu/Debian
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Fedora
sudo dnf install python3-gobject gtk3

# Arch Linux
sudo pacman -S python-gobject gtk3
```

#### macOS

```bash
brew install pygobject3 gtk+3
```

### Install OpenWire

```bash
# Clone the repository
git clone https://github.com/prottoy83/OpenWire.git
cd OpenWire

# Install dependencies
pip install -r requirements.txt

# Install OpenWire
pip install -e .
```

## Usage

### GUI Mode (Default)

Simply run:

```bash
openwire
```

Or from the source directory:

```bash
python -m openwire.main
```

### Command Line Options

```bash
openwire --version    # Show version information
openwire --help       # Show help message
```

## Features in Detail

### Active Connections

The **Active Connections** tab displays:
- Process ID (PID)
- Process name
- Connection type (TCP/UDP)
- Local address and port
- Remote address and port
- Connection status (ESTABLISHED, LISTEN, TIME_WAIT, etc.)

### Bandwidth Usage

The **Bandwidth Usage** tab shows:
- Process ID (PID)
- Process name
- Upload speed (bytes/second)
- Download speed (bytes/second)
- Total bandwidth (upload + download)

Processes are sorted by total bandwidth usage (highest first), and only active processes are displayed.

### Network Statistics

The statistics bar at the top shows:
- Total bytes sent and received
- Total packets sent and received
- Network errors and drops (if any)

## Requirements

- **PyGObject** >= 3.42.0 - Python bindings for GTK3
- **psutil** >= 5.9.0 - Cross-platform process and system utilities

## Permissions

On Linux and macOS, you may need elevated privileges to view all network connections:

```bash
sudo openwire
```

On Windows, run the application as Administrator for full access to all connections.

## Development

### Project Structure

```
OpenWire/
├── openwire/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Main entry point
│   ├── network_monitor.py   # Core network monitoring logic
│   └── gui.py               # GTK3 GUI implementation
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup configuration
├── LICENSE                  # MIT License
└── README.md               # This file
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Add firewall notifications
- [ ] Implement traffic alerts and thresholds
- [ ] Add bandwidth usage graphs and historical data
- [ ] Support for custom refresh intervals
- [ ] Export connection/bandwidth data to CSV
- [ ] System tray integration
- [ ] Dark mode theme

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [GlassWire](https://www.glasswire.com/)
- Built with [GTK](https://www.gtk.org/) and [psutil](https://github.com/giampaolo/psutil)

## Disclaimer

OpenWire is a monitoring tool for educational and legitimate system administration purposes. Users are responsible for ensuring they comply with applicable laws and regulations when monitoring network traffic.

## Support

If you encounter any issues or have questions:
- Open an issue on [GitHub](https://github.com/prottoy83/OpenWire/issues)
- Check the [documentation](https://github.com/prottoy83/OpenWire/wiki)

---

Made with ❤️ by the OpenWire community
