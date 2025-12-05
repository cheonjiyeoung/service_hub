#!/usr/bin/env python3
import os
import json
import socket
import subprocess
import configparser
import threading

SOCKET_PATH = "/run/service-hub/service_hubd.sock"
INI_FILE = "/var/lib/service-hub/services.ini"

# --------------------------------------
# IPC Helper
# --------------------------------------
def send_json(conn, obj):
    data = json.dumps(obj).encode("utf-8") + b"\n"
    conn.sendall(data)

# --------------------------------------
# Config Helper
# --------------------------------------
def get_config():
    cfg = configparser.ConfigParser()
    if os.path.exists(INI_FILE):
        cfg.read(INI_FILE)
    return cfg

def save_config(cfg):
    os.makedirs(os.path.dirname(INI_FILE), exist_ok=True)
    with open(INI_FILE, "w") as f:
        cfg.write(f)

# --------------------------------------
# systemctl helpers
# --------------------------------------
def svc_file(name):
    return f"/etc/systemd/system/{name}.service"

def run(cmd, check=True):
    return subprocess.run(cmd, text=True, capture_output=True, check=check)

# --------------------------------------
# Commands
# --------------------------------------
def cmd_register(req):
    name = req["name"]
    path = req["path"]

    cfg = get_config()
    if name in cfg.sections():
        return {"error": "already_exists"}

    # .service template
    content = f"""[Unit]
Description={name}
After=network.target

[Service]
ExecStart={path}
Restart=always
WorkingDirectory={os.path.dirname(path)}

[Install]
WantedBy=multi-user.target
"""

    sf = svc_file(name)
    with open(sf, "w") as f:
        f.write(content)

    run(["systemctl", "daemon-reload"])
    run(["systemctl", "enable", f"{name}.service"])

    cfg[name] = {"name": name, "path": path, "enabled": "true"}
    save_config(cfg)

    return {"result": "ok"}


def cmd_unregister(req):
    name = req["name"]

    run(["systemctl", "disable", f"{name}.service"], check=False)

    sf = svc_file(name)
    if os.path.exists(sf):
        os.remove(sf)

    run(["systemctl", "daemon-reload"], check=False)

    cfg = get_config()
    if name in cfg:
        cfg.remove_section(name)
        save_config(cfg)

    return {"result": "ok"}

def cmd_status(req):
    name = req["name"]
    p = run(["systemctl", "is-active", f"{name}.service"],check=False)
    state = p.stdout.strip()
    return {"state": state}

def cmd_start(req):
    run(["systemctl", "start", f"{req['name']}.service"])
    return {"result": "ok"}


def cmd_stop(req):
    run(["systemctl", "stop", f"{req['name']}.service"])
    return {"result": "ok"}


def cmd_restart(req):
    run(["systemctl", "restart", f"{req['name']}.service"])
    return {"result": "ok"}


def cmd_enable(req):
    name = req["name"]
    run(["systemctl", "enable", f"{name}.service"])

    cfg = get_config()
    if name in cfg:
        cfg[name]["enabled"] = "true"
        save_config(cfg)

    return {"result": "ok"}


def cmd_disable(req):
    name = req["name"]
    run(["systemctl", "disable", f"{name}.service"])

    cfg = get_config()
    if name in cfg:
        cfg[name]["enabled"] = "false"
        save_config(cfg)

    return {"result": "ok"}


def cmd_modify(req):
    path = req["path"]
    data = req["data"]

    with open(path, "w") as f:
        f.write(data)

    run(["systemctl", "daemon-reload"])
    return {"result": "ok"}


def cmd_list(req):
    cfg = get_config()
    items = []
    for s in cfg.sections():
        items.append({
            "name": s,
            "path": cfg.get(s, "path"),
            "enabled": cfg.get(s, "enabled", fallback="false")
        })
    return {"services": items}


# --------------------------------------
# journalctl streaming (separate thread)
# --------------------------------------
def cmd_stream_logs(req, conn):
    name = req["name"]

    p = subprocess.Popen(
        ["journalctl", "-u", name, "-f", "-n", "100", "--no-pager"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    def reader():
        for line in p.stdout:
            msg = {"log": line.rstrip()}
            try:
                send_json(conn, msg)
            except:
                break
        p.terminate()

    threading.Thread(target=reader, daemon=True).start()
    return {"result": "streaming"}


# --------------------------------------
# Command router
# --------------------------------------
COMMANDS = {
    "register": cmd_register,
    "unregister": cmd_unregister,
    "start": cmd_start,
    "stop": cmd_stop,
    "restart": cmd_restart,
    "enable": cmd_enable,
    "disable": cmd_disable,
    "modify": cmd_modify,
    "list": cmd_list,
    "status": cmd_status,
    "stream_logs": cmd_stream_logs,
}


# --------------------------------------
# Server Main Loop
# --------------------------------------
def run_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    os.chmod(SOCKET_PATH, 0o666)   # 또는 root:servicehub 전용 권한
    server.listen(5)

    print("ServiceHub daemon running...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


def handle_client(conn):
    with conn:
        for raw in conn.makefile():
            try:
                req = json.loads(raw)
            except:
                continue

            cmd = req.get("cmd")
            if cmd not in COMMANDS:
                send_json(conn, {"error": "unknown_command"})
                continue

            resp = COMMANDS[cmd](req)
            if resp:  # streaming 명령은 최초 response만 내보냄
                send_json(conn, resp)


if __name__ == "__main__":
    run_server()
