import json
from pathlib import Path

from models.ssh_profile import SSHProfile


PROFILE_DIR = Path("storage/profiles")
PROFILE_DIR.mkdir(parents=True, exist_ok=True)


class ProfileManager:
    def save_profile(self, profile: SSHProfile):
        filepath = PROFILE_DIR / f"{profile.name}.json"

        with open(filepath, "w") as f:
            json.dump(profile.model_dump(), f, indent=2)

    def load_profiles(self):
        profiles = []

        for file in PROFILE_DIR.glob("*.json"):
            with open(file, "r") as f:
                data = json.load(f)
                profiles.append(SSHProfile(**data))

        return profiles


profile_manager = ProfileManager()