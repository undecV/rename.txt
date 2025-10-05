# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from render_renamer.utilities.rich_difference_strings import (
    rich_difference_strings
)


class TestRichDifferenceStrings(unittest.TestCase):
    def test_rich_difference_strings(self):
        a = "The quick brown fox"
        b = "The quick red fox jumped over the lazy cat"
        self.assertEqual(
            rich_difference_strings(a, b).markup,
            "[equal]The quick [deleted][/equal]b[equal][/deleted]"
            "r[replaced][/equal]own[replacing][/replaced]ed[equal]"
            "[/replacing] fox[inserted][/equal] jumped over the lazy "
            "cat[/inserted]"
        )
