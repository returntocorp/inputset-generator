#!/usr/bin/env python3

from click import Choice, argument, command, option
from click_custom import SourceArgument, SortOption

types = {
    'npm': {
        'url': '',
        'lists': {}
    },
    'git': {
        'url': '',
        'lists': {}
    },
    'pypi': {
        'url': '',
        'lists': {
            '5k30days': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.json',
            '5kyear': 'https://hugovk.github.io/top-pypi-packages/top-pypi-packages-365-days.json'
        }
    }
}
sources = {t: [s for s in data['lists']] for t, data in types.items()}


@command()
@argument('type_', type=Choice(types.keys()))
@argument('source', cls=SourceArgument, sources=sources)
@option('--get', type=Choice(['latest', 'major', 'all']))
@option('--sort', cls=SortOption, multiple=True,
        type=Choice(['asc', 'desc', 'popularity', 'date', 'name']))
@option('--head', type=int)
@option('--sample', type=int)
def generate_inputset(type_: str, source: str, get: str, sort: tuple,
                      head: int, sample: int):
    """Generate an input set from one of the named source types."""
    if sort is None:
        print('happy')

    print('%s' % type_)


if __name__ == '__main__':
    generate_inputset()
