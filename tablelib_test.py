import unittest
import tablelib


class TestFuntions(unittest.TestCase):


    def test_auto_complete(self):
        self.assertEquals("|   |",tablelib.format_table("|"))

    def test_auto_complete_multi_line(self):
        raw_text ="""\
|
|
""".rstrip()
        expected = """\
|   |
|   |
""".rstrip()
        self.assertMultiLineEqual(expected,tablelib.format_table(raw_text))

    def test_simple_format(self):
        raw_text = """\
|col 1|col 2|
|-|-|
|cell 11 |cell 12|
|cell 21 |cell 22|
""".rstrip()
        expected = """\
|  col 1  |  col 2  |
|---------|---------|
| cell 11 | cell 12 |
| cell 21 | cell 22 |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_auto_alignment(self):
        raw_text = """\
|column 1|column 2|
|second line 1|second line 2|
|-|-|
|text value row 1 |0.9999999999999999|
|tv row 2 |99|
""".rstrip()
        expected = """\
|     column 1     |      column 2      |
|  second line 1   |   second line 2    |
|------------------|--------------------|
| text value row 1 | 0.9999999999999999 |
| tv row 2         |                 99 |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_specify_alignment(self):
        raw_text = """\
| column 1 | column 2 | column 3  |
| < | > | # |
|-|-|-|
| 1 | row 1 | c1 |
| 2 | row 2 | c2 |
| 3 | row 3 | c3 |
"""
        expected = """\
| column 1 | column 2 | column 3 |
| <<<<<<<< | >>>>>>>> | ######## |
|----------|----------|----------|
| 1        |    row 1 |    c1    |
| 2        |    row 2 |    c2    |
| 3        |    row 3 |    c3    |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_prefix(self):
        raw_text = """\
    |  col 1  |  col 2  |
|---------|---------|
| cell 11 | cell 12 |
| cell 21 | cell 22 |
""".rstrip()
        expected = """\
    |  col 1  |  col 2  |
    |---------|---------|
    | cell 11 | cell 12 |
    | cell 21 | cell 22 |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_tab_prefix(self):
        raw_text = """\
\t\t|  col 1  |  col 2  |
|---------|---------|
| cell 11 | cell 12 |
| cell 21 | cell 22 |
""".rstrip()
        expected = """\
\t\t|  col 1  |  col 2  |
\t\t|---------|---------|
\t\t| cell 11 | cell 12 |
\t\t| cell 21 | cell 22 |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_cell_tab(self):
        raw_text = """\
|\tcol 1\t|
""".rstrip()
        expected = """\
| col 1 |
""".rstrip()
        self.assertMultiLineEqual(expected, tablelib.format_table(raw_text))

    def test_not_table(self):
        with self.assertRaises(AssertionError):
            tablelib.format_table("")


if __name__ == '__main__':
    unittest.main()
