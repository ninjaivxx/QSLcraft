import os
import json
from appdirs import *

app_name = "QSLcraft"

PROFILE_PATH = os.path.join(os.path.dirname(__file__), user_data_dir(app_name),"qsl_profiles.json")



def load_profiles():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, 'r') as f:
            return json.load(f)
    return {}

def save_profiles(profiles):
    if not os.path.exists(os.path.dirname(PROFILE_PATH)):
        os.makedirs(os.path.dirname(PROFILE_PATH))
    with open(PROFILE_PATH, 'w') as f:
        json.dump(profiles, f, indent=2)