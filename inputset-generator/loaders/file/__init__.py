from .csv_loader import CsvLoader
from .json_loader import JsonLoader


fileloader_map = {
    '.csv': CsvLoader,
    '.json': JsonLoader
}
