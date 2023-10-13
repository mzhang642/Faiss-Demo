import json
import os

def load_config():
    with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as f:
        return json.load(f)

config = load_config()