# tablelib_test.py - unittest for tablelib

# Copyright (C) 2012  Free Software Foundation, Inc.

# Author: Valery Kocubinsky
# Package: SublimeTableEditor
# Homepage: https://github.com/vkocubinsky/SublimeTableEditor

# This file is part of SublimeTableEditor.

# SublimeTableEditor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# SublimeTableEditor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with SublimeTableEditor.  If not, see <http://www.gnu.org/licenses/>.

import unittest
import difflib

try:
    from . import tablelib
except ValueError:
    import tablelib


class BaseTableTest(unittest.TestCase):

    def assert_table_equals(self, expected, formatted):
        if formatted != expected:
            diff = list(difflib.unified_diff(expected.splitlines(),
                                            formatted.splitlines()))
            msg = ("Formatted table and Expected table doesn't match. " +
                   "\nExpected:\n{0}" +
                   "\nActual:\n{1}" +
                   "\nDiff:\n {2}").format(expected, formatted, "\n".join(diff))
            self.fail(msg)



class SimpleSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = tablelib.simple_syntax()

    def testBasic(self):
        unformatted = """\
| Name | Gender | Age |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa | F | 21 |
| Alex | M | 22 |
""".rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
""".rstrip()

        t = tablelib.parse_table(self.syntax, unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testCustomAlignment(self):
        unformatted = """\
| Name | Gender | Age |
| > | # | < |
|---|---|---|
| Alisa | F | 21 |
| Alex | M | 22 |
""".rstrip()

        expected = """\
|  Name | Gender | Age |
| >>>>> | ###### | <<< |
|-------|--------|-----|
| Alisa |   F    | 21  |
|  Alex |   M    | 22  |
""".rstrip()

        t = tablelib.parse_table(self.syntax, unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testSwapColumn(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |      Age      |    Gender   |
| Text Column | Number Column | Char Column |
|-------------|---------------|-------------|
| Alisa       |            21 | F           |
| Alex        |            22 | M           |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.swap_columns(1,2)
        self.assert_table_equals(expected,t.render())


    def testDeleteColumn(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |      Age      |
| Text Column | Number Column |
|-------------|---------------|
| Alisa       |            21 |
| Alex        |            22 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.delete_column(1)
        self.assert_table_equals(expected,t.render())


    def testSwapRows(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alex        | M           |            22 |
| Alisa       | F           |            21 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.swap_rows(3,4)
        self.assert_table_equals(expected,t.render())

    def testDeleteRow(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.delete_row(4)
        self.assert_table_equals(expected,t.render())

    def testInsertEmptyColumn(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |   |    Gender   |      Age      |
| Text Column |   | Char Column | Number Column |
|-------------|---|-------------|---------------|
| Alisa       |   | F           |            21 |
| Alex        |   | M           |            22 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.insert_empty_column(1)
        self.assert_table_equals(expected,t.render())

    def testInsertEmptyRow(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
|             |             |               |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.insert_empty_row(3)
        self.assert_table_equals(expected,t.render())

    def testInsertSeparatorRow(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.insert_single_separator_row(2)
        self.assert_table_equals(expected,t.render())


    def testInsertDoubleSeparatorRow(self):
        text = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|=============|=============|===============|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.rstrip()


        t = tablelib.parse_table(self.syntax, text)
        t.insert_double_separator_row(2)
        self.assert_table_equals(expected,t.render())

class TextileSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = tablelib.textile_syntax()

    def testBasic(self):
        unformatted = """\
|_. attribute list |
|<. align left |
| cell|
|>. align right|
|=. center |
|<>. justify |
|^. valign top |
|~. bottom |
""".rstrip()

        expected = """\
|_. attribute list |
|<. align left     |
|    cell          |
|>.    align right |
|=.     center     |
|<>. justify       |
|^. valign top     |
|~. bottom         |
""".rstrip()

        t = tablelib.parse_table(self.syntax, unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)


class MultiMarkdownSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = tablelib.multi_markdown_syntax()

    def testBasic(self):
        unformatted = """\
| Name | Gender | Age |
| Text Column | Char Column | Number Column |
|-:|:-:|:-|
| Alisa | F | 21 |
| Alex | M | 22 |
""".rstrip()

        expected = """\
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| ----------: | :---------: | :------------ |
|       Alisa |      F      | 21            |
|        Alex |      M      | 22            |
""".rstrip()

        t = tablelib.parse_table(self.syntax, unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)


class ReStructuredTextSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = tablelib.re_structured_text_syntax()

    def testBasic(self):
        unformatted = """\
+-------------+
| widget code |
+===============================================+
| code-block::javascript                        |
|                                               |
|    widget.dispatchEvent('onSetTags', object); |
+-----------------------------------------------+
""".rstrip()

        expected = """\
+-----------------------------------------------+
|                  widget code                  |
+===============================================+
| code-block::javascript                        |
|                                               |
|    widget.dispatchEvent('onSetTags', object); |
+-----------------------------------------------+
""".rstrip()

        self.syntax.keep_space_left = True
        t = tablelib.parse_table(self.syntax, unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)


if __name__ == '__main__':
    unittest.main()
