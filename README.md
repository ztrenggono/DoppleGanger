# Doppelgänger - Digital Identity Spoofing Tool

A lightweight CLI tool for spoofing various device identities to enhance digital privacy and security. Perfect for mid to low-end devices.

## Features

- MAC Address Spoofing
- Hostname Spoofing
- DNS Resolver Spoofing
- Locale & Keyboard Spoofing
- WebRTC Protection Information
- Hardware Serial Number Detection
- Interactive TUI (Terminal User Interface)
- Real-time Device Status Checking
- Automatic State Backup & Restore

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/doppelganger.git
cd doppelganger
```

2. Run the installer script:
```bash
sudo ./installer.sh
```

## Usage

Run the tool with:
```bash
sudo doppelganger
```

### Main Menu Options

1. **Spoof This Device**
   - Select which identities to spoof
   - View before/after changes
   - Get WebRTC protection tips
   - Automatic state backup before spoofing

2. **Restore Original State**
   - Revert all changes to original state
   - Restore system configuration
   - View restore progress and status
   - Automatic state verification

3. **Check Device Status**
   - View current device configuration
   - Compare with original settings
   - Check spoofing status
   - Real-time system information

4. **Exit**
   - Safely exit the program

## Requirements

- Python 3.6+
- Linux-based operating system
- Root privileges (for system-level changes)

## Dependencies

- rich
- typer
- inquirer
- netifaces
- psutil
- python-nmap
- requests
- uuid

## Security Notice

This tool is designed for privacy enhancement and security testing. Please use responsibly and in accordance with applicable laws and regulations.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - See LICENSE file for details 