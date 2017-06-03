import contextlib, sys
from . import config, library

ORIGINAL_SYS_PATH = sys.path[:]


def load(gitpath):
    """Load a class at a git path

    @returns the file path to the code."""
    try:
        lib = library.Library(*gitpath.split('/'))
    except Exception as e:
        e.msg += ('for gitpath ' + gitpath,)
        raise

    if not lib.load():
        lib.pull()

    return lib.path


def extend(path=None):
    """Extend sys.path by the resolved paths."""
    if path is None:
        path = config.PATH.split(':')
    sys.path.extend(load(p) for p in path)


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
