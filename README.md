![systemctl_manager_ico](https://github.com/user-attachments/assets/c037ed91-300f-48aa-a37c-35c1233e9239)

# Service Hub

A systemctl-based service auto-start manager with GUI interface for Linux systems.
![Uplo<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <rect x="12" y="12" width="40" height="40" rx="8" fill="#5C6BC0"/>
  <g transform="translate(32, 28)">
    <circle cx="0" cy="-10" r="2" fill="white"/>
    <circle cx="8.66" cy="-5" r="2" fill="white"/>
    <circle cx="8.66" cy="5" r="2" fill="white"/>
    <circle cx="0" cy="10" r="2" fill="white"/>
    <circle cx="-8.66" cy="5" r="2" fill="white"/>
    <circle cx="-8.66" cy="-5" r="2" fill="white"/>
  </g>
  
  <text x="32" y="45" font-family="Arial, sans-serif" font-size="5" font-weight="bold" fill="white" text-anchor="middle">SERVICE</text>
  <text x="32" y="51" font-family="Arial, sans-serif" font-size="5" font-weight="bold" fill="white" text-anchor="middle">HUB</text>
</svg>ading systemctl_manager_ico.svg…]()



## Overview

Service Hub provides a user-friendly interface to manage systemd services with automatic startup capabilities. The application features a clean GUI with system tray integration, allowing you to easily monitor and control your system services.

### Key Features

- Systemctl-based service management
- Automatic service startup configuration
- System tray integration
- Daemon mode support
- Support for AMD64 and ARM64 architectures

## Screenshots

### Main Interface
![Main Interface](screenshot_main.png)

### Service Configuration
![Service Configuration](screenshot_config.png)

### System Tray
![System Tray](screenshot_tray.png)

## Installation

### Download

Download the latest `.deb` package for your architecture:

- **AMD64**: [service-hub_1.0.0_amd64.deb](https://github.com/cheonjiyeoung/service_hub/blob/release/service-hub_1.0.0_amd64.deb)
- **ARM64**: [service-hub_1.0.0_arm64.deb](https://github.com/cheonjiyeoung/service_hub/blob/release/service-hub_1.0.0_arm64.deb)

### Install
```bash
# AMD64
sudo dpkg -i service-hub_1.0.0_amd64.deb
sudo apt-get install -f  # Install dependencies if needed

# ARM64
sudo dpkg -i service-hub_1.0.0_arm64.deb
sudo apt-get install -f
```

## Usage

### Starting the Application

The daemon starts automatically after installation. Launch the GUI:
```bash
service_hub_gui
```

Or run in daemon mode:
```bash
nohup service_hub_gui &
```

### Managing Services

1. Click the Service Hub icon in the system tray
2. Select "Add Service" to register a new service
3. Configure auto-start settings for each service
4. Monitor service status from the tray menu

## Requirements

- Linux with systemd
- Python 3.8 or higher
- PySide6

## Development

Want to contribute or build from source? Check out the source code:

**[View Source Code](https://github.com/cheonjiyeoung/service_hub/tree/source)**

## Architecture
```
Service Hub
├── Daemon (service_hubd)     - Background service monitor
├── GUI (service_hub_gui)     - System tray application
└── ICP Module                - Inter-process communication
```

## License

MIT License - Free to use for anyone without restrictions.

## Links

- **Source Code**: [source branch](https://github.com/cheonjiyeoung/service_hub/tree/source)
- **Releases**: [release branch](https://github.com/cheonjiyeoung/service_hub/tree/release)
- **Issues**: [Report a bug](https://github.com/cheonjiyeoung/service_hub/issues)

---

**Version**: 1.0.0  
**Last Updated**: December 2025
