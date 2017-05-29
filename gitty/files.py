import contextlib, os, re, shutil, unicodedata


def canonical(filename):
    return os.path.abspath(os.path.expanduser(filename))


def sanitize(value):
    """Strips all undesirable characters out of potential file paths."""
    # From https://stackoverflow.com/a/295466/43839, except that we allow
    # the / character because we accept file paths.
    value = unicodedata.normalize('NFKD', value)
    value = value.strip().lower()
    value = re.sub('[^\w\s-/]', '', value)
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
            shutil.rmtree(dirname)
        raise
