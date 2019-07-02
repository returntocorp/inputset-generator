import json

from file_handlers import FileHandler
from structures import Dataset


class JsonFileHandler(FileHandler):
    def __init__(self):
        self.parsers = {
            'r2c': self._parse_r2c
        }

        self.jsonifiers = {
            'GitRepo': self._jsonify_gitrepo,
            'GitRepoCommit': self._jsonify_gitrepocommit,
            'HttpUrl': self._jsonify_httpurl,
            'PackageVersion': self._jsonify_packageversion
        }

    def load(self, ds: Dataset, filepath: str,
             parser: str = 'r2c') -> None:
        """Loads a json file."""

        # load the file
        data = json.load(open(filepath))

        # check if the parsing schema exists
        if parser not in self.parsers:
            raise Exception('Unrecognized json parsing schema.')

        # run the appropriate parser
        try:
            self.parsers[parser](ds, data)
        except Exception:
            raise Exception('Json file does not match expected schema.')

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

        # check that there's at least one input line
        # (caller will catch any exceptions)
        data['inputs'][0]

        # generate the projects and versions
        # note: to add more input types, simply expand the p_keys and
        # v_keys lists to include the appropriate new values
        for input in data['inputs']:
            # some parts of the input are at the project level...
            p_keys = ['repo_url', 'url', 'package_name']
            p_dict = {k: v for k, v in input.items() if k in p_keys}
            project = ds.get_or_add_project(**p_dict)

            # ...while others are at the version level
            v_keys = ['commit_hash', 'version']
            v_dict = {k: v for k, v in input.items() if k in v_keys}
            if v_dict:
                version = project.get_or_add_version(**v_dict)
                # set standardized version attr--for historical function
                version.historical = v_dict.get('version', None)

    def save(self, ds: Dataset, filepath: str) -> None:
        """Writes a dataset to json. Unique to json filetype."""

        # jsonify the dataset
        try:
            data = self._jsonify(ds)
        except Exception:
            raise Exception('Error jsonifying the dataset.')

        # save the json to file
        with open(filepath, 'w') as file:
            json.dump(data, file)

    def _jsonify(self, ds: Dataset) -> dict:
        # add the dataset's metadata (common to all Datasets)
        d = dict()
        d['name'] = ds.name
        d['version'] = ds.version
        if ds.description: d['description'] = ds.description
        if ds.readme: d['readme'] = ds.readme
        if ds.author: d['author'] = ds.author
        if ds.email: d['email'] = ds.email

        # convert the dataset's projects and versions to inputs
        # using the appropriate registered jsonifier
        if ds.registry and ds.registry.name in ['github']:
            # git projects are outputted as GitRepo or GitRepoCommit
            if len(ds.projects[0].versions) == 0:
                d['inputs'] = self.jsonifiers['GitRepo'](ds)
            else:
                d['inputs'] = self.jsonifiers['GitRepoCommit'](ds)
        elif ds.registry and ds.registry.name in ['pypi', 'npm']:
            # pypi/npm projects are outputted as PackageVersion
            d['inputs'] = self.jsonifiers['PackageVersion'](ds)
        else:
            # other projects are outputted as HttpUrl
            d['inputs'] = self.jsonifiers['HttpUrl'](ds)

        return d

    @staticmethod
    def _jsonify_gitrepo(ds: Dataset) -> list:
        return [{
            'input_type': 'GitRepo',
            'repo_url': getattr(project, 'repo_url')
        } for project in ds.projects]

    @staticmethod
    def _jsonify_gitrepocommit(ds: Dataset) -> list:
        return [{
            'input_type': 'GitRepoCommit',
            'repo_url': getattr(project, 'repo_url'),
            'commit_hash': getattr(version, 'commit_hash')
        } for project in ds.projects for version in project.versions]

    @staticmethod
    def _jsonify_httpurl(ds: Dataset) -> list:
        return [{
            'input_type': 'HttpUrl',
            'url': getattr(project, 'url')
        } for project in ds.projects]

    @staticmethod
    def _jsonify_packageversion(ds: Dataset) -> list:
        return [{
            'input_type': 'PackageVersion',
            'package_name': getattr(project, 'package_name'),
            'version': getattr(version, 'version')
        } for project in ds.projects for version in project.versions]
