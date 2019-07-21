import json

from r2c_isg.loaders import Loader
from r2c_isg.structures import Dataset, DefaultProject, DefaultVersion
from r2c_isg.structures.projects import project_map
from r2c_isg.structures.versions import version_map


class JsonLoader(Loader):
    @classmethod
    def parsers(cls):
        # no parsers programmed by default
        return {}

    @classmethod
    def load(cls, filepath: str, **kwargs) -> Dataset:
        """Loads a json file."""

        # ensure the user specified which parser to use
        parser = kwargs.pop('parser', None)
        if not parser:
            raise Exception('Please provide the handle to a json parser. '
                            'Valid options are: %s' % list(cls.parsers()))

        # check if the parsing schema exists
        if not parser in cls.parsers():
            raise Exception('Unrecognized json parser name. Review the docs '
                            'to ensure any custom json parsers have been '
                            'properly registered.')

        # initialize a dataset
        ds = Dataset(**kwargs)

        # load the file
        data = json.load(open(filepath))

        # run the appropriate parser
        cls.parsers()[parser](ds, data)

        return ds
