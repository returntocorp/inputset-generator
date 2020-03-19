from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseStructure(ABC):
    """
    The Base Structure provides core functionality shared by the Project and
    Version classes.
    """

    @property
    @abstractmethod
    def id(self) -> Optional[str]:
        """
        The ID is the primary identifier of the structure. It is typically name
        (for projects) or version (for versions), but this can be modified as
        needed by BaseStructure's subclasses.
        """
        pass

    id: str = field(default=id, init=False)
    metadata: dict = field(default_factory=lambda: {}, repr=False)

    def keep(self, to_keep: List[str]):
        """???"""

        pass

    def drop(self, to_drop: List[str]):
        """???"""

        pass

    def _get_metadata(self, key: str) -> Optional[str]:
        """Helper function to get a value from the metadata dict."""
        val = self.metadata.get(key)
        return val if isinstance(val, str) else None


@dataclass
class Version(BaseStructure, ABC):
    """
    A Version is an abstract class used to store all version-related data.
    It is extended by GenericVersion, GithubCommit, NpmVersion, and PypiRelease.
    """

    pass


@dataclass
class Project(BaseStructure, ABC):
    """
    A Project is an abstract class used to store all project-related data.
    It is extended by GenericProject, GithubRepo, NpmPackage, and PypiProject.
    """

    versions: List[Version] = field(default_factory=lambda: [], repr=False)

    @abstractmethod
    def to_inputset(self) -> dict:
        pass
