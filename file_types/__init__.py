from ._base import FileType
from .csv import CsvFileType
from .json import JsonFileType

file_types = {
    '.csv': CsvFileType,
    '.json': JsonFileType
}
