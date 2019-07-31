#!/usr/bin/env python3

import os
import shutil
import click
import json
import atexit
import webbrowser
from copy import deepcopy
from datetime import timedelta
from click import argument, option, Choice, Path
from click_shell import shell

from r2c_isg.structures import Dataset
from r2c_isg.structures.projects import project_map
from r2c_isg.util import get_dataset, print_error
from r2c_isg.loaders.file import fileloader_map
from r2c_isg.loaders.weblist import weblistloader_map


DEBUG = False
# store meta/api settings if a dataset hasn't yet been loaded
TEMP_SETTINGS = dict()
TEMP_DIR = '.tmp/'


@shell(chain=True, prompt='r2c-isg> ')
@option('-d', '--debug', is_flag=True, default=False)
@option('-q', '--quiet', is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug, quiet):
    # set debug settings
    global DEBUG
    DEBUG = debug

    # create the ctx.obj dictionary
    ctx.ensure_object(dict)

    # create the temp dir
    if not os.path.isdir(TEMP_DIR):
        os.mkdir(TEMP_DIR)

    # register the cleanup callback on exit
    atexit.register(cleanup)

    # print the welcome screen
    if not quiet:
        print('=' * 100)
        print('Welcome to the R2C input set generator! We currently support '
              'the following registries: %s. For more info on specific '
              'commands, type "help [COMMAND]". For a quick start, try the '
              'following command sequences:\n\n'
              ''
              'Load the top 5,000 pypi projects by downloads in the last 365 '
              'days, sort by descending number of downloads, trim to the top '
              '100 most downloaded, download project metadata and all '
              'versions, and generate an input set json.\n'
              '    load pypi top5kyear\n    sort "desc download_count"\n'
              '    trim 100\n    get -mv all\n    set-meta -n test -v 1.0\n'
              '    export inputset.json\n\n'
              ''
              'Load all npm projects, sample 100, download the latest '
              'versions, and generate an input set json.\n'
              '    load npm allbydependents\n    sample -s abc123 100\n'
              '    get -v latest\n    set-meta -n test -v 1.0\n'
              '    export inputset.json\n\n'
              ''
              'Load a csv containing github urls and commit hashes, get '
              'project metadata and the latest versions, generate an input '
              'set json of type GitRepoCommit, remove all versions, and '
              'generate an input set json of type GitRepo.\n\n'
              '    load --columns "url v.commit" '
              'github list_of_github_urls_and_commits.csv\n'
              '    get -mv latest\n    set-meta -n test -v 1.0\n'
              '    export inputset_1.json\n    trim -v 0\n'
              '    export inputset_2.json\n\n'
              ''
              'To hide this message when loading the shell, add the quiet '
              '("-q") flag.'
              '' % ', '.join(list(project_map)))
        print('=' * 100)


@cli.command('and')
def spacer():
    """Does absolutely nothing, but sure does make command strings more
    readable! :)"""
    pass


weblist_options = '; '.join(['%s: %s' % (
    name,
    ', '.join(list(cls.weblists()))
) for name, cls in weblistloader_map.items()])


@cli.command('load', help='Generates a dataset from a weblist name or file '
                          'path.\n\nSupported file types are: %s. Note: there '
                          'are no default json parsers; you must write your '
                          'own.\n\nValid weblist names are %s.' %
                          (', '.join(list(fileloader_map)), weblist_options))
@argument('registry', type=Choice(list(project_map) + ['noreg']))
@argument('name_or_path')
@option('-c', '--columns', 'fileargs', type=str,
        help='Space-separated list of column names in a csv. Overrides default '
             'headers (name and version), as well as any headers listed in the '
             "file (headers in  files begin with a '!'). Recognized keywords: "
             'name, url, org, v.commit, v.version. Example usage: --headers '
             '"name v.version".')
@option('-p', '--parser', 'fileargs', type=str,
        help='Handle for a custom-build json parser. No json parsers '
             'are implemented by default.')
@click.pass_context
def load(ctx, registry, name_or_path, fileargs):
    """Generates a dataset from a weblist name or file path."""
    backup_ds = None
    
    try:
        backup_ds = deepcopy(ctx.obj.get('dataset', None))
        
        if registry == 'noreg':
            registry = None

        global TEMP_SETTINGS

        if '.' in name_or_path:
            # read in a file (fileargs is either a header string for csv
            # or a parser handle for json)
            ds = Dataset.load_file(name_or_path, registry,
                                   fileargs=fileargs, **TEMP_SETTINGS)

        else:
            # download a weblist
            ds = Dataset.load_weblist(name_or_path, registry, **TEMP_SETTINGS)

        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)
        
        # silently restore the dataset
        ctx.obj['dataset'] = backup_ds


@cli.command('restore', help='Restores a dataset from a pickle file. Use '
                             'the "backup" command to pickle the dataset.')
