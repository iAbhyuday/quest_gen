import json
import pkg_resources

class Base:
    def __init__(self):
        pass

    def _load_config(self, filename):
        config_path = pkg_resources.resource_filename('app', f'config/{filename}')
        with open(config_path, 'r') as config_file:
            return json.load(config_file)
