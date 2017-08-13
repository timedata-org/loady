import os
from . import files

"""
A list of configuration values for loady that are read from environment
variables and can also be set programmatically.
"""

CACHE_DISABLE = os.environ.get('LOADY_CACHE_DISABLE', False)
PATH = os.environ.get('LOADY_PATH', '')
CACHE_DIRECTORY = os.environ.get('LOADY_CACHE_DIRECTORY', '~/.loady')
WHITELIST = os.environ.get('LOADY_WHITELIST', '~/.loady_whitelist')

USE_WHITELIST = True
WHITELIST_PROMPT = True
LIBRARY_PREFIX = '//git/'


def cache():
    return files.canonical(CACHE_DIRECTORY)


def whitelist():
    return files.canonical(WHITELIST)
