from dill.source import getsource

from structures import Dataset, DefaultProject, DefaultVersion
from structures.projects import project_map
from structures.versions import version_map


def show(ds: Dataset, n: int = 5):
    """Summarizes the key data of the first n projects."""

    for p in ds.projects[:n]:
        project_type = str(type(p).__name__)
        attr_indent = len(project_type) + 5
        val_indent = 11

        # print project uuids
        print('%s(%s' % (
            (' ' * 4) + project_type,
            ('\n' + ' ' * attr_indent).join([
                '%s = %s' % (
                    a.ljust(val_indent - 3),
                    str(func())) for a, func in p.uuids_.items()
            ])
        ))

        # print project meta
        print('%s' % (
            ('\n' + ' ' * attr_indent).join([
                '%s = %s' % (
                    a.ljust(attr_indent + val_indent - 3),
                    str(func())) for a, func in p.meta_.items()
            ])
        ))

        # print project attributes
        for attr, val in vars(p).items():
            if attr in ['uuids_', 'meta_']:
                continue

            # format the value string
            val_str = str(val).replace('\n', ' ')
            if isinstance(val, str):
                val_str = val_str[:20]

            # print the attribute/value string
            print('         %s = %s' % (
                attr.ljust(attr_indent + val_indent - 7),
                val_str
            ))

        # print versions
        print('%s = [%s])' % (
            (' ' * attr_indent) + 'versions',
            ('\n' + ' ' * (attr_indent + val_indent + 1)).join([
                repr(v) for v in p.versions
            ])
        ))


def describe(ds: Dataset, scope: str = 'dataset'):
    """Describes the dataset/project/version structures."""

    if scope == 'dataset':
        # describe the dataset
        col_width = 13

        # print the attributes in the following order:
        attrs = ['registry', 'name', 'version',
                 'description', 'readme', 'author', 'email']
        for a in attrs:
            val = getattr(ds, a, None)
            print('         %s%s' % (a.ljust(col_width), val))

        # print projects summary info
        print('         projects')
        project_type = project_map.get(ds.registry, DefaultProject).__name__
        print('         %s%s' % ('         type'.ljust(col_width),
                            'list(%s)' % project_type))
        print('         {:}{:,}'.format(
            '         len'.ljust(col_width),
            len(ds.projects)
        ))

    elif scope in ['project', 'version']:
        # describe a project or version
        obj = ds.projects[0]
        if scope == 'version':
            obj = ds.projects[0].versions[0]

        # calculate the width of the first columne
        col_width = max([len(a) for a in vars(obj)]) + 2

        # print uuids & meta vars
        for key in ['uuids', 'meta']:
            print('         %s' % key)
            key_dict = getattr(obj, key + '_')
            if len(key_dict) == 0:
                print('             none')
            for a, func in key_dict.items():
                # convert the lambda function code to a string
                func_str = getsource(func).split(': ', 1)[1].strip()
                print('         %s%s' % (
                    ('         ' + a).ljust(col_width),
                    func_str
                ))

        # print all the attributes
        special_attrs = ['uuids_', 'meta_', 'versions']
        for a in sorted(vars(obj)):
            if a in special_attrs:
                continue

            print('         %s%s' % (
                a.ljust(col_width),
                type(getattr(obj, a)).__name__
            ))

        if scope == 'project':
            # print versions summary info, if applicable
            print('         versions')
            version_type = version_map.get(ds.registry,
                                           DefaultVersion).__name__
            print('         %s%s' % (
                '         type'.ljust(col_width),
                'list(%s)' % version_type
            ))
            print('         {:}{:,}'.format(
                '         len'.ljust(col_width),
                len(obj.versions)
            ))
