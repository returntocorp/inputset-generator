from ._base import Loader
from loaders.file.csv import CsvLoader
from loaders.file.json import JsonLoader


fileloaders_map = {
    '.csv': CsvLoader(),
    '.json': JsonLoader()
}
