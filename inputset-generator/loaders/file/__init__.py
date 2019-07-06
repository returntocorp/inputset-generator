from .csv_loader import CsvLoader
from .json_loader import JsonLoader


class_map = {
    '.csv': CsvLoader,
    '.json': JsonLoader
}
