import json

from file_handlers import FileHandler
from structures import Dataset


file_formats = {
    'GitRepo': {},
    'GitRepoCommit': {},
    'HttpUrl': {},
    'PackageVersion': {}
}


class JsonFileHandler(FileHandler):
    @staticmethod
    def load(dataset: Dataset, path: str, file_format: str = None) -> None:
        """Default json parser."""

        # load the file
        raw = json.load(open(path))

        # if not user defined, determine the json input type
        file_format = file_format or \
                      raw.get('inputs', [{}])[0].get('input_type', None)
        if not file_format:
            ex = 'Json parsing schema could not be determined.'
            raise Exception(ex)

        # we have a parsing schema for the input type
        if file_format not in file_formats:
            raise Exception('Invalid json parsing schema.')

        # load the appropriate input schema
        schema = file_formats[file_format]

        # parse the json, turn it into a list of projects, & return
        # shoot, how do we return meta info? it's not in the projects...
        # maybe we don't want to keep those for now? seems like they
        # might not carry over between versions

        # should we at least return the file format so that it knows
        # what type of json to save to? Or maybe that should be auto-
        # determined, since github output could be git_repo or
        # git_repo_commit?

        # also need to think through how Registry.get_meta() and
        # Registry.get_versions are going to return values... maybe
        # they're handed an initial Project? They operate on single
        # projects, after all.

        stop = 'here'

    @staticmethod
    def save(dataset: Dataset, name: str = ''):
        """Writes a dataset to json. Unique to json filetype."""
        pass
