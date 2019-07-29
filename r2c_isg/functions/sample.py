import random

from r2c_isg.structures import Dataset


def sample(ds: Dataset, n: int,
           on_versions: bool = True, seed: str = None) -> None:
    """Samples n projects in place."""

    # seed random, if a seed was provided
    if seed:
        random.seed(seed)

    # select a sample of versions in each project
    if on_versions:
        dropped = 0
        for project in ds.projects:
            dropped += len(project.versions)
            if len(project.versions) > n:
                project.versions = random.sample(project.versions, n)
            dropped -= len(project.versions)

        print('         Sampled {:,} versions from each of {:,} projects ({:,} '
              'total versions dropped).'.format(n, len(ds.projects), dropped))

    # select a sample of projects
    elif len(ds.projects) > n:
        orig_count = len(ds.projects)
        ds.projects = random.sample(ds.projects, n)
        print('         Sampled {:,} projects from {:,} (dropped {:,}).'
              .format(n, orig_count, max(orig_count - n, 0)))

    else:
        # this should never happen...
        raise Exception('Dataset has no projects; cannot sample.')
