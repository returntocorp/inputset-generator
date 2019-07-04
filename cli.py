#!/usr/bin/env python3

import click
from click import argument, option
from click_shell import shell

from dataset import Dataset
from util import get_user_name, get_user_email


@shell(chain=True, prompt='inputset-generator > ',
       intro='Starting input set generator...')
@click.pass_context
def cli(ctx):
    # create the ctx.obj dictionary
    ctx.ensure_object(dict)

    # initialize a dataset and add it to the context
    ctx.obj['dataset'] = Dataset()


@cli.command('meta')
@option('-n', '--name', help='Dataset name.')
@option('-v', '--version', help='Dataset version.')
@option('-d', '--description', help='Description string.')
@option('-r', '--readme', help='Readme string.')
@option('-a', '--author', default=get_user_name,
        help='Author name. Defaults to git user.name.')
@option('-e', '--email', default=get_user_email,
        help='Author email. Defaults to git user.email.')
@click.pass_context
def meta(ctx, name, version, description, readme, author, email):
    # set dataset metadata
    ctx.obj['dataset'].set_meta(name, version, description,
                                readme, author, email)


@cli.command('setreg')
@argument('name')
@click.pass_context
def setreg(ctx, name):
    # set the registry
    ctx.obj['dataset'].set_registry(name)


@cli.command('load')
@argument('handle')
@option('-m', '--metadata', 'load_metadata', is_flag=True)
@option('-v', '--versions', 'load_versions')
@option('-h', '--header', 'fileargs')
@click.pass_context
def load(ctx, handle, load_metadata, load_versions, fileargs):
    ds = ctx.obj['dataset']

    if handle == 'details':
        # filler arg for loading project details/versions without
        # also loading a weblist or file
        pass
    elif '.' in handle:
        # read in a file
        ds.load_file(handle, fileargs)
    else:
        # download a weblist
        ds.load_weblist(handle)

    if load_metadata:
        # load project details from the registry
        ds.load_project_metadata()

    if load_versions:
        # load project versions from the registry
        ds.load_project_versions(load_versions)


@cli.command('save')
@argument('filepath')
@click.pass_context
def save(ctx, filepath):
    # save to json file
    ctx.obj['dataset'].save_json(filepath)


@cli.command('head')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def head(ctx, n, on_projects):
    # trim all but the first n projects
    ctx.obj['dataset'].head(n, on_projects)


@cli.command('sort')
@argument('params', type=str)
@click.pass_context
def sort(ctx, params):
    ctx.obj['dataset'].sort(params.split())


@cli.command('sample')
@argument('n', type=int)
@option('-p/-v', '--projects/--versions', 'on_projects', default=True)
@click.pass_context
def sample(ctx, n, on_projects):
    # sample n projects
    ctx.obj['dataset'].sample(n, on_projects)


if __name__ == '__main__':
    cli()
