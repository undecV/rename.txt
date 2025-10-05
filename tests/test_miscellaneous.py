# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import unittest
from render_renamer.utilities.miscellaneous import (
    filenameify,
    readable_size,
)


class TestMiscellaneous(unittest.TestCase):
    def test_filenameify(self):
        cases = [
            ("valid_filename.txt", "valid_filename.txt"),
            ("inval|id:fi*le?name.txt", "invalidfilename.txt"),
            ("con<>:\"/\\|?*", "con"),
            ("normal name.doc", "normal name.doc"),
            ("name_with_ünicode.txt", "name_with_ünicode.txt"),
        ]

        for original, expected in cases:
            self.assertEqual(filenameify(original), expected)

    def test_readable_size(self):
        self.assertEqual(readable_size(0), "0.0 B")
        self.assertEqual(readable_size(512), "512.0 B")
        self.assertEqual(readable_size(1024), "1.0 KiB")
        self.assertEqual(readable_size(1536), "1.5 KiB")
        self.assertEqual(readable_size(1048576), "1.0 MiB")
        self.assertEqual(readable_size(1073741824), "1.0 GiB")
        self.assertEqual(readable_size(1099511627776), "1.0 TiB")
        self.assertEqual(readable_size(1125899906842624), "1.0 PiB")
        self.assertEqual(readable_size(1152921504606846976), "1.0 EiB")
        self.assertEqual(readable_size(1180591620717411303424), "1.0 ZiB")
        self.assertEqual(readable_size(1208925819614629174706176), "1.0 YiB")
