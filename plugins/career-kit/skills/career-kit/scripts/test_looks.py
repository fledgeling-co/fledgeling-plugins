"""Tests for looks.py: every named look sits inside the research's bounds, and the check refuses
values outside them. Run: python3 test_looks.py"""
import os, sys, unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from looks import LOOKS, check_look, contrast, get_look  # noqa: E402


class Looks(unittest.TestCase):
    def test_every_named_look_passes(self):
        self.assertGreaterEqual(len(LOOKS), 7)
        for look in LOOKS.values():
            check_look(look)

    def test_classic_is_the_old_default(self):
        l = get_look("classic")
        self.assertEqual((l["font"], l["pt"], l["lh"], l["h2_size"], l["name_size"], l["gap"]),
                         ("Arial", 11, 13, 14, 20, 12))
        self.assertEqual(l["accent"], "#1F2B5B")
        self.assertTrue(l["rule"])

    def test_out_of_bounds_values_are_refused(self):
        base = dict(LOOKS["classic"])
        cases = {"font": "Comic Sans MS", "pt": 10, "h2_size": 18, "name_size": 28, "gap": 20,
                 "h2_weight": 400, "accent": "#9AB0FF", "title_color": "#C8D2E0"}
        for key, value in cases.items():
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_look({**base, key: value})

    def test_leading_must_be_two_points(self):
        with self.assertRaises(ValueError):
            check_look({**LOOKS["classic"], "pt": 11, "lh": 16})

    def test_accent_override_is_checked(self):
        self.assertEqual(get_look("calibri-teal", "burgundy")["accent"], "#7A2E2E")
        with self.assertRaises(ValueError):
            get_look("classic", "#FFD54F")

    def test_contrast(self):
        self.assertAlmostEqual(contrast("#000000"), 21.0, places=1)
        self.assertGreater(contrast("#1F5F63"), 7)


if __name__ == "__main__":
    unittest.main()
