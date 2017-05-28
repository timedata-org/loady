import contextlib, unicodedata


def sanitize(value):
    """Strips all undesirable characters out of potential file paths."""
    # From https://stackoverflow.com/a/295466/43839, except that we allow
    # the / character because we accept file paths.
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-/]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value


@contextlib.contextmanager
def remove_on_exception(dirname, remove=True):
    """Creates a directory, yields to the caller, and removes that directory,
       if an exception is thrown."""
    os.makedirs(dirname)
    try:
        yield
    except:
        if remove:
            shutil.rmtree(dirname)
        raise
