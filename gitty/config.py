import os
from . import files

CACHE_DISABLE = os.environ.get('GITTY_CACHE_DISABLE', False)
PATH = os.environ.get('GITTY_PATH', '')
CACHE_DIRECTORY = os.environ.get('GITTY_CACHE_DIRECTORY', '~/.gitty')


def cache():
    return files.canonical(CACHE_DIRECTORY)