@argument('filepath', type=Path(exists=True))
@click.pass_context
def restore(ctx, filepath):
    """Restores a pickled dataset file."""
    backup_ds = None

    try:
        backup_ds = deepcopy(ctx.obj.get('dataset', None))

        ds = Dataset.restore(filepath)
        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        global TEMP_SETTINGS
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)

        # silently restore the dataset
        ctx.obj['dataset'] = backup_ds


@cli.command('backup', help='Backs up the full dataset to a pickle file. Use '
                            'the "restore" command to restore the file.')
@argument('filepath', type=Path(), default=None)
@click.pass_context
def backup(ctx, filepath):
    """Pickles the complete dataset."""
    try:
        ds = get_dataset(ctx)
        ds.backup(filepath)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('import', help='Imports a dataset from an R2C input set json. '
                            'Use the "export" command to export an input set.')
@argument('registry', type=Choice(list(project_map) + ['noreg']))
@argument('filepath', type=Path(exists=True))
@click.pass_context
def import_(ctx, registry, filepath):
    """Imports an input set json file."""
    backup_ds = None

    try:
        backup_ds = deepcopy(ctx.obj.get('dataset', None))

        if registry == 'noreg':
            registry = None

        global TEMP_SETTINGS

        ds = Dataset.import_inputset(filepath, registry, **TEMP_SETTINGS)
        ctx.obj['dataset'] = ds

        # reset the temporary api/metadata dict
        TEMP_SETTINGS = dict()

    except Exception as e:
        print_error(e, DEBUG)

        # silently restore the dataset
        ctx.obj['dataset'] = backup_ds


@cli.command('export', help='Exports a dataset to an R2C input set json. '
                            'Use the "import" command to import an input set.')
@argument('filepath', type=Path(), default=None)
@click.pass_context
def export(ctx, filepath):
    """Export a dataset to an input set json."""
    try:
        ds = get_dataset(ctx)
        ds.export_inputset(filepath)

    except Exception as e:
        print_error(e, DEBUG)


@cli.command('set-meta', help="Sets the dataset's metadata.")
@option('-n', '--name', type=str,
        help='Input set name. Must be set before the dataset can be exported.')
@option('-v', '--version', type=str,
        help='Input set version. Must be set before the dataset can be exported.')
@option('-d', '--description', type=str, help='Description string.')
@option('-r', '--readme', type=str, help='Markdown-formatted readme string.')
@option('-a', '--author', type=str,
        help='Author name. Defaults to git user.name.')
@option('-e', '--email', type=str,
        help='Author email. Defaults to git user.email.')
@click.pass_context
def set_meta(ctx, name, version, description, readme, author, email):
    """Sets dataset metadata."""
    backup_ds = None

    try:
        ds = ctx.obj.get('dataset', None)
        backup_ds = deepcopy(ds)

        if ds:
            # update dataset's metadata
            ds.update(name=name, version=version, description=description,
                      readme=readme, author=author, email=email)

        else:
            global TEMP_SETTINGS
            if name: TEMP_SETTINGS['name'] = name
            if version: TEMP_SETTINGS['version'] = version
            if description: TEMP_SETTINGS['description'] = description
            if readme: TEMP_SETTINGS['readme'] = readme
            if author: TEMP_SETTINGS['author'] = author
            if email: TEMP_SETTINGS['email'] = email

        # print the outcome
        settings = []
        if name: settings.append('name')
        if version: settings.append('version')
        if description: settings.append('description')
        if readme: settings.append('readme')
        if author: settings.append('author')
        if email: settings.append('email')
        set_str = ', '.join([s for s in settings if s])
        print("         Set the dataset's %s." % set_str)

    except Exception as e:
        print_error(e, DEBUG)

        # silently restore the dataset
        ctx.obj['dataset'] = backup_ds


@cli.command('set-api', help='Sets API-specific settings.')
@option('-d', '--cache_dir', type=Path(),
        help='The path to the requests cache. Defaults to ./.requests_cache.')
@option('-t', '--cache_timeout', type=int,
        help='The number of days before a cached request goes stale.')
@option('-n', '--nocache', is_flag=True,
        help='Disables request caching for this dataset.')
@option('-g', '--github_pat', type=str,
        help='A github personal access token, used to increase the max '
             'allowed hourly request rate from 60/hr to 5,000/hr. For '
             'instructions on how to obtain a token, see: https://help.'
             'github.com/en/articles/creating-a-personal-access-token-'
             'for-the-command-line.')
