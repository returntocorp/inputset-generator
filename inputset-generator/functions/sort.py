from typing import List

from structures import Dataset


def sort(ds: Dataset, params: List[str]) -> None:
    """Sorts the projects/versions based on the given parameters."""
    # useful url: https://realpython.com/python-sort/

    def clean(attr):
        """Cleans up the attribute to allow better sorting."""
        if isinstance(attr, str):
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

        else:
            # sort on this parameter
            # Note: Parameter strings can follow these formats:
            #   'attr'          sort on project attribute
            #   'uuids.key'     sort on project uuid
            #   'meta.key'      sort on project meta
            #   'v.attr'        sort on version attribute
            #   'v.uuids.key'   sort on version uuid
            #   'v.meta.key'    sort on version meta

            p_list = param.split('.')

            # determine if we're sorting on project or version
            on_project = True
            if p_list[0] == 'v':
                on_project = False
                p_list.pop(0)

            # build a sort function
            if p_list[0] == 'uuids':
                # sort on a uuid value
                sort_func = lambda o: o.uuids_[p_list[1]]()
            elif p_list[0] == 'meta':
                # sort on a meta value
                sort_func = lambda o: o.meta_[p_list[1]]()
            else:
                # sort on a regular attribute
                sort_func = lambda o: clean(getattr(o, p_list[0], ''))

            # perform the sort
            if on_project:
                # sort on project
                ds.projects.sort(key=sort_func, reverse=reverse)
            else:
                # sort on version
                for project in ds.projects:
                    project.versions.sort(key=sort_func, reverse=reverse)
