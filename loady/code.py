import functools
from . import data, importer, whitelist


def _guess_name(names, filename, url):
    if len(names) == 1:
        return names[0]

    if filename in names:
        return filename

    def canonical(symbol):
        return symbol.lower().replace('_', '')

    matches = [n for n in names if canonical(n) == canonical(filename)]
    if len(matches) == 1:
        return matches[0]

    raise ValueError('No member specified in %s' % url)


def load_location(url):
    """
    Read a single Python file in as code and extract members from it.

    Args:
        url: a URL looking like
             https://github.com/foo/bar/blob/master/bibliopixel/myfile.MyClass

    """
    slash = url.rfind('/')
    url_root, filepath = url[:slash + 1], url[slash + 1:]
    filename, *python_path = filepath.split('.')

    whitelist.check_url(url_root)

    file_url = url_root + filename + '.py'
    source = data.load(file_url, False)
    compiled = compile(source, file_url, mode='exec')
    local = {}
    exec(compiled, local)

    try:
        names = local['__all__']
    except KeyError:
        names = [k for k in local if not k.startswith('_')]

    if python_path and python_path[0] == 'py':
        python_path.pop(0)

    first, *rest = python_path or [_guess_name(names, filename, url)]
    try:
        result = local[first]
    except:
        raise AttributeError(first)

    for r in rest:
        result = getattr(result, r)

    return result


@functools.lru_cache()
def load(name):
    if '/' in name:
        return load_location(name)

    return importer.import_symbol(name)


def cache_clear():
    load.cache_clear()
    data.cache_clear()
