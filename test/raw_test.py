import unittest
from gitty.raw import raw


class RawTest(unittest.TestCase):
    def test_unchanged(self):
        for i in '', 'fails', 'http://batlab.com/foo/bar/baz/bang/bong':
            self.assertEqual(i, raw(i))

    def test_examples(self):
        for before, after in EXAMPLES:
            self.assertEqual(after, raw(before))


EXAMPLES = (
    ('https://github.com/ManiacalLabs/BiblioPixel/blob/master/tox.ini',
     'https://raw.githubusercontent.com/ManiacalLabs/BiblioPixel/master/tox.ini'
     ),

    ('https://github.com/ManiacalLabs/BiblioPixel/blob/dev/test/project.json',
     'https://raw.githubusercontent.com/ManiacalLabs/BiblioPixel/dev/test/' +
     'project.json'),

    ('https://gitlab.com/ase/ase/blob/fix_wannier/doc/Makefile',
     'https://gitlab.com/ase/ase/raw/fix_wannier/doc/Makefile'),

    ('https://gitlab.com/ase/ase/blob/master/ase/geometry/distance.py',
     'https://gitlab.com/ase/ase/raw/master/ase/geometry/distance.py'),
)
