import random

from structures import Dataset


def sample(ds: Dataset, n: int,
           on_projects: bool = True, seed: str = None) -> None:
    """Samples n projects in place."""

    # seed random, if a seed was provided
    if seed:
        random.seed(seed)

    # select a sample of projects
    if on_projects and len(ds.projects) > n:
        ds.projects = random.sample(ds.projects, n)

    # select a sample of versions in each project
    else:
        for project in ds.projects:
            if len(project.versions) > n:
                project.versions = random.sample(project.versions, n)
