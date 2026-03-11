"""
LUMEN HUB — THE RUNNER
Process Manager: spawns apps, assigns ports, monitors health, auto-restarts.
"""
import json
import os
import subprocess
import time
import threading
from datetime import datetime
from pathlib import Path

APPS_DIR = Path("E:/LUMEN_HUB/apps")
DATA_DIR = Path("E:/LUMEN_HUB/data")
STATE_FILE = DATA_DIR / "runner_state.json"
PORT_START = 9000

# Global process registry
_processes: dict[str, dict] = {}
_lock = threading.Lock()


def _load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {}


def _save_state():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    state = {
        name: {
            "port": info["port"],
            "pid": info["process"].pid if info.get("process") else None,
            "status": info["status"],
            "started_at": info.get("started_at"),
        }
        for name, info in _processes.items()
    }
    STATE_FILE.write_text(json.dumps(state, indent=2))


def _next_port() -> int:
    used = {info["port"] for info in _processes.values()}
    port = PORT_START
    while port in used:
        port += 1
    return port


def _read_procfile(app_name: str) -> str | None:
    procfile = APPS_DIR / app_name / "Procfile"
    if not procfile.exists():
        return None
    for line in procfile.read_text().splitlines():
        if line.startswith("web:"):
            return line[4:].strip()
    return None


def start(app_name: str) -> bool:
    """Start an app. Assigns port, launches process."""
    with _lock:
        if app_name in _processes and _processes[app_name]["status"] == "running":
            print(f"[RUNNER] '{app_name}' is already running on port {_processes[app_name]['port']}")
            return True

        cmd = _read_procfile(app_name)
        if not cmd:
            print(f"[RUNNER] ERROR: No Procfile found for '{app_name}'")
            return False

        port = _next_port()
        env = {**os.environ, "PORT": str(port), "APP_NAME": app_name}

        log_dir = DATA_DIR / "logs" / app_name
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = open(log_dir / "app.log", "a")

        print(f"[RUNNER] Starting '{app_name}' on port {port}...")
        try:
            process = subprocess.Popen(
                cmd, shell=True, env=env,
                stdout=log_file, stderr=log_file,
                cwd=str(APPS_DIR / app_name)
            )
            _processes[app_name] = {
                "process": process,
                "port": port,
                "status": "running",
                "started_at": datetime.now().isoformat(),
                "restarts": 0,
                "log_file": log_file,
            }
            _save_state()
            print(f"[RUNNER] ✅ '{app_name}' running — PID {process.pid}, port {port}")
            return True
        except Exception as e:
            print(f"[RUNNER] ERROR: Failed to start '{app_name}': {e}")
            return False


def stop(app_name: str) -> bool:
    """Stop a running app."""
    with _lock:
        if app_name not in _processes:
            print(f"[RUNNER] '{app_name}' not running")
            return False

        info = _processes[app_name]
        proc = info.get("process")
        if proc:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

        info["status"] = "stopped"
        _save_state()
        print(f"[RUNNER] ⛔ '{app_name}' stopped")
        return True


def status() -> list[dict]:
    """Return status of all managed apps."""
    result = []
    for name, info in _processes.items():
        proc = info.get("process")
        alive = proc is not None and proc.poll() is None
        result.append({
            "app": name,
            "port": info["port"],
            "status": "running" if alive else "stopped",
            "pid": proc.pid if proc else None,
            "restarts": info.get("restarts", 0),
            "started_at": info.get("started_at"),
        })
    return result


def _health_monitor():
    """Background thread: detects crashed apps and restarts them."""
    print("[RUNNER] Health monitor started")
    while True:
        time.sleep(10)
        with _lock:
            for name, info in list(_processes.items()):
                if info["status"] != "running":
                    continue
                proc = info.get("process")
                if proc and proc.poll() is not None:
                    print(f"[RUNNER] ⚠️  '{name}' crashed (exit {proc.returncode}). Restarting...")
                    info["restarts"] = info.get("restarts", 0) + 1
                    info["status"] = "crashed"

        # Restart crashed apps (outside lock to avoid deadlock)
        crashed = [n for n, i in _processes.items() if i["status"] == "crashed"]
        for name in crashed:
            time.sleep(2)
            start(name)


def run_monitor():
    """Start health monitor in background thread."""
    t = threading.Thread(target=_health_monitor, daemon=True)
    t.start()
    return t


if __name__ == "__main__":
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    app = sys.argv[2] if len(sys.argv) > 2 else None

    if cmd == "start" and app:
        start(app)
    elif cmd == "stop" and app:
        stop(app)
    elif cmd == "status":
        apps = status()
        if not apps:
            print("[RUNNER] No apps managed")
        for a in apps:
            print(f"  {a['app']:20} port={a['port']}  status={a['status']}  restarts={a['restarts']}")
    elif cmd == "monitor":
        print("[RUNNER] Starting in monitor mode (Ctrl+C to stop)")
        run_monitor()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[RUNNER] Shutting down")