@click.pass_context
def set_api(ctx, cache_dir, cache_timeout, nocache, github_pat):
    """Sets API settings."""
    backup_ds = None

    try:
        ds = ctx.obj.get('dataset', None)
        backup_ds = deepcopy(ds)

        # convert cache timeout string to timedelta
        if cache_timeout:
            cache_timeout = timedelta(days=cache_timeout)

        if ds and ds.api:
            # update the api
            ds.api.update(cache_dir=cache_dir,
                          cache_timeout=cache_timeout,
                          nocache=nocache,
                          github_pat=github_pat)

        else:
            # no ds/api; save the settings for when there is one
            global TEMP_SETTINGS
            if cache_dir: TEMP_SETTINGS['cache_dir'] = cache_dir
            if cache_timeout: TEMP_SETTINGS['cache_timeout'] = cache_timeout
            if nocache: TEMP_SETTINGS['nocache'] = nocache
            if github_pat: TEMP_SETTINGS['github_pat'] = github_pat

        # print the outcome
        settings = []
        if cache_dir: settings.append('cache_dir')
        if cache_timeout: settings.append('cache_timeout')
        if nocache: settings.append('nocache')
        if github_pat: settings.append('github_pat')
        set_str = ', '.join([s for s in settings if s])
        print("    Set the api's %s." % set_str)

    except Exception as e:
        print_error(e, DEBUG)

        # silently restore the dataset
        ctx.obj['dataset'] = backup_ds


@cli.command('get')
@option('-m', '--metadata', is_flag=True,
        help='Downloads project metadata.')
@option('-v', '--versions', type=Choice(['all', 'latest']),
        help='Downloads project versions.')
@click.pass_context
def get(ctx, metadata, versions):
    """Downloads project and version information."""
    backup_ds = None
    rolled_back = False

    # load project metadata
    if metadata:
        try:
            ds = get_dataset(ctx)
            backup_ds = deepcopy(ds)

            ds.get_projects_meta()

        except Exception as e:
            print_error(e, DEBUG)

            # roll back the db
            ctx.obj['dataset'] = backup_ds
            rolled_back = True

    # load project versions
    if versions:
        try:
            ds = get_dataset(ctx)
            backup_ds = deepcopy(ds)

            ds.get_project_versions(historical=versions)

        except Exception as e:
            print_error(e, DEBUG)

            # roll back the db
            ctx.obj['dataset'] = backup_ds
            rolled_back = True

    if rolled_back:
        print('         The dataset was not modified.')


@cli.command('trim', help='Trims to the first N projects (default) or '
                          'the first N versions per project.')
@argument('n', type=int)
@option('-v', '--versions', 'on_versions', is_flag=True, default=False,
        help='Trim to N versions per project.')
@click.pass_context
def trim(ctx, n, on_versions):
    """Trims projects or versions from a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.trim(n, on_versions)

    except Exception as e:
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('         The dataset was not modified.')


@cli.command('sort',
             help='Sorts the projects and versions based on a space-separated '
                  'string of keywords. Valid keywords include:\n\n'
                  '- Any project attributes\n\n'
                  '- Any version attributes (prepend "v." to the attribute '
                  'name)\n\n'
                  '- Any uuids (prepend "uuids." to the uuid name\n\n'
                  '- Any meta values (prepend "meta." to the meta name\n\n'
                  '- The words "asc" and "desc"\n\n'
                  'All values are sorted in ascending order by default. The '
                  'first keyword in the string is the primary sort key, the '
                  'next the secondary, and so on.\n\n'
                  'Example: The string "uuids.name meta.url downloads desc '
                  'v.version_str v.date" would sort the dataset by ascending '
                  'project name, url, and download count; and descending '
                  'version string and date--assuming those keys exist.\n\n'
                  'To determine all sortable attributes, '
                  'use the "show" command.')
@argument('keywords_string', type=str)
@click.pass_context
def sort(ctx, keywords_string):
    """Sorts a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.sort(keywords_string.split())

    except Exception as e:
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('         The dataset was not modified.')


@cli.command('sample', help='Samples N projects (default) '
                            'or N versions per project.')
@argument('n', type=int)
@option('-v', '--versions', 'on_versions', is_flag=True, default=False,
        help='Sample N versions per project.')
@option('-s', '--seed', type=str, help='Sets the random seed.')
@click.pass_context
def sample(ctx, n, on_versions, seed):
    """Samples projects or versions from a dataset."""
    backup_ds = None

    try:
        ds = get_dataset(ctx)
        backup_ds = deepcopy(ds)

        ds.sample(n, on_versions, seed)

    except Exception as e:
        print_error(e, DEBUG)

        # roll back the db
        ctx.obj['dataset'] = backup_ds
        print('         The dataset was not modified.')


@cli.command('show', help='Jsonifies the dataset and opens it in the '
                          'native json viewer.')
@click.pass_context
def show(ctx):
    """Opens the complete dataset as a json for easier review."""
    try:
        ds = get_dataset(ctx)
        data_dict = ds.to_json()

        # save & open temp file
        filepath = TEMP_DIR + 'jsonify.json'
        with open(filepath, 'w') as file:
            json.dump(data_dict, file, indent=4)
            fullpath = os.path.realpath(filepath)
            webbrowser.open_new('file://' + fullpath)

    except Exception as e:
        print_error(e, DEBUG)


def cleanup():
    """Cleanup on exit."""

    # delete the tem dir
    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


if __name__ == '__main__':
    cli()
