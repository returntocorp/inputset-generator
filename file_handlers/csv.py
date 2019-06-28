import csv

from file_handlers import FileHandler
from structures import Dataset


# for now, file formats match precisely to registry types
# in the future, this could be changed fairly easily
file_formats = {
    'github': {},
    'npm': {},
    'pypi': {},
    'noreg????': {}
}
file_formats['default'] = file_formats['npm']


class CsvFileHandler(FileHandler):
    @staticmethod
    def load(dataset: Dataset, path: str, file_format: str = None) -> None:
        """Default csv parser."""

        # Todo: read in file, pick parsing format

        # if not user defined, determine the csv input type
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
