import json

from structures import Dataset, DefaultProject, DefaultVersion
from structures.projects import project_map
from structures.versions import version_map
from loaders import Loader


class JsonLoader(Loader):
    @classmethod
    def parsers(cls):
        # no parsers programmed by default
        return {}

    @classmethod
    def load(cls, filepath: str, parser: str = None, **kwargs) -> Dataset:
        """Loads a json file."""

        # ensure the user specified which parser to use
        assert parser, ('Missing json parser. Valid options are: %s'
                        % list(cls.parsers()))

        # initialize a dataset
        ds = Dataset(**kwargs)

        # load the file
        data = json.load(open(filepath))

        # check if the parsing schema exists
        assert parser in cls.parsers, 'Unrecognized json parser.'

        # run the appropriate parser
        cls.parsers()[parser](ds, data)

        return ds
