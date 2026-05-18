import os
import json
from models.ssh_profile import SSHProfile

class ProfileManager:
    def __init__(self, directory="storage/profiles/"):
        self.directory = directory
        # Create the folder if it doesn't exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def load_profiles(self):
        profiles = []
        # Look for every .json file in the profiles directory
        for filename in os.listdir(self.directory):
            if filename.endswith(".json"):
                path = os.path.join(self.directory, filename)
                try:
                    with open(path, "r") as f:
                        data = json.load(f)
                        # Handle if the file is a single dict or a list
                        if isinstance(data, list):
                            profiles.extend([SSHProfile(**p) for p in data])
                        else:
                            profiles.append(SSHProfile(**data))
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        return profiles

    def save_profile(self, profile):
        # Save each profile as its own filename based on the profile name
        filename = f"{profile.name.replace(' ', '_').lower()}.json"
        path = os.path.join(self.directory, filename)
        
        with open(path, "w") as f:
            data = profile.model_dump() if hasattr(profile, 'model_dump') else profile.dict()
            json.dump(data, f, indent=4)

    def delete_profile(self, profile_name):
        profiles = self.load_profiles()
        profiles = [p for p in profiles if p.name != profile_name]
        with open(self.filename, "w") as f:
            json.dump([p.dict() if hasattr(p, 'dict') else p.__dict__ for p in profiles], f, indent=4)

profile_manager = ProfileManager()