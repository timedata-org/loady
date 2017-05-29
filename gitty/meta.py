import importlib.abc, sys


class TestFinder(importlib.abc.MetaPathFinder):
    def __init__(self, prefix='gitty.imp'):
        self.prefix = prefix

    def find_spec(self, fullname, paths, target=None):
        if fullname.startswith('gitty.imp'):
            print(fullname, paths, target)


def install():
    if sys.meta_path and isinstance(sys.meta_path[0], TestFinder):
        sys.meta_path.pop(0)
    sys.meta_path.insert(0, TestFinder())
