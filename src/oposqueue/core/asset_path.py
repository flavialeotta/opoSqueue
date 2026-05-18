import os

import os


CORE_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(CORE_DIR)

def get_asset_path(relative_path):
    """Converts a standard asset path into an absolute path relative to the package root."""
    return os.path.join(BASE_DIR, relative_path)