import unittest

from leftright.__main__ import DiffApplicationRunner


class TestDiffApplicationRunner(unittest.TestCase):

    """Test case docstring."""

    def test_cli_arguments(self):
        self.assertEqual(False, DiffApplicationRunner().fetch([]).debug,
                         "debug mode should be disabled by default")

        self.assertEqual(8080, DiffApplicationRunner().fetch([]).port,
                         "default port should be 8080")

        self.assertEqual(80, DiffApplicationRunner().fetch(["-p", "80"]).port,
                         "port setup should be flexible")

        self.assertEqual(True, DiffApplicationRunner().fetch(["--debug"]).debug,
                         "debug mode is a decision of user")
