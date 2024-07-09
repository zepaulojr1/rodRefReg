import json
import os

def load_settings():
    settings_path = os.path.join(os.path.dirname(__file__), 'settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            settings = json.load(file)
    else:
        settings = {}

    # Provide default values for any missing settings
    settings.setdefault('interval', 3600)
    settings.setdefault('stagger', 1)
    settings.setdefault('window_start', 8)
    settings.setdefault('window_end', 20)
    settings.setdefault('selected_relays', [])
    settings.setdefault('num_triggers', {})
    settings.setdefault('relay_pairs', [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10), (11, 12), (13, 14), (15, 16)])
    settings.setdefault('num_hats', 1)  # Add a default value for num_hats

    return settings
