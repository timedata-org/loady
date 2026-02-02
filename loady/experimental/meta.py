import importlib.abc, importlib.machinery, sys


class RedirectFinder(importlib.machinery.PathFinder):
    def __init__(self, name, path):
        self.name = name
        assert not name.endswith('.')
        self.path = path

    def find_spec(self, fullname, paths, target=None):
        print('!!', self.name, fullname, paths, target)
        if fullname == self.name:
            res = super().find_spec(fullname, paths, target=target)
            print('!!??', res)
            return res


class TestLoader(importlib.abc.SourceLoader):
    pass


# class TestFinder(importlib.abc.MetaPathFinder):


def install():
    f = RedirectFinder('loady.remote', '/development/loady/loady/test')
    sys.meta_path.insert(0, f)


if __name__ == '__main__':
    install()
    from loady.remote import toast

    print(toast.TOAST)
