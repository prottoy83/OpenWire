#!/usr/bin/env python3
"""
Example script showing how to use OpenWire programmatically
"""

from openwire.network_monitor import NetworkMonitor
import time
import sys
import os

# Add parent directory to path to import openwire
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def monitor_example():
    """Example of using NetworkMonitor programmatically"""
    monitor = NetworkMonitor()
    
    print("OpenWire Network Monitor - Programmatic Example")
    print("=" * 60)
    
    # Monitor for 10 seconds
    for i in range(5):
        print(f"\n[Update {i+1}/5]")
        
        # Get and display network stats
        stats = monitor.get_network_stats()
        print(f"Network: {monitor.format_bytes(stats['bytes_sent'])} sent, "
              f"{monitor.format_bytes(stats['bytes_recv'])} received")
        
        # Get connections count
        connections = monitor.get_connections()
        tcp_count = sum(1 for c in connections if c['type'] == 'TCP')
        udp_count = sum(1 for c in connections if c['type'] == 'UDP')
        print(f"Connections: {tcp_count} TCP, {udp_count} UDP")
        
        # Get bandwidth usage
        bandwidth = monitor.get_bandwidth_usage()
        active = [(pid, data) for pid, data in bandwidth.items() if data['total'] > 0]
        
        if active:
            # Sort by total bandwidth
            active.sort(key=lambda x: x[1]['total'], reverse=True)
            top_process = active[0]
            print(f"Top bandwidth user: {top_process[1]['name']} "
                  f"({monitor.format_bandwidth(top_process[1]['total'])})")
        else:
            print("No active bandwidth detected")
        
        if i < 4:  # Don't sleep after last iteration
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print("Monitoring complete!")


if __name__ == "__main__":
    try:
        monitor_example()
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
