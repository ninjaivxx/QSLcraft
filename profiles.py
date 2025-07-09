import os
import json

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "qsl_profiles.json")

def load_profiles():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    with open(PROFILE_PATH, 'w') as f:
        json.dump(profiles, f, indent=2)