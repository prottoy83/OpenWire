#!/usr/bin/env python3
"""
OpenWire - Main entry point
A lightweight, cross-platform network monitoring tool
"""

import sys
import argparse
from openwire.gui import run_gui


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="OpenWire - A lightweight network monitoring tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  openwire              Start the GUI application
  
OpenWire monitors:
  - Active TCP/UDP connections
  - Per-process bandwidth usage
  - Real-time network statistics
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='OpenWire 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Run the GUI
    try:
        run_gui()
    except KeyboardInterrupt:
        print("\nExiting OpenWire...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
