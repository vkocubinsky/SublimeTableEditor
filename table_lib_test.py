# table_lib_test.py - unittest for table_lib

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
    from . import table_lib
    from . import table_base as tbase
except ValueError:
    import table_lib
    import table_base as tbase


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
        self.syntax = table_lib.simple_syntax()

    def testBasic(self):
        unformatted = """
| Name | Gender | Age |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa | F | 21 |
| Alex | M | 22 |
""".strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testSpace(self):
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

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testCustomAlignment(self):
        unformatted = """
| Name | Gender | Age |
| > | # | < |
|---|---|---|
| Alisa | F | 21 |
| Alex | M | 22 |
""".strip()

        expected = """
|  Name | Gender | Age |
| >>>>> | ###### | <<< |
|-------|--------|-----|
| Alisa |   F    | 21  |
|  Alex |   M    | 22  |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testMoveColumnRight(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |      Age      |    Gender   |
| Text Column | Number Column | Char Column |
|-------------|---------------|-------------|
| Alisa       |            21 | F           |
| Alex        |            22 | M           |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_move_column_right(t, tbase.TablePos(0, 1))
        self.assertEqual(tbase.TablePos(0, 2), pos)
        self.assert_table_equals(expected, t.render())

    def testMoveColumnLeft(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |      Age      |    Gender   |
| Text Column | Number Column | Char Column |
|-------------|---------------|-------------|
| Alisa       |            21 | F           |
| Alex        |            22 | M           |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_move_column_left(t, tbase.TablePos(0, 2))
        self.assertEqual(tbase.TablePos(0, 1), pos)
        self.assert_table_equals(expected, t.render())

    def testDeleteColumn(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |      Age      |
| Text Column | Number Column |
|-------------|---------------|
| Alisa       |            21 |
| Alex        |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_delete_column(t, tbase.TablePos(0, 1))
        self.assertEqual(tbase.TablePos(0, 1), pos)
        self.assert_table_equals(expected, t.render())

    def testMoveRowDown(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alex        | M           |            22 |
| Alisa       | F           |            21 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_move_row_down(t, tbase.TablePos(3, 0))
        self.assertEqual(tbase.TablePos(4, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testMoveRowUp(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alex        | M           |            22 |
| Alisa       | F           |            21 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_move_row_up(t, tbase.TablePos(4, 0))
        self.assertEqual(tbase.TablePos(3, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testKillRow(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_kill_row(t, tbase.TablePos(4, 0))
        self.assertEqual(tbase.TablePos(3, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testInsertColumn(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |   |    Gender   |      Age      |
| Text Column |   | Char Column | Number Column |
|-------------|---|-------------|---------------|
| Alisa       |   | F           |            21 |
| Alex        |   | M           |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_insert_column(t, tbase.TablePos(0, 1))
        self.assertEqual(tbase.TablePos(0, 1), pos)
        self.assert_table_equals(expected, t.render())

    def testInsertRow(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
|             |             |               |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_insert_row(t, tbase.TablePos(3, 0))
        self.assertEqual(tbase.TablePos(3, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testInsertSingleHline(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_insert_single_hline(t, tbase.TablePos(1, 0))
        self.assertEqual(tbase.TablePos(1, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testInsertHlineAndMove(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|-------------|-------------|---------------|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_insert_hline_and_move(t, tbase.TablePos(1, 0))
        self.assertEqual(tbase.TablePos(3, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testInsertDoubleHline(self):
        text = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        expected = """
|     Name    |    Gender   |      Age      |
| Text Column | Char Column | Number Column |
|=============|=============|===============|
| Alisa       | F           |            21 |
| Alex        | M           |            22 |
        """.strip()

        t = self.syntax.table_parser.parse_text(text)
        d = self.syntax.table_driver
        msg, pos = d.editor_insert_double_hline(t, tbase.TablePos(1, 0))
        self.assertEqual(tbase.TablePos(1, 0), pos)
        self.assert_table_equals(expected, t.render())

    def testParseCsv(self):
        csv_text = """
a,b,c
1,2,3
        """.strip()

        expected = """
| a | b | c |
| 1 | 2 | 3 |
        """.strip()

        d = self.syntax.table_driver
        t = d.parse_csv(csv_text)
        self.assert_table_equals(expected, t.render())


class TextileSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = table_lib.textile_syntax()

    def testBasic(self):
        unformatted = """
|_. attribute list |
|<. align left |
| cell|
|>. align right|
|=. center|
|<>. justify |
|^. valign top |
|~. bottom|
|     >.  poor syntax
|(className). class|
|{key:value}. style|
""".strip()

        expected = """
|_.  attribute list |
|<. align left      |
| cell              |
|>.     align right |
|=.      center     |
|<>. justify        |
|^. valign top      |
|~. bottom          |
|>.     poor syntax |
|(className). class |
|{key:value}. style |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testCompoundSyntax(self):
        unformatted = r"""
|_>. header |_. centered header |
|>^. right and top align | long text to show alignment |
|=\2. centered colspan|
|<>(red). justified |~=. centered |
|{text-shadow:0 1px 1px black;}(highlight)<~. syntax overload | normal text |
""".strip()

        expected = r"""
|_>.                                                   header |_.      centered header      |
|>^.                                      right and top align | long text to show alignment |
|=\2.                                    centered colspan                                   |
|<>(red). justified                                           |~=.         centered         |
|{text-shadow:0 1px 1px black;}(highlight)<~. syntax overload | normal text                 |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testColspan(self):
        unformatted = r"""
