import os
import json

def save_log(log, filename="compliance_logs.json"):
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    filepath = os.path.join(logs_dir, filename)

    # Load existing logs if file exists
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            try:
                logs = json.load(f)
                # Ensure it's a list
                if not isinstance(logs, list):
                    logs = []
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []

    # Append the new log
    logs.append(log)

    # Write back as single array
    with open(filepath, "w") as f:
        json.dump(logs, f, indent=2)