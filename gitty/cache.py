import git, os, shutil
from . import files, config


def cache_root():
    return files.canonical(config.root)


def clear():
    shutil.rmtree(cache_root(), ignore_errors=True)


def fill_python_directories(*path):
    pass
