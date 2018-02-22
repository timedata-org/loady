import importlib


def _import(typename, base_path):
    if not typename:
        raise ValueError

    assert isinstance(typename, str), str(typename)
    assert not base_path or isinstance(base_path, str), str(base_path)
    def imp(typename):
        try:
            return importlib.import_module(typename)

        except ImportError as e:
            parts = typename.split('.')
            if len(parts) > 1:
                module = parts.pop()

                # Call import_module recursively for the parent module
                namespace = imp('.'.join(parts))
                try:
                    return getattr(namespace, module)
                except AttributeError:
                    pass
            raise

        except:
            raise ImportError(
                'Bad path or typename', name=typename, path=base_path)

    if not base_path:
        return typename, imp(typename)

    if typename.startswith('.'):
        typename = base_path + typename
        return typename, imp(typename)

    try:
        return typename, imp(typename)

    except:
        typename = base_path + '.' + typename
        return typename, imp(typename)


def import_symbol(typename, base_path=None):
    """
    Import a module, or a typename within a module from its name.

    Arguments:

    typename: An absolute or relative (starts with a .) Python path
    base_path: If typename is relative, base_path is prepended to it.
    """
    _, symbol = _import(typename, base_path)
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

    raise ValueError('No member specified in %s' % fullname)


def import_code(typename, base_path=None):
    typename, symbol = _import(typename, base_path)
    if callable(symbol):
        return symbol

    candidates = vars(symbol)
    names = candidates.keys()
    module_name = typename.split('.')[-1]
    return candidates[guess_name(names, module_name, typename)]
