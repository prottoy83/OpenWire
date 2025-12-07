"""
Network monitoring module for tracking TCP/UDP connections and bandwidth usage
"""

import psutil
import time
from typing import List, Dict


class NetworkMonitor:
    """Monitor network connections and bandwidth usage"""
    
    def __init__(self):
        self.last_io_counters = {}
        self.last_check_time = time.time()
        
    def get_connections(self) -> List[Dict]:
        """Get all active TCP/UDP connections with process information"""
        connections = []
        
        try:
            # Get all network connections
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'NONE':  # Skip connections without status (usually UDP)
                    conn_type = 'UDP'
                else:
                    conn_type = 'TCP'
                
                # Get process information
                process_name = "System"
                pid = conn.pid
                
                if pid:
                    try:
                        process = psutil.Process(pid)
                        process_name = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = f"PID {pid}"
                
                # Format addresses
                local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                
                connections.append({
                    'pid': pid,
                    'process': process_name,
                    'type': conn_type,
                    'local_address': local_addr,
                    'remote_address': remote_addr,
                    'status': conn.status if conn.status != 'NONE' else 'N/A'
                })
        except (psutil.AccessDenied, PermissionError):
            # Some connections may require elevated privileges
            pass
            
        return connections
    
    def get_bandwidth_usage(self) -> Dict[int, Dict[str, float]]:
        """
        Get bandwidth usage per process (bytes/second)
        
        Note: This method uses general I/O counters (read_bytes/write_bytes)
        as a proxy for network activity. This includes all I/O operations,
        not just network traffic. For most network-intensive applications,
        this provides a reasonable approximation, but it may include disk I/O.
        
        Returns a dictionary with PID as key and bandwidth data as value.
        """
        current_time = time.time()
        time_delta = current_time - self.last_check_time
        
        if time_delta < 0.1:  # Avoid division by very small numbers
            return {}
        
        bandwidth_data = {}
        
        try:
            # Get per-process network IO counters
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    
                    # Get IO counters for the process
                    io_counters = proc.io_counters()
                    
                    current_bytes_sent = io_counters.write_bytes if hasattr(io_counters, 'write_bytes') else 0
                    current_bytes_recv = io_counters.read_bytes if hasattr(io_counters, 'read_bytes') else 0
                    
                    # Calculate bandwidth if we have previous data
                    if pid in self.last_io_counters:
                        last_sent, last_recv = self.last_io_counters[pid]
                        
                        bytes_sent = max(0, current_bytes_sent - last_sent)
                        bytes_recv = max(0, current_bytes_recv - last_recv)
                        
                        bandwidth_data[pid] = {
                            'name': name,
                            'upload': bytes_sent / time_delta,
                            'download': bytes_recv / time_delta,
                            'total': (bytes_sent + bytes_recv) / time_delta
                        }
                    
                    # Store current values for next calculation
                    self.last_io_counters[pid] = (current_bytes_sent, current_bytes_recv)
                    
                except (psutil.NoSuchProcess, psutil.AccessDenied, AttributeError):
                    continue
                    
        except Exception:
            pass
        
        self.last_check_time = current_time
        return bandwidth_data
    
    def get_network_stats(self) -> Dict[str, int]:
        """Get overall network statistics"""
        try:
            net_io = psutil.net_io_counters()
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errors_in': net_io.errin,
                'errors_out': net_io.errout,
                'drops_in': net_io.dropin,
                'drops_out': net_io.dropout
            }
        except Exception:
            return {}
    
    def format_bytes(self, bytes_value: float) -> str:
        """Format bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"
    
    def format_bandwidth(self, bytes_per_sec: float) -> str:
        """Format bandwidth to human-readable format"""
        return f"{self.format_bytes(bytes_per_sec)}/s"
