from flask import Flask, render_template, request, Response, jsonify
import subprocess
import os
import sys
import json
import threading

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE_DIR, '.venv', 'Scripts', 'python.exe')
PYTHON = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

_processes: dict = {}
_lock = threading.Lock()

SKIP_DIRS = {'.venv', '__pycache__', '.idea', '.git', 'templates', 'static'}
SKIP_FILES = {'app.py'}


def get_scripts():
    groups: dict[str, list] = {}
    for root, dirs, files in os.walk(BASE_DIR):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        rel_root = os.path.relpath(root, BASE_DIR)
        group = 'Root' if rel_root == '.' else rel_root

        py_files = sorted(f for f in files if f.endswith('.py') and f not in SKIP_FILES)
        if py_files:
            groups[group] = [
                {
                    'name': f,
                    'path': (f if rel_root == '.' else os.path.join(rel_root, f)).replace('\\', '/'),
                }
                for f in py_files
            ]
    return groups


@app.route('/')
def index():
    groups = get_scripts()
    flat = []
    for group, items in groups.items():
        for item in items:
            flat.append({**item, 'group': group})
    return render_template('index.html', groups=groups, scripts=flat)


@app.route('/api/run', methods=['POST'])
def run_script():
    data = request.get_json(force=True) or {}
    rel_path = data.get('path', '')
    stdin_text = data.get('stdin', '')

    if not rel_path:
        return jsonify({'error': 'path required'}), 400

    abs_path = os.path.normpath(os.path.join(BASE_DIR, rel_path.replace('/', os.sep)))
    if not abs_path.startswith(BASE_DIR) or not os.path.isfile(abs_path):
        return jsonify({'error': 'script not found'}), 404

    key = rel_path

    def stream():
        try:
            kwargs = {}
            if sys.platform == 'win32':
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW

            proc = subprocess.Popen(
                [PYTHON, '-u', abs_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=0,
                cwd=os.path.dirname(abs_path),
                **kwargs,
            )
            with _lock:
                _processes[key] = proc

            if stdin_text:
                try:
                    payload = stdin_text if stdin_text.endswith('\n') else stdin_text + '\n'
                    proc.stdin.write(payload)
                except Exception:
                    pass
            try:
                proc.stdin.close()
            except Exception:
                pass

            for line in proc.stdout:
                yield f"data: {json.dumps({'t': 'out', 'text': line})}\n\n"

            proc.wait()
            yield f"data: {json.dumps({'t': 'done', 'code': proc.returncode})}\n\n"

        except Exception as exc:
            yield f"data: {json.dumps({'t': 'err', 'text': str(exc)})}\n\n"
        finally:
            with _lock:
                _processes.pop(key, None)

    return Response(
        stream(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        },
    )


@app.route('/api/kill', methods=['POST'])
def kill_script():
    data = request.get_json(force=True) or {}
    key = data.get('path', '')
    with _lock:
        proc = _processes.get(key)
    if proc:
        try:
            proc.kill()
        except Exception:
            pass
        return jsonify({'ok': True})
    return jsonify({'ok': False, 'error': 'not running'}), 404


if __name__ == '__main__':
    print(f"Using Python: {PYTHON}")
    print(f"Open http://127.0.0.1:5000 in your browser")
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)