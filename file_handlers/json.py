import json

from file_handlers import FileHandler
from structures import Dataset


class JsonFileHandler(FileHandler):
    def __init__(self):
        super().__init__()

        self.parsers = {
            'r2c': self._parse_r2c
        }

        self.jsonifiers = {
            'r2c': self._jsonify_r2c
        }

    def load(self, ds: Dataset, filepath: str, parser: str = 'r2c') -> None:
        """Default json parser."""

        # load the file
        data = json.load(open(filepath))

        # check if the parsing schema exists
        if parser not in self.parsers:
            raise Exception('Unrecognized json parsing schema.')

        # run the appropriate parser
        try:
            self.parsers[parser](ds, data)
        except:
            raise Exception('Json file does not match expected schema.')

    def save(self, ds: Dataset, filepath: str, jsonifier: str = 'r2c') -> None:
        """Writes a dataset to json. Unique to json filetype."""
        # check if the parsing schema exists
        if jsonifier not in self.jsonifiers:
            raise Exception('Unrecognized jsonify schema.')

        # run the appropriate parser
        try:
            data = self.jsonifiers[jsonifier](ds)
        except:
            raise Exception('Json file does not match expected schema.')

        # write to file
        with open(filepath, 'w') as file:
            json.dump(data, file)

    @staticmethod
    def _parse_r2c(ds: Dataset, data: dict):
        # don't overwrite previously set metadata
        ds.name = ds.name or data['name']
        ds.version = ds.version or data['version']

        # grab any optional metadata
        ds.description = ds.description or data.get('description', None)
        ds.readme = ds.readme or data.get('readme', None)
        ds.author = ds.author or data.get('author', None)
        ds.email = ds.email or data.get('email', None)

        # generate the projects and versions
        for input in data['inputs']:
            # some parts of the input are at the project level...
            p_keys = ['repo_url', 'url', 'package_name']
            p_dict = {k: v for k, v in input.items() if k in p_keys}
            project = ds._get_or_add_project(**p_dict)

            # ...while others are at the version level
            v_keys = ['commit_hash', 'version']
            v_dict = {k: v for k, v in input.items() if k in v_keys}
            if v_dict:
                project._get_or_add_version(**v_dict)

    @staticmethod
    def _jsonify_r2c(ds: Dataset):
        pass
