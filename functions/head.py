from structures import Dataset


def head(ds: Dataset, n: int) -> None:
    """Keep only the first n projects inplace."""

    ds.projects = ds.projects[:n]
