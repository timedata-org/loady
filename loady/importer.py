import importlib


def import_symbol(typename, base_path=None):
    """
    Import a module or typename within a module from its name.

    Arguments:

    typename: An absolute or relative (starts with a .) Python path
    base_path: If typename is relative, base_path is prepended to it.
    """

    if base_path and typename.startswith('.'):
        typename = base_path + typename

    try:
        return importlib.import_module(typename)

    except ImportError as e:
        parts = typename.split('.')
        if len(parts) > 1:
            typename = parts.pop()

            # Call import_module recursively.
            namespace = import_symbol('.'.join(parts))

            try:
                return getattr(namespace, typename)
            except AttributeError:
                pass
        raise
