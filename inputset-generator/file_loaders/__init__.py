from ._base import FileLoader
from .csv import CsvLoader
from .json import JsonLoader


mapping = {
    '.csv': CsvLoader(),
    '.json': JsonLoader()
}
