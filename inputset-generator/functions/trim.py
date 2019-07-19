from structures import Dataset


def trim(ds: Dataset, n: int, on_projects: bool = True) -> None:
    """Keep only the first n projects inplace."""

    # select a sample of projects
    if on_projects:
        orig_count = len(ds.projects)
        ds.projects = ds.projects[:n]
        print('         Trimmed to first {:,} projects ({:,} dropped).'
              .format(n, max(orig_count - n, 0)))

    # select a sample of versions in each project
    else:
        dropped = 0
        for project in ds.projects:
            dropped += len(project.versions)
            project.versions = project.versions[:n]
            dropped -= len(project.versions)

        print('         Trimmed to first {:,} versions in each project '
              '({:,} total versions dropped).'.format(n, dropped))
