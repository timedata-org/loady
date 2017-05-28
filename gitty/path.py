import contextlib, sys
from . import library

GIT_INTRO = '//git/'


def resolve(path):
    """If the path starts with //git, try to load it from a git repo.
    @returns the file path to the code."""
    if not path.startswith(GIT_INTRO):
        return path

    url = path[len(GIT_INTRO):]
    lib = library.Library(*url.split('/', 6))

    if not lib.load():
        lib.pull()

    return lib.path


def extend(paths):
    """Extend sys.path by the resolved paths."""
    try:
        paths = (paths or '').split(':')
    except:
        pass

    sys.path.extend(resolve(p) for p in split(paths))


@contextlib.contextmanager
def extender(paths):
    """A context that extends sys.path and reverts it after the context is
       complete."""
    old_path = sys.path[:]
    extend(paths)

    try:
        yield
    finally:
        sys.path = old_path
