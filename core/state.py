import json
import os

class GlobalState:
    def __init__(self, file_path="core/state_data.json"):
        self.file_path = file_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {
            "whitelist": [],      # Wick Whitelist
            "rescue_key": None,   # Wick Rescue Key
            "temp_rooms": {},     # Astro Room Tracking
            "quarantined": {},    # Wick Jail Data
            "tts_enabled": True   # Global TTS Toggle
        }

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    # Helper methods to sync across modules
    def is_whitelisted(self, user_id):
        return user_id in self.data["whitelist"]

    def set_quarantine(self, user_id, roles):
        self.data["quarantined"][str(user_id)] = roles
        self.save()
