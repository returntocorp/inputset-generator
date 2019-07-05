from .csv_loader import CsvLoader
from .json_loader import JsonLoader


file_loaders = {
    '.csv': CsvLoader,
    '.json': JsonLoader
}
