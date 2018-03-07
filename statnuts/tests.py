__author__ = 'mgrandrie'

import unittest
from . import note_converter


class NoteConverterTest(unittest.TestCase):
    def test_compute_note(self):
        self.assertEqual(note_converter.compute_note([
            {
                "source": "04c19d53-ba15-11e4-97c6-b1229586dec7",
                "source_name": "Whoscored",
                "rating": "7.7"
            },
            {
                "source": "57f67e0c-bba3-11e4-aabd-e33b7dc35c80",
                "source_name": "Sport-Express.ru",
                "rating": "6.5"
            },
            {
                "source": "0ecffaee-ba15-11e4-97c6-b1229586dec7",
                "source_name": "Sports.fr",
                "rating": "7.5"
            },
            {
                "source": "1f64e6da-bba1-11e4-aabd-e33b7dc35c80",
                "source_name": "Datasport.it",
                "rating": "6.5"
            }
        ]), 6.625)
        self.assertEqual(note_converter.compute_note([]), 0)

    def test_conv_ws(self):
        self.assertEqual(note_converter._conv_ws(5.4), 3.0)
        self.assertEqual(note_converter._conv_ws(5.8), 3.5)
        self.assertEqual(note_converter._conv_ws(5.9), 3.5)
        self.assertEqual(note_converter._conv_ws(6), 4.0)
        self.assertEqual(note_converter._conv_ws(6.2), 4.0)
        self.assertEqual(note_converter._conv_ws(6.3), 4.0)
        self.assertEqual(note_converter._conv_ws(6.6), 4.5)
        self.assertEqual(note_converter._conv_ws(6.7), 5.0)
        self.assertEqual(note_converter._conv_ws(6.9), 5.0)
        self.assertEqual(note_converter._conv_ws(7.0), 5.0)
        self.assertEqual(note_converter._conv_ws(7.2), 5.5)
        self.assertEqual(note_converter._conv_ws(7.5), 6.0)
        self.assertEqual(note_converter._conv_ws(7.6), 6.0)
        self.assertEqual(note_converter._conv_ws(7.7), 6.0)
        self.assertEqual(note_converter._conv_ws(7.8), 6.5)
        self.assertEqual(note_converter._conv_ws(7.9), 6.5)

    def test_conv_kicker(self):
        self.assertEqual(note_converter._conv_kicker(1), 8.75)
        self.assertEqual(note_converter._conv_kicker(3.5), 5.625)
        self.assertEqual(note_converter._conv_kicker(4.5), 4.375)


def main():
    unittest.main()


if __name__ == '__main__':
    main()