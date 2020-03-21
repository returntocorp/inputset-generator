from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseStructure(ABC):
    """
    The Base Structure provides core functionality shared by the Project and
    Version classes.
    """

    # set by user or obtained from a weblist or other non-authoritative source
    data: dict = field(default_factory=lambda: {}, repr=False)

    # obtained from a registry api; should be treated as readonly
    metadata: dict = field(default_factory=lambda: {}, repr=False, init=False)

    def keep(self, to_keep: List[str]):
        """???"""

        pass

    def drop(self, to_drop: List[str]):
        """???"""

        pass


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

    # every project contains a list of versions
    versions: List[Version] = field(default_factory=lambda: [], repr=False)

    @abstractmethod
    def to_inputset(self, include_invalid: bool = False) -> list:
        """Convert a project and its versions into a list of input set items."""
        pass
