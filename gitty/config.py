import os

NOLOAD = os.environ.get('GITTY_NOLOAD')
PATH = os.environ.get('GITTY_PATH', '')
ROOT = os.environ.get('GITTY_ROOT', '~/.gitty')

del os
