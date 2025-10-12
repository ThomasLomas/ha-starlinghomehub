"""A mock server to simulate a Starling Home Hub API using Flask."""

import json
from flask import Flask, jsonify, request

app = Flask(__name__)


def load_stub(stub_name):
    """Load a stub JSON file."""
    with open(f'./stubs/{stub_name}.json') as f:
        stub = json.loads(f.read())
    return stub


@app.get('/status')
def get_status():
    """Get the status of the Starling Home Hub."""
    return jsonify(load_stub('status'))


@app.get('/devices')
def get_devices():
    """Get a list of all devices."""
    return jsonify(load_stub('devices'))


@app.get('/devices/<device_id>')
def get_device(device_id):
    """Get a specific device by ID."""
    return jsonify(load_stub(f'device/{device_id}'))


@app.post('/devices/<device_id>')
def update_device(device_id):
    """Update a specific device by ID."""

    request_body = request.json

    # Check if device exists
    try:
        device = load_stub(f'device/{device_id}')
    except FileNotFoundError:
        return jsonify({"status": "Error", "code": "DEVICE_NOT_FOUND"}), 400

    set_status = {}
    for key in request_body:
        set_status[key] = "OK"
        device['properties'][key] = request_body[key]

    # Save the updated device state back to the stub file (simulating a real update)
    with open(f'./stubs/device/{device_id}.json', 'w') as f:
        f.write(json.dumps(device, indent=4) + '\n')
        f.flush()

    resp = {
        "status": "OK",
        "setStatus": set_status
    }

    return jsonify(resp)


if __name__ == '__main__':
    app.run()