|\2. spans two cols |
| col 1 | col 2 |
""".strip()

        expected = r"""
|\2. spans two cols   |
| col 1    | col 2    |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testRowspan(self):
        unformatted = r"""
|/3. spans 3 rows | a |
| b |
| c |
""".strip()

        expected = r"""
|/3. spans 3 rows | a |
| b               |
| c               |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testIntelligentFormatting(self):
        self.syntax.intelligent_formatting = True
        unformatted = r"""
|_. Attribute Name |_. Required |_. Value Type |
| \3. All Events                 |            |              |
""".strip()

        expected = r"""
|_. Attribute Name |_. Required |_. Value Type |
|\3. All Events                                |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testVisualTointernalIndex(self):

        unformatted = r"""
| a     | b     | c        | d     | e     | f        |
|\2. visual 0   | visual 1 |\2. visual 2   | visual 3 |
| 0     | 1     | 2        | 3     | 4     | 5        |
""".strip()

        t = self.syntax.table_parser.parse_text(unformatted)
        d = self.syntax.table_driver
        #formatted = t.render()

        # test visual_to_internal_index
        self.assertEqual(tbase.TablePos(1, 0), d.visual_to_internal_index(t, tbase.TablePos(1, 0)))
        self.assertEqual(tbase.TablePos(1, 2), d.visual_to_internal_index(t, tbase.TablePos(1, 1)))
        self.assertEqual(tbase.TablePos(1, 3), d.visual_to_internal_index(t, tbase.TablePos(1, 2)))
        self.assertEqual(tbase.TablePos(1, 5), d.visual_to_internal_index(t, tbase.TablePos(1, 3)))

        self.assertEqual(tbase.TablePos(1, 5), d.visual_to_internal_index(t, tbase.TablePos(1, 1000)))

        # test trivial
        for col in range(len(t[0])):
            self.assertEqual(tbase.TablePos(0, col), d.visual_to_internal_index(t, tbase.TablePos(0, col)))
            self.assertEqual(tbase.TablePos(2, col), d.visual_to_internal_index(t, tbase.TablePos(2, col)))

            self.assertEqual(tbase.TablePos(0, col), d.internal_to_visual_index(t, tbase.TablePos(0, col)))
            self.assertEqual(tbase.TablePos(2, col), d.internal_to_visual_index(t, tbase.TablePos(2, col)))

        # test internal_to_visual_index
        self.assertEqual(tbase.TablePos(1, 0), d.internal_to_visual_index(t, tbase.TablePos(1, 0)))
        self.assertEqual(tbase.TablePos(1, 0), d.internal_to_visual_index(t, tbase.TablePos(1, 1)))
        self.assertEqual(tbase.TablePos(1, 1), d.internal_to_visual_index(t, tbase.TablePos(1, 2)))
        self.assertEqual(tbase.TablePos(1, 2), d.internal_to_visual_index(t, tbase.TablePos(1, 3)))
        self.assertEqual(tbase.TablePos(1, 2), d.internal_to_visual_index(t, tbase.TablePos(1, 4)))
        self.assertEqual(tbase.TablePos(1, 3), d.internal_to_visual_index(t, tbase.TablePos(1, 5)))


class MultiMarkdownSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = table_lib.multi_markdown_syntax()

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

        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testColspan(self):
                unformatted = """\
    |                 |          Grouping           ||
    |   First Header  | Second Header | Third Header |
    |    ------------ | :-------:     | --------:    |
    |   Content       |          *Long Cell*        ||
    |   Content       |   **Cell**    |         Cell |
    |   New section   |     More      |         Data |
    |   And more      |            And more          |
    | :---: |||
        """.rstrip()

                expected = """\
    |              |           Grouping          ||
    | First Header | Second Header | Third Header |
    | ------------ | :-----------: | -----------: |
    | Content      |         *Long Cell*         ||
    | Content      |    **Cell**   |         Cell |
    | New section  |      More     |         Data |
    | And more     |    And more   |              |
    | :---------------------------------------: |||
        """.rstrip()

                t = self.syntax.table_parser.parse_text(unformatted)
                formatted = t.render()
                self.assert_table_equals(expected, formatted)

    text = """

"""


class ReStructuredTextSyntaxTest(BaseTableTest):

    def setUp(self):
        self.syntax = table_lib.re_structured_text_syntax()

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
        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)

    def testDetectHeader(self):
        unformatted = """\
+---------+
|  header |
+------------------------------+
|    long and shifted data row |
+------------------------------+
""".rstrip()

        expected = """\
+------------------------------+
|  header                      |
+------------------------------+
|    long and shifted data row |
+------------------------------+
""".rstrip()

        self.syntax.detect_header = False
        self.syntax.keep_space_left = True
        t = self.syntax.table_parser.parse_text(unformatted)
        formatted = t.render()
        self.assert_table_equals(expected, formatted)


if __name__ == '__main__':
    unittest.main()
