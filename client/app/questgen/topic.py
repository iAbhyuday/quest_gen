import json
import random
import pkg_resources


class Topic:

    def __init__(self,desc):
        self.desc = desc
        self.qtypes = self._load_config("qtypes.json")["types"]

    def _load_config(self, filename):
        config_path = pkg_resources.resource_filename('app', f'config/{filename}')
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def get_qtype(self):
        return random.choice(self.qtypes)
    
    

    
