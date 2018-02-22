import unittest

from loady.importer import import_code, import_symbol
from test.sub import foo


class ImporterTest(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError):
            import_symbol('')

    def test_single(self):
        import_symbol('math')
        import_symbol('loady')

    def test_failed_single(self):
        with self.assertRaises(ImportError):
            import_symbol('DOESNT_EXIST')

    def test_double(self):
        import_symbol('math.log')
        import_symbol('test.sub')

    def test_failed_double(self):
        with self.assertRaises(ImportError):
            import_symbol('math12.log')

        with self.assertRaises(ImportError):
            import_symbol('math.log12')

        with self.assertRaises(ImportError):
            import_symbol('loady.log12')

    def test_longer(self):
        self.assertIs(import_symbol('test.sub.foo'), foo)
        self.assertIs(import_symbol('test.sub.foo.Bar'), foo.Bar)

    def test_base_path(self):
        self.assertIs(import_symbol('test.sub.foo.Bar'), foo.Bar)
        self.assertIs(import_symbol('test.sub.foo.Bar', 'test'), foo.Bar)

        with self.assertRaises(ImportError):
            self.assertIs(import_symbol('.test.sub.foo.Bar'), foo.Bar)
        with self.assertRaises(ImportError):
            import_symbol('.test.sub.foo.Bar', 'test')
        with self.assertRaises(ImportError):
            import_symbol('.sub.foo.Bar')

        self.assertIs(import_symbol('.sub.foo.Bar', 'test'), foo.Bar)
        self.assertIs(import_symbol('sub.foo.Bar', 'test'), foo.Bar)
        self.assertIs(import_symbol('.foo.Bar', 'test.sub'), foo.Bar)
        self.assertIs(import_symbol('foo.Bar', 'test.sub'), foo.Bar)

        with self.assertRaises(ImportError):
            import_symbol('.test.sub.foo.Bar')

        self.assertIs(import_symbol('.foo', 'test.sub'), foo)
        self.assertIs(import_symbol('.sub.foo.Bar', 'test'), foo.Bar)

    def test_import_code(self):
        self.assertTrue(import_code('test.sub.modules.same')())
        self.assertTrue(import_code('test.sub.modules.single')())
        self.assertTrue(import_code('test.sub.modules.underscore')())
        self.assertTrue(import_code('test.sub.modules.under_score')())
        with self.assertRaises(ValueError):
            import_code('test.sub.modules.ambiguous')
