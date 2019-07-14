import dill as pickle

from loaders import Loader
from structures import Dataset


class DatasetLoader(Loader):
    def load(self, ds: Dataset, filepath: str, **_) -> None:
        """Loads a complete dataset from a pickle file."""

        # load the file
        ds = pickle.load(open(filepath, 'rb'))
