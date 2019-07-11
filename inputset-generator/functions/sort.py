from typing import List

from structures import Dataset


def sort(ds: Dataset, params: List[str]) -> None:
    """Sorts the projects/versions based on the given parameters."""
    # useful url: https://realpython.com/python-sort/

    def clean(attr):
        """Cleans up the attribute to allow better sorting."""
        if type(attr) is str:
            return attr.lower()
        return attr

    # organize the params list--sort by last param first
    # default sort order is ascending
    if params[0] not in ['asc', 'desc']:
        params.insert(0, 'asc')
    # reverse the list
    params = params[::-1]
    # re-insert the sort orders before their associated sort keys
    insert_at = 0
    for i in range(len(params)):
        if params[i] in ['asc', 'desc']:
            param = params.pop(i)
            params.insert(insert_at, param)
            insert_at = i + 1

    # sort the dataset
    reverse = True
    for param in params:
        if param in ['asc', 'desc']:
            # set the sort order
            reverse = (param == 'desc')

        elif param.startswith('v.'):
            # sort by version attribute
            param = param[2:]
            for project in ds.projects:
                project.versions.sort(
                    key=lambda version: clean(getattr(version, param, '')),
                    reverse=reverse
                )

        else:
            # sort by project attribute
            ds.projects.sort(
                key=lambda project: clean(getattr(project, param, '')),
                reverse=reverse
            )
