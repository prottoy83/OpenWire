"""
GTK3 GUI for OpenWire network monitoring tool
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from openwire.network_monitor import NetworkMonitor
import threading


class OpenWireWindow(Gtk.Window):
    """Main application window"""
    
    def __init__(self):
        super().__init__(title="OpenWire - Network Monitor")
        self.set_default_size(1000, 600)
        self.set_border_width(10)
        
        # Initialize network monitor
        self.monitor = NetworkMonitor()
        self.update_interval = 2000  # Update every 2 seconds
        
        # Create main layout
        self.create_ui()
        
        # Start monitoring
        self.start_monitoring()
        
    def create_ui(self):
        """Create the user interface"""
        # Main vertical box
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(main_vbox)
        
        # Title label
        title_label = Gtk.Label()
        title_label.set_markup("<b><big>OpenWire Network Monitor</big></b>")
        title_label.set_halign(Gtk.Align.CENTER)
        main_vbox.pack_start(title_label, False, False, 0)
        
        # Network statistics frame
        stats_frame = Gtk.Frame(label="Network Statistics")
        main_vbox.pack_start(stats_frame, False, False, 0)
        
        self.stats_label = Gtk.Label()
        self.stats_label.set_halign(Gtk.Align.START)
        self.stats_label.set_margin_start(10)
        self.stats_label.set_margin_end(10)
        self.stats_label.set_margin_top(5)
        self.stats_label.set_margin_bottom(5)
        stats_frame.add(self.stats_label)
        
        # Create notebook for tabs
        notebook = Gtk.Notebook()
        main_vbox.pack_start(notebook, True, True, 0)
        
        # Connections tab
        connections_scroll = Gtk.ScrolledWindow()
        connections_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.connections_store = Gtk.ListStore(str, str, str, str, str, str)
        self.connections_tree = Gtk.TreeView(model=self.connections_store)
        
        # Add columns
        columns = [
            ("PID", 0),
            ("Process", 1),
            ("Type", 2),
            ("Local Address", 3),
            ("Remote Address", 4),
            ("Status", 5)
        ]
        
        for title, col_id in columns:
            renderer = Gtk.CellRendererText()
            renderer.set_property("font", "Monospace 9")
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_sort_column_id(col_id)
            if col_id in [3, 4]:  # Local and Remote Address columns
                column.set_min_width(150)
            self.connections_tree.append_column(column)
        
        connections_scroll.add(self.connections_tree)
        notebook.append_page(connections_scroll, Gtk.Label(label="Active Connections"))
        
        # Bandwidth usage tab
        bandwidth_scroll = Gtk.ScrolledWindow()
        bandwidth_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        self.bandwidth_store = Gtk.ListStore(str, str, str, str, str)
        self.bandwidth_tree = Gtk.TreeView(model=self.bandwidth_store)
        
        # Add columns
        bandwidth_columns = [
            ("PID", 0),
            ("Process", 1),
            ("Upload", 2),
            ("Download", 3),
            ("Total", 4)
        ]
        
        for title, col_id in bandwidth_columns:
            renderer = Gtk.CellRendererText()
            renderer.set_property("font", "Monospace 9")
            column = Gtk.TreeViewColumn(title, renderer, text=col_id)
            column.set_resizable(True)
            column.set_sort_column_id(col_id)
            self.bandwidth_tree.append_column(column)
        
        bandwidth_scroll.add(self.bandwidth_tree)
        notebook.append_page(bandwidth_scroll, Gtk.Label(label="Bandwidth Usage"))
        
        # Control buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_halign(Gtk.Align.CENTER)
        main_vbox.pack_start(button_box, False, False, 0)
        
        refresh_button = Gtk.Button(label="Refresh Now")
        refresh_button.connect("clicked", self.on_refresh_clicked)
        button_box.pack_start(refresh_button, False, False, 0)
        
        quit_button = Gtk.Button(label="Quit")
        quit_button.connect("clicked", self.on_quit_clicked)
        button_box.pack_start(quit_button, False, False, 0)
        
    def start_monitoring(self):
        """Start the monitoring loop"""
        # Initial update
        self.update_data()
        
        # Schedule periodic updates
        GLib.timeout_add(self.update_interval, self.update_data)
        
    def update_data(self):
        """Update all monitoring data"""
        # Update connections in a separate thread to avoid blocking UI
        threading.Thread(target=self._update_connections, daemon=True).start()
        threading.Thread(target=self._update_bandwidth, daemon=True).start()
        threading.Thread(target=self._update_stats, daemon=True).start()
        
        return True  # Continue periodic updates
    
    def _update_connections(self):
        """Update connections list"""
        connections = self.monitor.get_connections()
        
        # Update UI in main thread
        GLib.idle_add(self._refresh_connections_ui, connections)
    
    def _refresh_connections_ui(self, connections):
        """Refresh connections tree view"""
        self.connections_store.clear()
        
        for conn in connections:
            self.connections_store.append([
                str(conn['pid']) if conn['pid'] else "N/A",
                conn['process'],
                conn['type'],
                conn['local_address'],
                conn['remote_address'],
                conn['status']
            ])
    
    def _update_bandwidth(self):
        """Update bandwidth usage"""
        bandwidth = self.monitor.get_bandwidth_usage()
        
        # Update UI in main thread
        GLib.idle_add(self._refresh_bandwidth_ui, bandwidth)
    
    def _refresh_bandwidth_ui(self, bandwidth):
        """Refresh bandwidth tree view"""
        self.bandwidth_store.clear()
        
        # Sort by total bandwidth (descending)
        sorted_bandwidth = sorted(
            bandwidth.items(),
            key=lambda x: x[1]['total'],
            reverse=True
        )
        
        for pid, data in sorted_bandwidth:
            if data['total'] > 0:  # Only show processes with active bandwidth
                self.bandwidth_store.append([
                    str(pid),
                    data['name'],
                    self.monitor.format_bandwidth(data['upload']),
                    self.monitor.format_bandwidth(data['download']),
                    self.monitor.format_bandwidth(data['total'])
                ])
    
    def _update_stats(self):
        """Update network statistics"""
        stats = self.monitor.get_network_stats()
        
        # Update UI in main thread
        GLib.idle_add(self._refresh_stats_ui, stats)
    
    def _refresh_stats_ui(self, stats):
        """Refresh statistics label"""
        if stats:
            stats_text = (
                f"Total Sent: {self.monitor.format_bytes(stats['bytes_sent'])}  |  "
                f"Total Received: {self.monitor.format_bytes(stats['bytes_recv'])}  |  "
                f"Packets Sent: {stats['packets_sent']:,}  |  "
                f"Packets Received: {stats['packets_recv']:,}"
            )
            if stats['errors_in'] + stats['errors_out'] > 0:
                stats_text += f"  |  Errors: {stats['errors_in'] + stats['errors_out']}"
            if stats['drops_in'] + stats['drops_out'] > 0:
                stats_text += f"  |  Drops: {stats['drops_in'] + stats['drops_out']}"
        else:
            stats_text = "Unable to retrieve network statistics"
        
        self.stats_label.set_text(stats_text)
    
    def on_refresh_clicked(self, button):
        """Handle refresh button click"""
        self.update_data()
    
    def on_quit_clicked(self, button):
        """Handle quit button click"""
        Gtk.main_quit()


def run_gui():
    """Run the GTK3 GUI application"""
    win = OpenWireWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
