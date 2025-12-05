"""
service_utils.py

systemd 기반 서비스 등록/삭제/제어 및 journalctl 로그 스트리밍 유틸
UI(PySide6)에서 호출하기 쉽게 설계됨.
"""

import subprocess
import configparser
import os
# -----------------------------------------------------------
# Register new systemd service (.sh 파일 기반)
# -----------------------------------------------------------
from PySide6.QtCore import QObject, Signal

class ServiceEventBus(QObject):
    service_changed = Signal()

event_bus = ServiceEventBus()

def register_service(service_name: str, service_path: str) -> None:
    """
    서비스 등록: .service 파일 생성 → daemon-reload → enable → INI 저장
    서비스 이름 및 파일 경로 중복 검사 추가
    """
    config = return_config()

    # -------------------------------
    # 1) 서비스 이름 중복 검사
    # -------------------------------
    if service_name in config.sections():
        raise ValueError(f"Service '{service_name}' already exists.")

    # -------------------------------
    # 2) 서비스 파일 경로(.sh) 중복 검사
    # -------------------------------
    for section in config.sections():
        if config.get(section, "path") == service_path:
            raise ValueError(
                f"Path '{service_path}' is already used by service '{section}'."
            )

    # -------------------------------
    # 3) sh 파일 검사
    # -------------------------------
    _, ext = os.path.splitext(service_path)
    if ext != ".sh":
        raise ValueError("Service path must point to a .sh script")

    # -------------------------------
    # 4) systemd 서비스 파일 템플릿
    # -------------------------------
    service_content = f"""
[Unit]
Description={service_name} service
After=network.target

[Service]
ExecStart={service_path}
Restart=always
WorkingDirectory={os.path.dirname(service_path)}

[Install]
WantedBy=multi-user.target
"""

    service_file = f"/etc/systemd/system/{service_name}.service"

    try:
        with open(service_file, "w") as f:
            f.write(service_content)
    except PermissionError:
        raise PermissionError("Root privilege required to install systemd services")

    subprocess.run(["systemctl", "daemon-reload"], check=True)
    subprocess.run(["systemctl", "enable", f"{service_name}.service"], check=True)
    # subprocess.run(["systemctl", "start", f"{service_name}.service"], check=True)

    # -------------------------------
    # 5) INI 파일 저장
    # -------------------------------
    config[service_name] = {
        "name": service_name,
        "path": service_path,
        "enabled": "true"
    }

    with open("services.ini", "w") as f:
        config.write(f)
    event_bus.service_changed.emit()



# -----------------------------------------------------------
# Unregister service
# -----------------------------------------------------------
def unregister_service(service_name: str) -> None:
    """
    서비스 제거: disable → .service 삭제 → daemon-reload → INI에서 제거
    """
    subprocess.run(["systemctl", "disable", f"{service_name}.service"], check=False)

    service_file = f"/etc/systemd/system/{service_name}.service"
    if os.path.exists(service_file):
        os.remove(service_file)

    subprocess.run(["systemctl", "daemon-reload"], check=False)

    # INI 업데이트
    config = return_config()

    if service_name in config:
        config.remove_section(service_name)
        with open("services.ini", "w") as f:
            config.write(f)
    event_bus.service_changed.emit()


# -----------------------------------------------------------
# Enable / Disable 서비스
# -----------------------------------------------------------
def enable_service(service_name: str) -> None:
    subprocess.run(["systemctl", "enable", f"{service_name}.service"], check=True)

    config = return_config()

    if service_name in config:
        config[service_name]["enabled"] = "true"
        with open("services.ini", "w") as f:
            config.write(f)


def disable_service(service_name: str) -> None:
    subprocess.run(["systemctl", "disable", f"{service_name}.service"], check=True)

    config = return_config()

    if service_name in config:
        config[service_name]["enabled"] = "false"
        with open("services.ini", "w") as f:
            config.write(f)


# -----------------------------------------------------------
# Start / Stop / Restart
# -----------------------------------------------------------
def start_service(service_name: str) -> None:
    subprocess.run(["systemctl", "start", f"{service_name}.service"], check=True)


def stop_service(service_name: str) -> None:
    subprocess.run(["systemctl", "stop", f"{service_name}.service"], check=True)


def restart_service(service_name: str) -> None:
    subprocess.run(["systemctl", "restart", f"{service_name}.service"], check=True)


# -----------------------------------------------------------
# journalctl 로그 스트리밍 (yield generator)
# -----------------------------------------------------------
def stream_journalctl(service_name: str):
    """
    journalctl -f 를 subprocess + generator로 감싸서
    QThread에서 편하게 사용하도록 설계.
    """
    process = subprocess.Popen(
        ["journalctl", "-u", service_name, "-f", "-n", "100", "--no-pager"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        while True:
            line = process.stdout.readline()
            if not line:
                break
            yield line.rstrip()
    finally:
        process.terminate()

def return_config():
    config = configparser.ConfigParser()
    config.read("services.ini")
    return config

def return_service_state(service_name):
    result = subprocess.run(
        ["systemctl", "is-active", service_name],
        capture_output=True,
        text=True,
        check=False
    )
    return result

def modify_service_file(service_path, data):
    with open(service_path, "w") as f:
        f.write(data)
    subprocess.run(["systemctl", "daemon-reload"], check=True)
