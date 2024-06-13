import json
import os

def load_settings():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(base_dir, 'settings.json')
    with open(settings_path, 'r') as f:
        return json.load(f)
