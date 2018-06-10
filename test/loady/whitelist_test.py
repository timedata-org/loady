import contextlib, unittest
from loady import whitelist

WHITELIST = [
    ['github.com', 'rec', 'swirly'],
    ['github.com', 'rec2'],
    ['github.com', ''],  # Should have no effect.
    ['gitlab.com', 'rec3', 'forbidden'],
    ['gitlab.com', 'rec', 'swirly', '', ''],  # Extra fields should be OK.
]

BAD_WHITELIST = [
    ['github.com', 'rec', 'swirly'],
    ['github.com'],  # This should cause an exception.
]


class WhitelistTest(unittest.TestCase):
    def test_matches(self):
        def matches(*target):
            return whitelist.matches_any(target, WHITELIST)

        self.assertFalse(matches())
        self.assertFalse(matches('nothing.com'))
        self.assertFalse(matches('github.com'))
        self.assertFalse(matches('gitlab.com', 'frog'))
        self.assertFalse(matches('github.com', 'rec'))
        self.assertFalse(matches('gitlab.com', 'rec'))
        self.assertFalse(matches('github.com', 'rec', 'random'))
        self.assertFalse(matches('github.com', 'rec3', 'forbidden'))

        self.assertTrue(matches('github.com', 'rec2'))
        self.assertTrue(matches('github.com', 'rec2', 'swirly'))
        self.assertTrue(matches('github.com', 'rec2', 'random'))
        self.assertTrue(matches('github.com', 'rec', 'swirly'))

    def test_check_allow_prompt(self):
        prompts = []

        def check(value, *entry):
            def mock_input(prompt):
                return prompts.append(prompt) or value

            prompts.clear()
            return whitelist.check_allow_prompt(
                entry, WHITELIST, input=mock_input)

        self.assertTrue(check('y', 'github.com', 'rec', 'swirly'))
        self.assertFalse(prompts)

        self.assertFalse(check('y', 'github.com', 'rec', 'swirly2'))
        self.assertIn('https://github.com/rec/swirly2', prompts[0])
        self.assertIn('https://github.com/rec/swirly2', prompts[1])

        self.assertTrue(check('n', 'github.com', 'rec', 'swirly'))
        self.assertFalse(prompts)

        with self.assertRaises(ValueError):
            check('n', 'github.com', 'rec', 'swirly2')


EXAMPLES = (
    ('https://gist.github.com/rec/adb4bc48080a6505e73b945c1178f614',
     'https://gist.githubusercontent.com/rec/adb4bc48080a6505e73b945c1178f614'
     '/raw/55c99dbc774be86a1ec163c244a4ef94c31b5420/larsen-scanner.json'),

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
