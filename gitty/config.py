import os

ROOT = os.environ.get('GITTY_ROOT', '~/.gitty')


def root():
    return os.path.abspath(os.path.expanduser(ROOT))
