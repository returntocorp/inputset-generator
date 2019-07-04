from ._base import FileLoader
from .csv import CsvLoader
from .json import JsonLoader


file_handlers = {
    '.csv': CsvLoader(),
    '.json': JsonLoader()
}
