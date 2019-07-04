import random

from structures.dataset import Dataset


def sample(ds: Dataset, n: int, on_projects: bool) -> None:
    """Samples n projects in place."""

    # select a sample of projects
    if on_projects and len(ds.projects) > n:
        ds.projects = random.sample(ds.projects, n)

    # select a sample of versions in each project
    elif not on_projects:
        for project in ds.projects:
            if len(project.versions) > n:
                project.versions = random.sample(project.versions, n)
