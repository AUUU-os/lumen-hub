"""
LUMEN HUB — Main CLI
Usage:
  python lumen.py deploy <app_name>   # build + start
  python lumen.py start <app_name>
  python lumen.py stop <app_name>
  python lumen.py status
  python lumen.py gateway [port]
  python lumen.py monitor
"""
import sys
from orchestrator.builder import build
from orchestrator.runner import start, stop, status, run_monitor
from orchestrator.gateway import run as run_gateway
import time

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0]
    app = args[1] if len(args) > 1 else None

    if cmd == "deploy" and app:
        print(f"[LUMEN] Deploying '{app}'...")
        if build(app):
            start(app)
    elif cmd == "start" and app:
        start(app)
    elif cmd == "stop" and app:
        stop(app)
    elif cmd == "status":
        apps = status()
        if not apps:
            print("[LUMEN] No apps running")
        for a in apps:
            print(f"  {a['app']:20} :{a['port']}  {a['status']}  restarts={a['restarts']}")
    elif cmd == "gateway":
        port = int(args[1]) if len(args) > 1 else 8080
        run_monitor()
        run_gateway(port)
    elif cmd == "monitor":
        run_monitor()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
