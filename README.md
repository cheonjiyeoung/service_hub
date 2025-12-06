
<div align="center">
  <img width="256" height="256" alt="Service Hub Icon" src="https://github.com/user-attachments/assets/c5190f09-629c-4359-9a15-3014adc924be" />
  
  ### Download Latest Release
  
  [![AMD64](https://img.shields.io/badge/Download-AMD64-blue?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_amd64.deb)
  [![ARM64](https://img.shields.io/badge/Download-ARM64-green?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_arm64.deb)
</div>
# Service Hub
## Overview

Service Hub provides a user-friendly interface to manage systemd services with automatic startup capabilities. The application features a clean GUI with system tray integration, allowing you to easily monitor and control your system services.

## How to use

### Main Interface
![Main Interface](screenshot_main.png)

### Service Configuration
![Service Configuration](screenshot_config.png)

### System Tray
![System Tray](screenshot_tray.png)

## Installation

### Download

Download the latest `.deb` package for your architecture:

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

- **Source Code**: [view source](https://github.com/cheonjiyeoung/service_hub/tree/source)
- **Releases**: [release](https://github.com/cheonjiyeoung/service_hub/tree/release)
- **Issues**: [Report a bug](https://github.com/cheonjiyeoung/service_hub/issues)

---

**Version**: 1.0.0  
**Last Updated**: December 2025
