
<div align="center">
  <img width="256" height="256" alt="Service Hub Icon" src="https://github.com/user-attachments/assets/c5190f09-629c-4359-9a15-3014adc924be" />
  <br><br>
  
  [![AMD64](https://img.shields.io/badge/Download-AMD64-blue?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_amd64.deb)
  [![ARM64](https://img.shields.io/badge/Download-ARM64-green?style=for-the-badge)](https://github.com/cheonjiyeoung/service_hub/raw/release/service-hub_1.0.0_arm64.deb)
</div>

# Service Hub
## Overview

Service Hub provides a user-friendly interface to manage systemd services with automatic startup capabilities. The application features a clean GUI with system tray integration, allowing you to easily monitor and control your system services.

## How to use

### Register service
1. Click "Add" button
   <img width="374" height="292" alt="how_to_register_1" src="https://github.com/user-attachments/assets/adde90ae-0c1a-45c5-a857-080baeba20e3" />

2. Input service name (systemctl service file name)
  <img width="216" height="183" alt="how_to_register_2" src="https://github.com/user-attachments/assets/bda1271b-3fca-4175-b858-d9decd23b48b" />

3. Input target launch file path via text input or "Browse" button (Currently only supports .sh file format)
  <img width="219" height="187" alt="how_to_register_3" src="https://github.com/user-attachments/assets/23d93850-a0a0-45db-a13a-12b975bbf1f3" />

4. Check registered service (Initially in stopped state, auto launch enabled)
  <img width="211" height="143" alt="how_to_register_4" src="https://github.com/user-attachments/assets/e1e86873-c413-47df-91c1-3058e12f9b67" />
  
  ## Service Status Indicators
  - 🔴: Service not running
  - 🟢: Service is running
  - ⚠️: Error

### Service Configuration
When click service name, service manager menu appear
<img width="611" height="144" alt="setting" src="https://github.com/user-attachments/assets/8b3d91a3-3516-4866-9929-40c2364b1537" />

| Button | Description |
|--------|-------------|
| **Start** | Start service |
| **Stop** | Stop service |
| **Restart** | Restart service |
| **Enable** | Enable auto launch |
| **Disable** | Disable auto launch |
| **Remove** | Remove service file and disable auto launch |
| **Modify** | Modify the service file |
| **View Logs** | View service output |

ex)
1. Start button clicked
<img width="624" height="148" alt="start" src="https://github.com/user-attachments/assets/9e61b6da-654f-40bd-b79c-c599ec2ea1fa" />

2. Modify button clicked
<img width="832" height="640" alt="configulation" src="https://github.com/user-attachments/assets/8e761411-eb7b-4846-9019-4c800ffd9545" />

3. View Logs button clicked
<img width="618" height="350" alt="logs" src="https://github.com/user-attachments/assets/17e6ea4c-c7cf-4068-97c3-7f209d4199fe" />

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

## Uninstallation
```bash
# Remove package
sudo apt remove service-hub

# Remove package and configuration files
sudo apt purge service-hub
```

## Usage

### Starting the Application

The daemon starts automatically after installation. Launch the GUI:
```bash
service_hub
```

Or run in daemon mode:
```bash
nohup service_hub &
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
