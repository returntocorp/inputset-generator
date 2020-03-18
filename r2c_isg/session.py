import dataclasses
import json
import os
import shutil
import webbrowser

from apis import Github, Npm, Pypi#, Requester
#from cache import Cache
from dataset import Dataset
from loaders.file import JsonLoader, CsvLoader
from loaders.weblist import GithubLoader, NpmLoader, PypiLoader


class Session(object):
    """
    A Session manages session- and user-specific data, such as cache settings
    and API keys. It provides functionality for saving and loading datasets to
    and from various sources such as csv files, input set and dataset json
    files, and registry-specific weblists.
    """

    def __init__(self, tmp_dir='.tmp/'):
        # initialize the tmp dir
        self.tmp_dir = tmp_dir
        self._create_tmp_dir()

        # initialize the cache (use defaults for now)
        #self.cache = Cache()

        # initialize the apis
        self.github = Github()
        self.npm = Npm()
        self.pypi = Pypi()

        # generic requester handles all requests not to an api
        #self.requester = Requester()

        self.weblist_loaders = {
            'github': GithubLoader(),
            'npm': NpmLoader(),
            'pypi': PypiLoader(),
        }

    def configure(self, tmp_dir: str = None):
        """Configure the session settings."""

        if tmp_dir:
            self._delete_tmp_dir()
            self.tmp_dir = tmp_dir
            self._create_tmp_dir()

    def _create_tmp_dir(self):
        """Make the temp dir."""

        if not os.path.isdir(self.tmp_dir):
            os.mkdir(self.tmp_dir)

    def _delete_tmp_dir(self):
        """Delete the temp dir."""

        shutil.rmtree(self.tmp_dir)

    def __del__(self):
        self.end()

    def end(self):
        """End the session."""

        self._delete_tmp_dir()
        #self.cache.destroy()

    def load_dataset(self, filepath: str) -> Dataset:
        """Restore a jsonified dataset."""

        return self.load_json(filepath, 9999999999999999, 'dataset')

    def save_dataset(self, dataset: Dataset, filepath: str):
        """Save a jsonified dataset."""

        # convert the dataset to a dict
        dataset_dict = dataclasses.asdict(dataset)

        # save to disk
        self._save_json(filepath, dataset_dict)

    def load_json(self, filepath: str, registry: str, schema: str) -> Dataset:
        """Read in a json file based on a particular schema."""

        return JsonLoader.load(filepath, registry, schema=schema)

    def load_csv(self, filepath: str, registry: str, columns: list) -> Dataset:
        """Read in a csv file with a specified list of columns."""

        return CsvLoader.load(filepath, registry, columns=columns)

    def load_weblist(self, name: str, registry: str) -> Dataset:
        """Download a list of projects from a website."""

        # pick the relevant weblist loader
        loader = self.weblist_loaders[registry]

        return loader.load(name)

    def get_project_metadata(self, dataset: Dataset) -> Dataset:
        """Get project metadata using the relevant API."""
        pass

    def get_project_versions(self, dataset: Dataset) -> Dataset:
        """Load project versions using the relevant API."""
        pass

    def import_inputset(self, filepath: str, registry: str = None) -> Dataset:
        """Import an r2c inputset json."""

        return self.load_json(filepath, registry, 'inputset')

    def export_inputset(self, dataset: Dataset, filepath: str):
        """Export a dataset to an r2c inputset json."""

        # convert the dataset to an input set json
        inputset_dict = dataset.to_inputset()

        # save to disk
        self._save_json(filepath, inputset_dict)

        # show the file
        self._show_json_file(filepath)

    def show_dataset(self, dataset: Dataset):
        """Show a dataset in the native json viewer."""

        # save to a temp file
        filepath = f'{self.tmp_dir}dataset.json'
        self.save_dataset(dataset, filepath)

        # show the file
        self._show_json_file(filepath)

    def _save_json(self, filepath: str, data: dict):
        """Save a dict to a json file."""

        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def _show_json_file(self, filepath: str):
        """Show a json file in the native json viewer."""

        fullpath = os.path.realpath(filepath)
        webbrowser.open_new('file://' + fullpath)
