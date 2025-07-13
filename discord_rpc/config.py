import os
import time

class Config:
    def __init__(self, path=None):
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(os.path.dirname(base_dir), 'config.txt')
        self.path = path
        self._last_modified = 0
        self.reload()

    def reload(self):
        modified_time = os.path.getmtime(self.path)
        if modified_time != self._last_modified:
            self._last_modified = modified_time
            config_data = {}
            with open(self.path, 'r') as f:
                for line in f:
                    if line.strip() and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        config_data[key.strip()] = value.strip()

            self.client_id = config_data.get("CLIENT_ID", "")
            self.large_image = config_data.get("LARGE_IMAGE", "")
            self.large_text = config_data.get("LARGE_TEXT", "")
            self.state = config_data.get("STATE", "")
            self.details = config_data.get("DETAILS", "")
            self.enable_timestamp = config_data.get("ENABLE_TIMESTAMP", "true").lower() == "true"
            self.timestamp = int(config_data.get("TIMESTAMP", 0))
            return True
        return False