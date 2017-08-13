import contextlib, sys
from . import config, library


def extend(path=None):
    """Extend sys.path by a list of git paths."""
    if path is None:
        path = config.PATH
    try:
        path = path.split(':')
    except:
        pass

    sys.path.extend([library.to_path(p) for p in path])


@contextlib.contextmanager
def extender(path=None):
    """A context that temporarily extends sys.path and reverts it after the
       context is complete."""
    old_path = sys.path[:]
    extend(path)

    try:
        yield
    finally:
        sys.path = old_path
