import os

NOCACHE = os.environ.get('GITTY_NOCACHE', False)
PATH = os.environ.get('GITTY_PATH', '')
ROOT = os.environ.get('GITTY_ROOT', '~/.gitty')

del os
