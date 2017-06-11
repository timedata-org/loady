import contextlib, os, re, shutil, unicodedata


def canonical(filename):
    """Given a filename, return an absolute path with usenames expanded."""

    return os.path.abspath(os.path.expanduser(filename))


def sanitize(value):
    """Strips all undesirable characters out of potential file paths."""

    value = unicodedata.normalize('NFKD', value)
    value = value.strip()
    value = re.sub('[^./\w\s-]', '', value)
    value = re.sub('[-\s]+', '-', value)

    return value


@contextlib.contextmanager
def remove_on_exception(dirname, remove=True):
    """Creates a directory, yields to the caller, and removes that directory
       if an exception is thrown."""
    os.makedirs(dirname)
    try:
        yield
    except:
        if remove:
            shutil.rmtree(dirname, ignore_errors=True)
        raise
