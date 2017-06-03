import os
from . import files

NOCACHE = os.environ.get('GITTY_NOCACHE', False)
PATH = os.environ.get('GITTY_PATH', '')
ROOT = os.environ.get('GITTY_ROOT', '~/.gitty')


def root():
    return files.canonical(ROOT)
