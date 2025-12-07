# OpenWire Examples

This directory contains example scripts demonstrating how to use OpenWire programmatically.

## Running Examples

### Method 1: Using the installed package

If you've installed OpenWire using `pip install -e .`, you can run examples directly:

```bash
python3 examples/monitor_example.py
```

### Method 2: Using PYTHONPATH

If you haven't installed the package, set PYTHONPATH to the repository root:

```bash
PYTHONPATH=/path/to/OpenWire python3 examples/monitor_example.py
```

## Available Examples

### monitor_example.py

A simple script that demonstrates:
- Creating a NetworkMonitor instance
- Collecting network statistics
- Counting active connections (TCP/UDP)
- Tracking bandwidth usage per process
- Displaying formatted output

The script runs for about 10 seconds, collecting data every 2 seconds.

## Creating Your Own Scripts

Here's a minimal example of using OpenWire in your own scripts:

```python
from openwire.network_monitor import NetworkMonitor

# Create a monitor instance
monitor = NetworkMonitor()

# Get network statistics
stats = monitor.get_network_stats()
print(f"Bytes sent: {monitor.format_bytes(stats['bytes_sent'])}")

# Get active connections
connections = monitor.get_connections()
print(f"Active connections: {len(connections)}")

# Get bandwidth usage (requires two samples)
bandwidth1 = monitor.get_bandwidth_usage()
time.sleep(1)
bandwidth2 = monitor.get_bandwidth_usage()

# Display processes using bandwidth
for pid, data in bandwidth2.items():
    if data['total'] > 0:
        print(f"{data['name']}: {monitor.format_bandwidth(data['total'])}")
```

For more details, see the [main README](../README.md).
