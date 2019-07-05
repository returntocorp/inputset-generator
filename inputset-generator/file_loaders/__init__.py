from ._base import FileLoader
from .csv import CsvLoader
from .json import JsonLoader


fileloaders_map = {
    '.csv': CsvLoader(),
    '.json': JsonLoader()
}
