from click import Argument, Option, Choice, Path


class SourceArgument(Argument):
    """A custom argument that accepts either a valid file path string or
    the name of a downloadable package list for the specified type."""

    def __init__(self, *args, **kwargs):
        # choices is of type dict(str: list), mapping types to lists of
        # names of downloadable package lists
        self.sources = kwargs.pop('sources')

        # init a choice of either <path> or <source>; this Choice will
        # be overriden by handle_parse_result()
        kwargs['type'] = Choice(['<filepath>', '<listname>'])
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts: dict, args: list) -> tuple:
        # set the parser type
        if '.' in opts['source']:
            # source is likely a file path
            self.type = Path(exists=True)
            source_type = 'file'

        else:
            # source is likely a weblist name
            self.type = Choice(self.sources[opts['registry']])
            source_type = 'weblist'

        # parse the argument
        parsed = super().handle_parse_result(ctx, opts, args)

        # add source type to params to be passed to generate_inputset
        value_key = 'path' if source_type == 'file' else 'name'
        ctx.params['source'] = {'type': source_type,
                                value_key: ctx.params['source']}

        return parsed


class SortOption(Option):
    """
    A custom option that accepts an asc/desc value followed by any
    number of sort criteria.

    This code is loosely based on the following example:
    https://stackoverflow.com/questions/48391777/nargs-equivalent-for-options-in-click
    """

    def __init__(self, *args, **kwargs):
        self.original_process = None
        super().__init__(*args, **kwargs)

    def add_to_parser(self, parser, ctx):
        """Parses an unlimited number of sort args by overriding the
        default add_to_parser() function and pulling additional params
        off the command line until a new option (beginning with '-')
        is encountered."""

        def override_process(value: str, state):
            """Overrides the original parser.process and loops over the
            remaining args, adding them to the values for the --sort
            option until a new option is encountered."""

            # grab everything up to the next option (starts with '-')
            value = [value]
            # state.rargs contains *all* remaining args
            while state.rargs and not state.rargs[0].startswith('-'):
                value.append(state.rargs.pop(0))

            # call the original parser process()
            self.original_process(value, state)

        # first call the original add_to_process to add the --sort
        # option to the list of parsed options
        super().add_to_parser(parser, ctx)

        # get the original parser process for the --sort option
        name = self.opts[0]
        # long_opt or short_opt supports both -l and --long options
        parser = parser._long_opt.get(name) or \
                 parser._short_opt.get(name)

        # store the original parser.process...
        self.original_process = parser.process
        # ... and replace it with our own
        parser.process = override_process

    def handle_parse_result(self, ctx, opts: dict, args: list) -> tuple:
        # convert sort opt from list(list()) to list(); needed due to
        # overriding the option's default add_to_parser()
        if opts.get('sort'):
            opts['sort'] = opts['sort'][0]

        return super().handle_parse_result(ctx, opts, args)
