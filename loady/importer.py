import importlib


def _import(name, path):
    def imp(tn):
        try:
            return importlib.import_module(tn)
        except:
            parts = tn.split('.')
            if len(parts) <= 1:
                raise
            module = parts.pop()

            namespace = imp('.'.join(parts))
            return getattr(namespace, module)

    try:
        if not path:
            return name, imp(name)

        if name.startswith('.'):
            pname = path + name
            return pname, imp(pname)

        try:
            return name, imp(name)
        except:
            pname = '%s.%s' % (path, name)
            return pname, imp(pname)
    except:
        msg = "Cannot import symbol '%s'" % name
        raise ImportError(msg, name=name, path=path)


def import_symbol(name=None, path=None, typename=None, base_path=None):
    """
    Import a module, or a typename within a module from its name.

    Arguments:

    name: An absolute or relative (starts with a .) Python path
    path: If name is relative, path is prepended to it.
    base_path: (DEPRECATED) Same as path
    typename: (DEPRECATED) Same as path
    """
    _, symbol = _import(name or typename, path or base_path)
    return symbol


def guess_name(names, module_name, fullname):
    names = [n for n in names if not n.startswith('_')]

    if len(names) == 1:
        return names[0]

    if module_name in names:
        return module_name

    def canonical(symbol):
        return symbol.lower().replace('_', '')

    matches = [n for n in names if canonical(n) == canonical(module_name)]
    if len(matches) == 1:
        return matches[0]

    names.sort()
    matches.sort()
    raise ValueError(GUESS_ERROR.format(**locals()))


def import_code(
        name=None, path=None, typename=None, base_path=None, recurse=False):
    name, symbol = _import(name or typename, path or base_path)

    while not callable(symbol):
        candidates = vars(symbol)
        names = candidates.keys()
        module_name = name.split('.')[-1]

        symbol = candidates[guess_name(names, module_name, name)]
        if not recurse:
            return symbol

    return symbol


GUESS_ERROR = """
No member specified in fullname = {fullname}:
names = {names}
module_name = {module_name}
matches = {matches}
"""
