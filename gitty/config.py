import os
from . import files

NOCACHE = os.environ.get('GITTY_NOCACHE', False)
PATH = os.environ.get('GITTY_PATH', '')
CACHE = os.environ.get('GITTY_CACHE', '~/.gitty')

def cache():
    return files.canonical(CACHE)
