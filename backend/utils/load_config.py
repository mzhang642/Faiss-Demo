import json
import os

def load_config(file_name='config.json'):
    try:
        with open(os.path.join(os.path.dirname(__file__), file_name), 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"An error occurred while loading the config: {e}")
        return None

