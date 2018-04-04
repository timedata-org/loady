import functools
from . import data, importer, whitelist


def load_location(url, base_path=None, module=False):
    """
    Read a single Python file in as code and extract members from it.

    Args:
        url -- a URL either absolute (contains ':') or relative
        base_path -- if url is relative, base_path is prepended to it.

    The resulting URL needs to look something like this:
        https://github.com/foo/bar/blob/master/bibliopixel/myfile.MyClass
    """
    if base_path and ':' not in url:
        slashes = base_path.endswith('/') + url.startswith('/')
        if slashes == 0:
            url = base_path + '/' + url
        elif slashes == 1:
            url = base_path + url
        else:
            url = base_path[:-1] + url

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
        names = local

    if python_path and python_path[0] == 'py':
        python_path.pop(0)

    if not python_path:
        if module:
            return local
        python_path = [importer.guess_name(names, filename, url)]

    first, *rest = python_path

    try:
        result = local[first]
    except:
        raise AttributeError(first)

    for r in rest:
        result = getattr(result, r)

    return result


@functools.lru_cache()
def load_code(name, base_path=None, recurse=False):
    """Load executable code from a URL or a path"""
    if '/' in name:
        return load_location(name, base_path, module=False)

    return importer.import_code(name, base_path, recurse=recurse)


@functools.lru_cache()
def load(name, base_path=None):
    """Load a module from a URL or a path"""
    if '/' in name:
        return load_location(name, base_path, module=True)

    return importer.import_symbol(name, base_path)


load_module = load


def cache_clear():
    load.cache_clear()
    data.cache_clear()
