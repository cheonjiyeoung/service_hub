import socket
import json

SOCKET_PATH = "/run/service-hub/service_hubd.sock"

# --------------------------------------
# 내부 IPC helper
# --------------------------------------
def _send(req: dict):
    """
    요청(req)을 UDS에 보내고 단일 응답을 받는다.
    스트리밍은 별도 함수 사용.
    """
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(SOCKET_PATH)
        sock.sendall(json.dumps(req).encode("utf-8") + b"\n")

        # 1회 응답 받음
        data = sock.recv(65536)
        if not data:
            return None
        return json.loads(data.decode("utf-8"))


# --------------------------------------
# PUBLIC API (GUI에서 사용)
# --------------------------------------
def register_service(service_name: str, service_path: str):
    req = {
        "cmd": "register",
        "name": service_name,
        "path": service_path
    }
    return _send(req)


def unregister_service(service_name: str):
    req = {
        "cmd": "unregister",
        "name": service_name
    }
    return _send(req)

def return_service_state(service_name: str):
    req = {"cmd": "status", "name": service_name}
    return _send(req)

def start_service(service_name: str):
    req = {"cmd": "start", "name": service_name}
    return _send(req)


def stop_service(service_name: str):
    req = {"cmd": "stop", "name": service_name}
    return _send(req)


def restart_service(service_name: str):
    req = {"cmd": "restart", "name": service_name}
    return _send(req)


def enable_service(service_name: str):
    req = {"cmd": "enable", "name": service_name}
    return _send(req)


def disable_service(service_name: str):
    req = {"cmd": "disable", "name": service_name}
    return _send(req)


def modify_service_file(path: str, data: str):
    req = {
        "cmd": "modify",
        "path": path,
        "data": data
    }
    return _send(req)


def list_services():
    req = {"cmd": "list"}
    return _send(req)


# --------------------------------------
# 로그 스트리밍 (yield generator)
# --------------------------------------
def stream_logs(service_name: str):
    """
    로그를 지속적으로 yield하는 generator.
    GUI(QThread)에서 사용 가능.
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET_PATH)
    sock.sendall(json.dumps({"cmd": "stream_logs", "name": service_name}).encode("utf-8") + b"\n")

    f = sock.makefile()

    # 첫 응답 (streaming 시작 메시지)
    first = f.readline()
    if first:
        yield json.loads(first)

    # 이후 들어오는 log 메시지 streaming
    for line in f:
        try:
            msg = json.loads(line)
            yield msg
        except:
            break
