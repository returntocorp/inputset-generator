import subprocess
import traceback

from r2c_isg.structures import Dataset


def get_name():
    """Loads the default user name."""

    # only check git user.name for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.name']
        ).decode("utf-8").strip()
    except:
        return None


def get_email():
    """Loads the default user email."""

    # only check git user.email for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.email']
        ).decode("utf-8").strip()
    except:
        return None


def get_dataset(ctx) -> Dataset:
    """Gets the dataset from the CLI context."""
    ds = ctx.obj.get('dataset', None)

    if not ds:
        raise Exception('You must load a dataset before using this command. '
                        'Use the "load", "import", or "restore" commands.')

    return ds


def print_error(err: Exception, debug: bool = False) -> None:
    """Prints all CLI errors."""

    # print the exception stack trace & error message
    if debug:
        traceback.print_tb(err.__traceback__)

    # print the error message
    print('         %s: %s' % (type(err).__name__, err))
