from flask import Flask, request, jsonify
import threading
from lockdown import monitor_and_kill

app = Flask(__name__)

# Global state
state = {
    "banned": [],
    "password": None,
    "stop_event": None,
    "thread": None
}

@app.route('/api/config', methods=['POST'])
def set_config():
    data = request.json
    state['banned'] = [name.lower() for name in data.get('banned', [])]
    state['password'] = data.get('password')
    return jsonify(success=True)

@app.route('/api/start', methods=['POST'])
def start_monitor():
    if state['thread'] and state['thread'].is_alive():
        return jsonify(error="Monitor already running"), 400
    stop_event = threading.Event()
    t = threading.Thread(
        target=monitor_and_kill,
        args=(state['banned'], stop_event),
        daemon=True
    )
    t.start()
    state['stop_event'] = stop_event
    state['thread'] = t
    return jsonify(success=True)

@app.route('/api/stop', methods=['POST'])
def stop_monitor():
    data = request.json
    if data.get('password') != state['password']:
        return jsonify(success=False), 403
    if state['stop_event']:
        state['stop_event'].set()
        state['thread'].join()
        state['thread'] = None
        state['stop_event'] = None
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
