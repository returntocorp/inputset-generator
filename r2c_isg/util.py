import re
import subprocess
import traceback
from typing import Optional


def get_name() -> Optional[str]:
    """Loads the default user name."""

    # only check git user.name for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.name']
        ).decode("utf-8").strip()
    except:
        return None


def get_email() -> Optional[str]:
    """Loads the default user email."""

    # only check git user.email for now
    try:
        return subprocess.check_output(
            ['git', 'config', '--get', 'user.email']
        ).decode("utf-8").strip()
    except:
        return None


def get_str(key: str, d: dict) -> str:
    """Helper function to get a string value from a dict."""
    val = d.get(key)
    return val if isinstance(val, str) else ''


def name_from_url(url: str, pattern) -> Optional[str]:
    match = re.match(pattern, url)
    return match['name'] if match else None


def url_from_name(name: str, url_literal) -> Optional[str]:
    return url_literal.format(name) if name else None


def get_dataset(ctx):
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

