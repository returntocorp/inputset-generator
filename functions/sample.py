import random

from structures import Dataset


def sample(ds: Dataset, n: int, sample_projects: bool) -> None:
    """Samples n projects in place."""

    # select a sample of projects
    if sample_projects and len(ds.projects) > n:
        ds.projects = random.sample(ds.projects, n)

    # select a sample of versions in each project
    elif not sample_projects:
        for project in ds.projects:
            if len(project.versions) > n:
                project.versions = random.sample(project.versions, n)
