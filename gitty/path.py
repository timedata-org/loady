import contextlib, sys
from . import library

GIT_INTRO = '//git/'


def resolve(path, root=None):
    """If the path starts with //git, try to load it from a git repo.
    @returns the file path to the code."""
    if not path.startswith(GIT_INTRO):
        return path

    url = path[len(GIT_INTRO):]
    lib = library.Library(*url.split('/', 5), root=root)

    if not lib.load():
        lib.pull()

    return lib.path


def extend(paths, root=None):
    """Extend sys.path by the resolved paths."""
    try:
        paths = (paths or '').split(':')
    except:
        pass

    sys.path.extend(resolve(p, root=root) for p in split(paths))


@contextlib.contextmanager
def extender(paths, root=None):
    """A context that extends sys.path and reverts it after the context is
       complete."""
    old_path = sys.path[:]
    extend(paths, root=root)

    try:
        yield
    finally:
        sys.path = old_path
