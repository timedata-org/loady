import contextlib, sys
from . import config, library

ORIGINAL_SYS_PATH = sys.path[:]
PREFIX = '//git/'


def load(gitpath, prefix=PREFIX):
    """
    Load a Python library from a git path.

    @returns the file path to the code.
    """
    if not gitpath.startswith(prefix):
        return gitpath

    path = gitpath[len(prefix):]
    try:
        lib = library.Library(*path.split('/'))
    except Exception as e:
        e.msg += ('for path ' + gitpath,)
        raise

    lib.load() or lib.pull()
    return lib.path


def extend(path=None, prefix=PREFIX):
    """Extend sys.path by a list of git paths."""
    if path is None:
        path = config.PATH
    try:
        path = path.split(':')
    except:
        pass

    sys.path.extend(load(p, prefix) for p in path)


@contextlib.contextmanager
def extender(path=None):
    """A context that temporarily extends sys.path and reverts it after the
       context is complete."""
    old_path = sys.path[:]
    extend(path, prefix)

    try:
        yield
    finally:
        sys.path = old_path
