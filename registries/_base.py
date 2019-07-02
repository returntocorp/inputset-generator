from abc import ABC, abstractmethod

from structures import Dataset, Project


class Registry(ABC):
    def __init__(self):
        # child classes must set name and url_format
        self.name: str
        self.url_format: str

        self.weblists: dict = {}

    def load_weblist(self, dataset: Dataset, name: str) -> None:
        """Loads and parses a weblist, adding all identified projects/
        versions to the given dataset."""

        # try to load the weblist data (calls the registered loader)
        try:
            data = self.weblists[name]['loader']()
        except Exception:
            raise Exception('Error loading weblist.')

        # parse the data (calls the registered parser)
        try:
            self.weblists[name]['parser'](dataset, data)
        except Exception:
            raise Exception('Error parsing weblist data.')

    @abstractmethod
    def load_project_metadata(self, project: Project) -> None: pass

    @abstractmethod
    def load_project_versions(self, project: Project, historical: str = 'all') -> None: pass
