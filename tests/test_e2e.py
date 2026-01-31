import socket
import subprocess
import sys
import time

import httpx

def _free_port() -> int:
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def test_e2e_ping() -> None:
    port = _free_port()
    cmd = [sys.executable, '-m', 'uvicorn', 'demo_project.app:app', '--host', '127.0.0.1', '--port', str(port)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        # Wait briefly for server
        deadline = time.time() + 5
        url = f'http://127.0.0.1:{port}/ping'
        last_err = None
        while time.time() < deadline:
            try:
                r = httpx.get(url, timeout=0.5)
                if r.status_code == 200:
                    assert r.json() == {'pong': True}
                    return
            except Exception as e:  # noqa: BLE001
                last_err = e
                time.sleep(0.1)
        raise AssertionError(f'e2e request never succeeded; last error: {last_err}')
    finally:
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
