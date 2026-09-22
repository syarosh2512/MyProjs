import http.server
import subprocess
import json
import os
import webbrowser
import threading

SCRIPTS = {
    "cuasvvc0001": "cuasvvc0001 autologin.py",
    "cuasvvc0002": "cuasvvc0002 autologin.py",
    "dlt2000": "DLT 2000 Access.py",
    "hpimc": "HP IMC Access.py",
}

DIR = os.path.dirname(os.path.abspath(__file__))

HTML = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>VMware Servers</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: "Segoe UI", Arial, sans-serif;
            background: #1a1a2e;
            color: #e0e0e0;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            min-height: 100vh;
        }
        h1 { font-size: 22px; font-weight: 600; color: #a78bfa; margin-bottom: 8px; letter-spacing: 1px; }
        .subtitle { font-size: 12px; color: #6b7280; margin-bottom: 30px; }
        .card-grid { display: flex; flex-direction: column; gap: 14px; width: 100%; max-width: 420px; }
        .card {
            background: #16213e;
            border: 1px solid #2d2d5e;
            border-radius: 10px;
            padding: 18px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .card:hover { border-color: #7c3aed; }
        .card-title { font-size: 15px; font-weight: 600; color: #c4b5fd; }
        .card-url { font-size: 11px; color: #6b7280; margin-top: 4px; }
        .btn {
            background: #7c3aed;
            color: #fff;
            border: none;
            border-radius: 7px;
            padding: 9px 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
        }
        .btn:hover { background: #6d28d9; }
        .btn:disabled { background: #4b5563; cursor: default; }
        #status { margin-top: 22px; font-size: 12px; color: #10b981; min-height: 18px; }
    </style>
</head>
<body>
    <h1>VM ware Launcher</h1>
    <div class="subtitle">vSphere auto-login scripts</div>
    <div class="card-grid">
        <div class="card">
            <div>
                <div class="card-title">cuasvvc0001</div>
                <div class="card-url">cuasvvc0001.ua.inpkg.net</div>
            </div>
            <button class="btn" onclick="run('cuasvvc0001')">Launch</button>
        </div>
        <div class="card">
            <div>
                <div class="card-title">cuasvvc0002</div>
                <div class="card-url">cuasvvc0002.ua.inpkg.net</div>
            </div>
            <button class="btn" onclick="run('cuasvvc0002')">Launch</button>
        </div>
        <div class="card">
            <div>
                <div class="card-title">DLT 2000</div>
                <div class="card-url">10.222.1.220</div>
            </div>
            <button class="btn" onclick="run('dlt2000')">Launch</button>
        </div>
        <div class="card">
            <div>
                <div class="card-title">HP IMC</div>
                <div class="card-url">10.222.1.123:8080</div>
            </div>
            <button class="btn" onclick="run('hpimc')">Launch</button>
        </div>
    </div>
    <div id="status"></div>
    <script>
        function run(name) {
            const status = document.getElementById("status");
            status.style.color = "#10b981";
            status.textContent = "Launching " + name + "...";
            fetch("/run/" + name)
                .then(r => r.json())
                .then(d => {
                    status.textContent = d.ok ? "Launched: " + name : "Error: " + d.error;
                    if (!d.ok) status.style.color = "#ef4444";
                });
        }
    </script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

        elif self.path.startswith("/run/"):
            name = self.path[5:]
            script = SCRIPTS.get(name)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            if script:
                try:
                    subprocess.Popen(["python", os.path.join(DIR, script)])
                    self.wfile.write(json.dumps({"ok": True}).encode())
                except Exception as e:
                    self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
            else:
                self.wfile.write(json.dumps({"ok": False, "error": "unknown script"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = 8765
    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}"
    print(f"Launcher running at {url}  (close this window to stop)")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    server.serve_forever()