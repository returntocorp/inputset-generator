from structures import Dataset


def head(ds: Dataset, n: int, on_projects: bool = True) -> None:
    """Keep only the first n projects inplace."""

    # select a sample of projects
    if on_projects:
        ds.projects = ds.projects[:n]

    # select a sample of versions in each project
    else:
        for project in ds.projects:
            project.versions = project.versions[:n]
