from ._loader import Loader
from loaders.file.csv_loader import CsvLoader
from loaders.file.json_loader import JsonLoader


fileloaders_map = {
    '.csv': CsvLoader(),
    '.json': JsonLoader()
}
