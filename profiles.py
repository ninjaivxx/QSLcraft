import os
import json
from tkinter import messagebox
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

def backup_profiles(backup_dir):
    backup_path = os.path.join(backup_dir, "qsl_profiles_backup.json")
    
    if not backup_dir:
        messagebox.showerror("Error", "No output folder selected.")
        return
    if not os.path.exists(PROFILE_PATH):
        messagebox.showerror("Error", "No profiles to backup.")
        return

    try:
        with open(PROFILE_PATH, 'r') as f:
            profiles = json.load(f)
        with open(backup_path, 'w') as f:
            json.dump(profiles, f, indent=2)
        messagebox.showinfo("Backup Successful", f"Profiles backed up to {backup_path}")
    except Exception as e:
        messagebox.showerror("Backup Failed", f"An error occurred while backing up profiles: {str(e)}")
        return

    return backup_path