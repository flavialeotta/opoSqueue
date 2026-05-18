import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def get_asset_path(relative_path):
    """Converts a standard asset path into an absolute system path."""
    return os.path.join(BASE_DIR, relative_path)