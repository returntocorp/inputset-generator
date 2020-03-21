from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class BaseStructure(ABC):
    """
    The Base Structure provides core functionality shared by the Project and
    Version classes.
    """

    @abstractmethod
    def get_ids(self) -> dict:
        """The unique identifiers of the structure."""
        pass

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

    def __eq__(self, other):
        # must be the same class type
        if type(self) != type(other):
            return False

        self_ids = self.get_ids()
        other_ids = other.get_ids()

        # must share at least one id
        shared_ids = set(self_ids.keys()).intersection(set(other_ids.keys()))

        for key in shared_ids:
            # must not disagree on any shared ids
            if self_ids[key] != other_ids[key]:
                return False

        return True if len(shared_ids) > 0 else False


@dataclass(eq=False)
class Version(BaseStructure, ABC):
    """
    A Version is an abstract class used to store all version-related data.
    It is extended by GenericVersion, GithubCommit, NpmVersion, and PypiRelease.
    """
    pass


@dataclass(eq=False)
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
