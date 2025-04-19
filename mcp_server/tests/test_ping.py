# mcp_server/tests/test_ping.py

import json
import subprocess
import time
import socket
import sys

def free_port() -> int:
    import socket as s
    sock = s.socket()
    sock.bind(("", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def test_ping():
    port = free_port()
    # Arranca server.py en un puerto libre
    proc = subprocess.Popen([sys.executable, "server.py", "--port", str(port)])
    time.sleep(1)  # esperamos que arranque
    # Invocamos ping vía CLI
    out = subprocess.check_output([
        sys.executable, "-m", "mcpcli",
        "ping", "--server", "local",
        "--url", f"http://127.0.0.1:{port}"
    ])
    proc.terminate()
    data = json.loads(out)
    assert data["message"] == "pong"