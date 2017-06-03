import contextlib, sys
from . import config, library

ORIGINAL_SYS_PATH = sys.path[:]


def resolve(subpath):
    """Resolve from a git path.

    @returns the file path to the code."""
    lib = library.Library(*subpath.split('/', 5))

    if not lib.load():
        lib.pull()

    return lib.path


def extend(path=None):
    """Extend sys.path by the resolved paths."""
    if path is None:
        path = config.PATH.split(':')
    sys.path.extend(resolve(p) for p in path)


@contextlib.contextmanager
def extender(path=None):
    """A context that extends sys.path and reverts it after the context is
       complete."""
    old_path = sys.path[:]
    extend(path=path)

    try:
        yield
    finally:
        sys.path = old_path
