import json

from file_handlers import FileHandler
from structures import Dataset


class JsonFileHandler(FileHandler):
    def __init__(self):
        super().__init__()

        self.parsers = {
            'GitRepo': self._parse_r2c_git_repo,
            'GitRepoCommit': self._parse_r2c_git_repo_commit,
            'HttpUrl': self._parse_r2c_http_url,
            'PackageVersion': self._parse_r2c_package_version
        }

    def load(self, ds: Dataset, path: str) -> None:
        """Default json parser."""

        # load the file
        data = json.load(open(path))

        # if not user defined, try to determine the json input type
        file_format = data.get('inputs', [{}])[0].get('input_type', None)
        if not file_format:
            ex = 'Json parsing schema could not be determined.'
            raise Exception(ex)

        # we have a parsing schema for the input type
        if file_format not in self.parsers:
            raise Exception('Invalid json parsing schema.')

        # run the appropriate parser
        try:
            self.parsers[file_format](ds, data)
        except:
            raise Exception('Json file does not match expected schema.')

    def save(self, ds: Dataset, name: str = ''):
        """Writes a dataset to json. Unique to json filetype."""
        pass

    @staticmethod
    def _parse_r2c_meta(ds: Dataset, data: dict):
        # data must include a name and version
        ds.name = ds.name or data['name']
        ds.version = ds.version or data['version']

        # data can include description, readme, author, and email
        ds.description = ds.description or data.get('description', None)
        ds.readme = ds.readme or data.get('readme', None)
        ds.author = ds.author or data.get('author', None)
        ds.email = ds.email or data.get('email', None)

    @staticmethod
    def _parse_r2c_git_repo(ds: Dataset, data: dict):
        """
        GIT_REPO = {
            "repo_url": "GIT_URL",
            "input_type": "GitRepo"
        }
        """

        # parse the dataset metadata
        JsonFileHandler._parse_r2c_meta(ds, data)

        # generate the repos
        for d in data['inputs']:
            ds._get_or_add_project(url=d['repo_url'])

    @staticmethod
    def _parse_r2c_git_repo_commit(ds: Dataset, data: dict):
        """
         GIT_REPO_COMMIT = {
             "repo_url": "GIT_URL",
             "commit_hash": "COMMIT_HASH",
             "input_type": "GitRepo"
         }
         """

        # parse the dataset metadata
        JsonFileHandler._parse_r2c_meta(ds, data)

        # generate the repos and commits
        for d in data['inputs']:
            project = ds._get_or_add_project(url=d['repo_url'])
            project._get_or_add_version(commit=d['commit_hash'])

    @staticmethod
    def _parse_r2c_http_url(ds: Dataset, data: dict):
        """
        HTTP_URL = {
            "url": "HTTP_URL",
            "input_type": "HttpUrl"
        }
        """

        # parse the dataset metadata
        JsonFileHandler._parse_r2c_meta(ds, data)

        # generate the projects
        for d in data['inputs']:
            ds._get_or_add_project(url=d['url'])

    @staticmethod
    def _parse_r2c_package_version(ds: Dataset, data: dict):
        """
        PACKAGE_VERSION = {
            "package_name": "PACKAGE_NAME",
            "version": "VERSION_STRING",
            "input_type": "PackageVersion"
        }
        """

        # parse the dataset metadata
        JsonFileHandler._parse_r2c_meta(ds, data)

        # generate the projects and versions
        for d in data['inputs']:
            project = ds._get_or_add_project(name=d['package_name'])
            project._get_or_add_version(version=d['version'])
