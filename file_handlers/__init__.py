from ._base import FileHandler
from .csv import CsvFileHandler
from .json import JsonFileHandler


file_handlers = {
    '.csv': CsvFileHandler,
    '.json': JsonFileHandler
}
