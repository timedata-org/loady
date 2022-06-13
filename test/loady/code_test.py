import math, unittest
from loady import code, config, data, whitelist

SIMPLE_FILE = """
FOO = 1
BAR = 2

py = 7

class Sim_Ple:
    MEMBER = 4
    py = 3
"""

MOCK_FILES = {
    'http://foo/bar/trivial.py': 'A = 1',
    'http://foo/bar/simple.py': SIMPLE_FILE,
}


def mock_load(url, base_path=None):
    def load_data(file_url, is_json):
        return MOCK_FILES[file_url]

    use_whitelist, config.USE_WHITELIST = config.USE_WHITELIST, False
    code.data.load, code_data_load = load_data, code.data.load
    try:
        return code.load_code(url, base_path)
    finally:
        config.USE_WHITELIST = use_whitelist
        code.data.load = code_data_load


class LoadTest(unittest.TestCase):
    def test_trivial(self):
        self.assertEqual(mock_load('http://foo/bar/trivial'), 1)

    def test_simple(self):
        self.assertEqual(mock_load('http://foo/bar/simple').MEMBER, 4)
        self.assertEqual(mock_load('http://foo/bar/simple.Sim_Ple.MEMBER'), 4)
        self.assertEqual(mock_load('http://foo/bar/simple.FOO'), 1)

    def test_py(self):
        self.assertEqual(mock_load('http://foo/bar/simple.py').MEMBER, 4)
        self.assertEqual(mock_load('http://foo/bar/simple.py.py'), 7)
        self.assertEqual(mock_load('http://foo/bar/simple.Sim_Ple.py'), 3)
        self.assertEqual(mock_load('http://foo/bar/simple.py.Sim_Ple.py'), 3)

    def test_base_path(self):
        self.assertEqual(mock_load('bar/trivial', 'http://foo'), 1)
        self.assertEqual(mock_load('/bar/simple', 'http://foo').MEMBER, 4)
        self.assertEqual(mock_load('/bar/simple.FOO', 'http://foo/'), 1)
        self.assertEqual(mock_load('bar/simple.py', 'http://foo/').MEMBER, 4)

    def test_error(self):
        with self.assertRaises(ImportError):
            mock_load('failure')

        with self.assertRaises(AttributeError):
            mock_load('http://foo/bar/trivial.B')

    def test_imports(self):
        self.assertIs(mock_load('math.log'), math.log)
        self.assertIs(mock_load('test.loady.code_test.LoadTest'), LoadTest)
