import importlib


def _import_symbol(typename):
    try:
        return importlib.import_module(typename)

    except ImportError as e:
        parts = typename.split('.')
        if len(parts) > 1:
            typename = parts.pop()

            # Call import_module recursively.
            namespace = _import_symbol('.'.join(parts))

            try:
                return getattr(namespace, typename)
            except AttributeError:
                pass
        raise


def _make_typename(typename, base_path):
    if base_path and typename.startswith('.'):
        return base_path + typename

    return typename


def import_symbol(typename, base_path=None):
    """
    Import a module or typename within a module from its name.

    Arguments:

    typename: An absolute or relative (starts with a .) Python path
    base_path: If typename is relative, base_path is prepended to it.
    """
    return _import_symbol(_make_typename(typename, base_path))


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

    raise ValueError('No member specified in %s' % fullname)


def import_code(typename, base_path=None):
    typename = _make_typename(typename, base_path)
    symbol = _import_symbol(typename)
    if callable(symbol):
        return symbol

    candidates = vars(symbol)
    names = candidates.keys()
    module_name = typename.split('.')[-1]
    return candidates[guess_name(names, module_name, typename)]
