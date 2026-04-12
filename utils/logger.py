import json
from datetime import datetime


def log_event(event_type, data):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        "data": data
    }

    print("\n[LOG]", json.dumps(log, indent=2))


def log_state(node_name, state):
    print(f"\n[STATE @ {node_name}]")
    print(json.dumps(state, indent=2))