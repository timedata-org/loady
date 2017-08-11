import math, unittest
from gitty import config, load, load_symbol, whitelist

SIMPLE_FILE = """
FOO = 1
BAR = 2

py = 7

class Sim_Ple:
    MEMBER = 4
    py = 3
"""

MOCK_FILES = {
    'foo/bar/trivial.py': 'A = 1',
    'foo/bar/simple.py': SIMPLE_FILE,
}


def mock_load(url):
    def request(file_url, json):
        return MOCK_FILES[file_url]

    use_whitelist, config.USE_WHITELIST = config.USE_WHITELIST, False
    load_symbol.raw.request, raw_request = request, load_symbol.raw.request
    try:
        return load(url)
    finally:
        config.USE_WHITELIST = use_whitelist
        load_symbol.raw.request = raw_request


class LoadTest(unittest.TestCase):
    def test_trivial(self):
        self.assertEquals(mock_load('foo/bar/trivial'), 1)

    def test_simple(self):
        self.assertEquals(mock_load('foo/bar/simple').MEMBER, 4)
        self.assertEquals(mock_load('foo/bar/simple.Sim_Ple.MEMBER'), 4)
        self.assertEquals(mock_load('foo/bar/simple.FOO'), 1)

    def test_py(self):
        self.assertEquals(mock_load('foo/bar/simple.py').MEMBER, 4)
        self.assertEquals(mock_load('foo/bar/simple.py.py'), 7)
        self.assertEquals(mock_load('foo/bar/simple.Sim_Ple.py'), 3)
        self.assertEquals(mock_load('foo/bar/simple.py.Sim_Ple.py'), 3)

    def test_error(self):
        with self.assertRaises(ImportError):
            mock_load('failure')

        with self.assertRaises(AttributeError):
            mock_load('foo/bar/trivial.B')

    def test_imports(self):
        self.assertIs(mock_load('math'), math)
        self.assertIs(mock_load('math.log'), math.log)
        self.assertIs(mock_load('test.load_test.LoadTest'), LoadTest)
