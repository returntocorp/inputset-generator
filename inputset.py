#!/usr/bin/env python3

from click import Argument, Choice, Option, Path, argument, command, option

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


class SourceArgument(Argument):
    """A custom argument that accepts either a valid file path string or
    the name of a downloadable package list for the specified type."""

    def __init__(self, *args, **kwargs):
        # init a choice of either <path> or <source>; this Choice will
        # be overriden by handle_parse_result()
        kwargs['type'] = Choice(['<path>', '<source>'])
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts: dict, args: list):
        if '.' in opts['source']:
            # source is likely a file path
            self.type = Path(exists=True)
            return super().handle_parse_result(ctx, opts, args)
        else:
            # source is likely a web list
            self.type = Choice(sources[opts['type_']])
            return super().handle_parse_result(ctx, opts, args)


class SortOption(Option):
    """A custom option that accepts an asc/desc value followed by any
    number of sort criteria."""

    def __init__(self, *args, **kwargs):
        self.parser_process = None

        kwargs['type'] = Choice(['asc', 'desc', 'popularity', 'date', 'name'])
        kwargs['multiple'] = True
        super().__init__(*args, **kwargs)

    def add_to_parser(self, parser, ctx):
        """Parses an unlimited number of sort args."""
        # Simplified version of: https://stackoverflow.com/questions/48391777/nargs-equivalent-for-options-in-click
        def parser_process(value, state):
            # grab everything up to the next option
            value = [value]
            while state.rargs and not state.rargs[0].startswith('-'):
                value.append(state.rargs.pop(0))

            # call the actual process()
            self.parser_process(value, state)

        super().add_to_parser(parser, ctx)

        # do some magic...
        name = self.opts[0]
        our_parser = parser._long_opt.get(name) or \
                     parser._short_opt.get(name)
        our_parser.action = 'append'
        self.parser_process = our_parser.process
        our_parser.process = parser_process

    def handle_parse_result(self, ctx, opts: dict, args: list):
        # convert sort opt from list(list()) to list()
        if opts.get('sort'):
            opts['sort'] = opts['sort'][0]
        return super().handle_parse_result(ctx, opts, args)


@command()
@argument('type_', type=Choice(types.keys()))
@argument('source', cls=SourceArgument)
@option('--get', type=Choice(['latest', 'major', 'all']))
@option('--sort', cls=SortOption)
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
