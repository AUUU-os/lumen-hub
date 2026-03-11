"""
LUMEN HUB — THE GATEWAY
Reverse Proxy: routes http://localhost/apps/<name> → internal port.
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen, Request as URLRequest
from urllib.error import URLError

DATA_DIR = Path("E:/LUMEN_HUB/data")
STATE_FILE = DATA_DIR / "runner_state.json"
GATEWAY_PORT = 80


def _get_app_port(app_name: str) -> int | None:
    if not STATE_FILE.exists():
        return None
    state = json.loads(STATE_FILE.read_text())
    info = state.get(app_name)
    if info and info.get("status") == "running":
        return info.get("port")
    return None


def _list_apps() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())


class GatewayHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[GATEWAY] {self.address_string()} - {format % args}")

    def _send_html(self, code: int, body: str):
        content = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(content))
        self.end_headers()
        self.wfile.write(content)

    def _dashboard(self):
        apps = _list_apps()
        rows = ""
        for name, info in apps.items():
            status = info.get("status", "unknown")
            port = info.get("port", "-")
            color = "green" if status == "running" else "red"
            rows += f"""
            <tr>
                <td><a href="/apps/{name}">{name}</a></td>
                <td style="color:{color}">{status}</td>
                <td>{port}</td>
                <td>{info.get('pid', '-')}</td>
                <td>{info.get('started_at', '-')[:19] if info.get('started_at') else '-'}</td>
            </tr>"""

        html = f"""<!DOCTYPE html>
<html><head><title>LUMEN HUB</title>
<style>
  body {{ font-family: monospace; background: #0a0a0a; color: #ccc; padding: 2rem; }}
  h1 {{ color: #ff6b35; }} a {{ color: #61dafb; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #333; padding: 8px 12px; text-align: left; }}
  th {{ background: #1a1a1a; color: #ff6b35; }}
</style></head>
<body>
  <h1>🐺 LUMEN HUB</h1>
  <p><em>Own the Code. Own the Runtime. Own the Metal.</em></p>
  <table>
    <tr><th>App</th><th>Status</th><th>Port</th><th>PID</th><th>Started</th></tr>
    {rows if rows else '<tr><td colspan="5">No apps deployed</td></tr>'}
  </table>
  <br><small>Gateway running on :{GATEWAY_PORT}</small>
</body></html>"""
        self._send_html(200, html)

    def _proxy(self, app_name: str, path: str):
        port = _get_app_port(app_name)
        if not port:
            self._send_html(503, f"<h2>503 — '{app_name}' not running</h2><a href='/'>← Hub</a>")
            return

        target_url = f"http://127.0.0.1:{port}{path}"
        try:
            req = URLRequest(target_url, headers={"Host": f"localhost"})
            with urlopen(req, timeout=10) as resp:
                body = resp.read()
                self.send_response(resp.status)
                for header, value in resp.headers.items():
                    if header.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(header, value)
                self.end_headers()
                self.wfile.write(body)
        except URLError as e:
            self._send_html(502, f"<h2>502 — Bad Gateway</h2><p>{e}</p><a href='/'>← Hub</a>")

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "":
            self._dashboard()
            return

        parts = path.lstrip("/").split("/", 2)
        if len(parts) >= 2 and parts[0] == "apps":
            app_name = parts[1]
            sub_path = "/" + parts[2] if len(parts) > 2 else "/"
            self._proxy(app_name, sub_path)
            return

        self._send_html(404, f"<h2>404 — Not Found</h2><code>{path}</code><br><a href='/'>← Hub</a>")

    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET


def run(port: int = GATEWAY_PORT):
    server = HTTPServer(("0.0.0.0", port), GatewayHandler)
    print(f"[GATEWAY] 🚀 LUMEN HUB running on http://localhost:{port}")
    print(f"[GATEWAY] Apps at http://localhost:{port}/apps/<name>")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[GATEWAY] Shutting down")


if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else GATEWAY_PORT
    run(port)
