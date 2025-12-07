#!/usr/bin/env python3
"""
Simple CLI test script for OpenWire to verify functionality without GUI
"""

from openwire.network_monitor import NetworkMonitor
import time
import sys


def main():
    """Run CLI tests"""
    print("=" * 70)
    print("OpenWire - Network Monitor Test")
    print("=" * 70)
    
    monitor = NetworkMonitor()
    
    # Test 1: Network Statistics
    print("\n[1] Network Statistics:")
    print("-" * 70)
    stats = monitor.get_network_stats()
    if stats:
        print(f"  Total Sent:     {monitor.format_bytes(stats['bytes_sent'])}")
        print(f"  Total Received: {monitor.format_bytes(stats['bytes_recv'])}")
        print(f"  Packets Sent:   {stats['packets_sent']:,}")
        print(f"  Packets Recv:   {stats['packets_recv']:,}")
        if stats['errors_in'] + stats['errors_out'] > 0:
            print(f"  Errors:         {stats['errors_in'] + stats['errors_out']}")
        if stats['drops_in'] + stats['drops_out'] > 0:
            print(f"  Drops:          {stats['drops_in'] + stats['drops_out']}")
    else:
        print("  Unable to retrieve network statistics")
    
    # Test 2: Active Connections
    print("\n[2] Active Connections:")
    print("-" * 70)
    connections = monitor.get_connections()
    print(f"  Total connections: {len(connections)}")
    
    # Count by type
    tcp_count = sum(1 for c in connections if c['type'] == 'TCP')
    udp_count = sum(1 for c in connections if c['type'] == 'UDP')
    print(f"  TCP: {tcp_count}, UDP: {udp_count}")
    
    # Show first 10 connections
    print("\n  First 10 connections:")
    print(f"  {'PID':<8} {'Process':<25} {'Type':<5} {'Local':<25} {'Remote':<25} {'Status':<15}")
    print("  " + "-" * 103)
    for conn in connections[:10]:
        pid = str(conn['pid']) if conn['pid'] else "N/A"
        process = conn['process'][:24] if len(conn['process']) > 24 else conn['process']
        local = conn['local_address'][:24] if len(conn['local_address']) > 24 else conn['local_address']
        remote = conn['remote_address'][:24] if len(conn['remote_address']) > 24 else conn['remote_address']
        print(f"  {pid:<8} {process:<25} {conn['type']:<5} {local:<25} {remote:<25} {conn['status']:<15}")
    
    # Test 3: Bandwidth Monitoring
    print("\n[3] Bandwidth Monitoring:")
    print("-" * 70)
    print("  Collecting initial sample...")
    bandwidth1 = monitor.get_bandwidth_usage()
    
    print("  Waiting 2 seconds...")
    time.sleep(2)
    
    print("  Collecting second sample...")
    bandwidth2 = monitor.get_bandwidth_usage()
    
    # Filter and sort by total bandwidth
    active_processes = [(pid, data) for pid, data in bandwidth2.items() if data['total'] > 0]
    active_processes.sort(key=lambda x: x[1]['total'], reverse=True)
    
    if active_processes:
        print(f"\n  Processes with active bandwidth (top 10):")
        print(f"  {'PID':<8} {'Process':<30} {'Upload':<15} {'Download':<15} {'Total':<15}")
        print("  " + "-" * 83)
        for pid, data in active_processes[:10]:
            print(f"  {pid:<8} {data['name'][:29]:<30} "
                  f"{monitor.format_bandwidth(data['upload']):<15} "
                  f"{monitor.format_bandwidth(data['download']):<15} "
                  f"{monitor.format_bandwidth(data['total']):<15}")
    else:
        print("  No active bandwidth detected in this 2-second window")
        print("  (Try running network-intensive tasks for better results)")
    
    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
