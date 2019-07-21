import dill as pickle

from .. import Loader
from ...structures import Dataset


class DatasetLoader(Loader):
    @classmethod
    def load(cls, filepath: str, **_) -> Dataset:
        """Loads a complete dataset from a pickle file."""

        # Note: This may fail to load or produce unexpected behavior if
        # dataset/project/version models have been altered after the
        # backup was made. For now, this scenario has been left
        # unaddressed, as the backup functionality is intended to be
        # used more for quick and easy checkpointing than a full-
        # featured archiving system.

        # load the file
        return pickle.load(open(filepath, 'rb'))
