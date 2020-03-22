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
        """
        A name:value dict of all the unique identifiers of the structure. For
        most structures, ids will consist of some variant of name and url (for
        projects) or version (for versions).

        This function is used for:
        1. Comparing structures. See `__eq__()` below for details.
        2. Adding new projects/versions to existing project/version lists. See
           the `load_...()` functions in the dataset for details.
        """

        pass

    # data obtained from a non-authoritative source (user, file, weblist, etc.)
    data: dict = field(default_factory=lambda: {}, repr=False)

    # data obtained from an authoritative source (typically a registry api)
    metadata: dict = field(default_factory=lambda: {}, init=False, repr=False)

    def keep(self, to_keep: List[str]):
        """???"""

        pass

    def drop(self, to_drop: List[str]):
        """???"""

        pass

    def __post_init__(self):
        if not self.get_ids():
            # Give early warning that no ids means we can't compare structures.
            # It's not the end of the world, but it limits functionality.
            # TODO: log a warning
            pass

    def __eq__(self, other):
        """
        Two structures are considered equal if:
        1. they are of the same type,
        2. they share at least one id key, and
        3. they do not disagree on any values of shared id keys.
        """

        # must be the same class type
        if type(self) != type(other):
            return False

        self_ids = self.get_ids()
        other_ids = other.get_ids()
        if not self_ids or not other_ids:
            # can't effectively compare structures
            # TODO: log a warning
            pass

        shared_ids = set(self_ids.keys()).intersection(set(other_ids.keys()))

        for key in shared_ids:
            # must not disagree on any shared ids
            if self_ids[key] != other_ids[key]:
                return False

        # must share at least one id
        return True if len(shared_ids) > 0 else False


@dataclass(eq=False)
class Version(BaseStructure, ABC):
    """
    A Version is an abstract class used to store all version-related data. It is
    extended by GenericVersion, GithubCommit, NpmVersion, and PypiRelease.
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
        """
        Convert a project and its versions into a list of input set items.
        """

        pass
