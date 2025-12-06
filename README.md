# Service Hub

A systemctl-based service auto-start manager with GUI interface for Linux systems.

## Overview

Service Hub provides a user-friendly interface to manage systemd services with automatic startup capabilities. The application consists of two main components:

- **Service Hub Daemon**: Background service that monitors and manages systemd services
- **Service Hub GUI**: System tray application for convenient service management

The GUI runs in the system tray and can be hidden or closed while the daemon continues to operate in the background. For persistent operation, daemon mode execution is recommended.

## Prerequisites

- Linux operating system with systemd
- Python 3.8 or higher
- Root privileges (for daemon operation)

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd service-hub
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Daemon

The daemon requires root privileges to interact with systemd services.
```bash
sudo python service_hub_daemon/service_hubd.py
```

### Starting the GUI

**Standard mode:**
```bash
python service_hub_gui/service_hub_gui.py
```

**Daemon mode (recommended):**
```bash
nohup python service_hub_gui/service_hub_gui.py &
```

Running in daemon mode allows the GUI to persist in the system tray without being tied to a terminal session.

## Features

- Monitor systemd service status
- Configure automatic service startup
- System tray integration for quick access
- Minimize to tray on close
- Background daemon operation

## Architecture
```
service-hub/
├── service_hub_daemon/    # Background service monitor
├── service_hub_gui/       # System tray GUI application
└── service_hub_icp/       # Inter-process communication
```

## License

MIT License - Free to use for anyone without restrictions.
