# table_plugin_test.py - sublime plugin with integration tests

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

from __future__ import print_function
import sublime
import sublime_plugin


class CommandDef:

    def __init__(self, name, args=None):
        self.name = name
        self.args = args


class CallbackTest:
    def __init__(self, name, syntax):
        self.name = name
        self.commands = []
        self.commands.append(CommandDef("table_editor_set_syntax",
                                        {"syntax": syntax}))
        self.commands.append(CommandDef("table_editor_disable_for_current_view",
                                        {"prop": "table_editor_keep_space_left"}))
        self.commands.append(CommandDef("table_editor_enable_for_current_view",
                                        {"prop": "table_editor_detect_header"}))
        self.commands.append(CommandDef("table_editor_enable_for_current_view",
                                        {"prop": "table_editor_align_number_right"}))
        self.commands.append(CommandDef("table_editor_enable_for_current_view",
                                        {"prop": "table_editor_intelligent_formatting"}))
        self.commands.append(CommandDef("select_all"))
        self.commands.append(CommandDef("cut"))

    def expected_value(self):
        pass

    def test(actual_value):
        pass


class SimpleBasicEditingTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Basic Editing", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| Name | Phone |
|-"""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "Anna"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "123456789"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "Alexander"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "987654321"}))
        self.commands.append(CommandDef("table_editor_next_field"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Create simple table
- Navigate with tab key
- Automatic row creation
- Fill the table
""".format(self.name)

    def expected_value(self):
        return """{0}
|    Name   |   Phone   |
|-----------|-----------|
| Anna      | 123456789 |
| Alexander | 987654321 |
|           |           |""".format(self.description)


class SimpleQuickTableCreateTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Quick Table Creation", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| Name | Phone"""}))
        self.commands.append(CommandDef("table_editor_hline_and_move"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Quick table creation with key ctrl+k,enter
""".format(self.name)

    def expected_value(self):
        return """{0}
| Name | Phone |
|------|-------|
|      |       |""".format(self.description)


class SimpleGridTableTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Grid Table Creation", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| Name | Phone |
|="""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "Anna"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "123456789"}))
        self.commands.append(CommandDef("table_editor_hline_and_move"))
        self.commands.append(CommandDef("insert", {"characters": "Alexander"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "987654321"}))
        self.commands.append(CommandDef("table_editor_hline_and_move"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Create simple table
- Use double hline
- Add lines separated by single hline
""".format(self.name)

    def expected_value(self):
        return """{0}
|    Name   |   Phone   |
|===========|===========|
| Anna      | 123456789 |
|-----------|-----------|
| Alexander | 987654321 |
|-----------|-----------|
|           |           |""".format(self.description)


class SimpleColumnsTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Work with columns", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| Name | Phone |
|-"""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "Anna"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "123456789"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "Alexander"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "987654321"}))
        self.commands.append(CommandDef("table_editor_next_row"))
        self.commands.append(CommandDef("table_editor_insert_column"))
        for i in range(0, 3):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("insert", {"characters": "28"}))
        for i in range(0, 3):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("insert", {"characters": "32"}))
        for i in range(0, 3):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("insert", {"characters": "Age"}))
        self.commands.append(CommandDef("table_editor_move_column_right"))
        self.commands.append(CommandDef("table_editor_delete_column"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Create simple table
- Insert And Fill Column
- Move Column Right
- Delete Column
""".format(self.name)

    def expected_value(self):
        return """{0}
|    Name   |   Phone   |
|-----------|-----------|
| Anna      | 123456789 |
| Alexander | 987654321 |
|           |           |""".format(self.description)


class SimpleRowsTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Work with rows", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
|    Name   |   Phone   | Age |
|-----------|-----------|-----|
| Anna      | 123456789 |  32 |
| Alexander | 987654321 |  28 |"""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        for i in range(4):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("table_editor_insert_row"))
        self.commands.append(CommandDef("table_editor_kill_row"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Insert Row
- Delete Row
""".format(self.name)

    def expected_value(self):
        return """{0}
|    Name   |   Phone   | Age |
|-----------|-----------|-----|
| Anna      | 123456789 |  32 |
| Alexander | 987654321 |  28 |
|           |           |     |""".format(self.description)


class SimpleLongRowsTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Work with long rows", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
|    Name   |   Phone   | Age |             Position             |
|-----------|-----------|-----|----------------------------------|
| Anna      | 123456789 |  32 | Senior Software Engineer         |
| Alexander | 987654321 |  28 | Senior Software Testing Engineer |"""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        for i in range(5):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("table_editor_insert_single_hline"))
        self.commands.append(CommandDef("move", {"by": "words", "forward": False}))
        self.commands.append(CommandDef("table_editor_split_column_down"))
        for i in range(4):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("move", {"by": "words", "forward": False}))
        self.commands.append(CommandDef("table_editor_split_column_down"))
        for i in range(4):
            self.commands.append(CommandDef("table_editor_previous_field"))
        self.commands.append(CommandDef("table_editor_join_lines"))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("table_editor_hline_and_move"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Split Row
- Join Rows
- Insert hlines
""".format(self.name)

    def expected_value(self):
        return """{0}
|    Name   |   Phone   | Age |             Position             |
|-----------|-----------|-----|----------------------------------|
| Anna      | 123456789 |  32 | Senior Software Engineer         |
|-----------|-----------|-----|----------------------------------|
| Alexander | 987654321 |  28 | Senior Software Testing Engineer |
|-----------|-----------|-----|----------------------------------|
|           |           |     |                                  |""".format(self.description)


class SimpleCustomAlignTest(CallbackTest):

    def __init__(self):
        CallbackTest.__init__(self, "Custom align test", "Simple")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| column A | column B | column C |
| < | > | # |
|-"""}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'1'"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'2'"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": ">"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "<"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "#"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'1'"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_editor_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'2'"}))
        self.commands.append(CommandDef("table_editor_next_field"))

    @property
    def description(self):
        return """Test: {0}
- Simple Table Syntax
- Create table with separator
- Navigate with tab key
- Custom align
""".format(self.name)

    def expected_value(self):
        return """{0}
| column A | column B | column C |
| <<<<<<<< | >>>>>>>> | ######## |
|----------|----------|----------|
| 1        |      one |   '1'    |
| 2        |      two |   '2'    |
| >>>>>>>> | <<<<<<<< | ######## |
|        1 | one      |   '1'    |
|        2 | two      |   '2'    |
|          |          |          |""".format(self.description)


class reStructuredTextKeepSpaceLeftTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Keep Spece left", "reStructuredText")
        self.commands.append(CommandDef("table_editor_enable_for_current_view", {"prop": "table_editor_keep_space_left"}))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
+-------------+
| widget code |
+===============================================+
| code-block::javascript                        |
|                                               |
|    widget.dispatchEvent('onSetTags', object); |
+-----------------------------------------------+"""}))
        self.commands.append(CommandDef("table_editor_align"))


    @property
    def description(self):
        return """Test: {0}
- reStructuredText Syntax
""".format(self.name)

    def expected_value(self):
        return """{0}
+-----------------------------------------------+
|                  widget code                  |
+===============================================+
| code-block::javascript                        |
|                                               |
|    widget.dispatchEvent('onSetTags', object); |
+-----------------------------------------------+""".format(self.description)


class reStructuredTextDisableDetectHeaderTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Disable Detect Header Test", "reStructuredText")
        self.commands.append(CommandDef("table_editor_disable_for_current_view", {"prop": "table_editor_detect_header"}))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
+--------+
| header |
+--------+
| long and shifted data row |
+---------------------------+"""}))
        self.commands.append(CommandDef("table_editor_align"))


    @property
    def description(self):
        return """Test: {0}
- reStructuredText Syntax
- Disable detect header
""".format(self.name)

    def expected_value(self):
        return """{0}
+---------------------------+
| header                    |
+---------------------------+
| long and shifted data row |
+---------------------------+""".format(self.description)


class PandocAlignTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Pandoc Align Test", "Pandoc")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
+-----------+-----------+-----+
|    Name   |   Phone   | Age |
+===========+===========+=====+
| Anna      | 123456789 |  32 |
+-----------+-----------+-----+
| Alexander | 987654321 |  28 |
+-----------+-----------+-----+"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- Pandoc Syntax
""".format(self.name)

    def expected_value(self):
        return """{0}
+-----------+-----------+-----+
|    Name   |   Phone   | Age |
+===========+===========+=====+
| Anna      | 123456789 |  32 |
+-----------+-----------+-----+
| Alexander | 987654321 |  28 |
+-----------+-----------+-----+""".format(self.description)


class EmacsOrgModeAlignTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "EmacsOrgMode Align Test", "EmacsOrgMode")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
|-----------+-----------+-----|
|    Name   |   Phone   | Age |
|===========+===========+=====|
| Anna      | 123456789 |  32 |
|-----------+-----------+-----|
| Alexander | 987654321 |  28 |
|-----------+-----------+-----|"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- EmacsOrgMode Syntax
""".format(self.name)

    def expected_value(self):
        return """{0}
|-----------+-----------+-----|
|    Name   |   Phone   | Age |
|===========+===========+=====|
| Anna      | 123456789 |  32 |
|-----------+-----------+-----|
| Alexander | 987654321 |  28 |
|-----------+-----------+-----|""".format(self.description)


class MarkdownColspanTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "MultiMarkdown Colspan Test", "MultiMarkdown")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
|              |           Grouping          ||
| First Header | Second Header | Third Header |
| ------------ | :-----------: | -----------: |
| Content      |         *Long Cell*         ||
| Content      |    **Cell**   |         Cell |
| New section  |      More     |         Data |
| And more     |    And more   |              |
| :---------------------------------------: |||"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- MultiMarkdown Syntax
""".format(self.name)

    def expected_value(self):
        return """{0}
|              |           Grouping          ||
| First Header | Second Header | Third Header |
| ------------ | :-----------: | -----------: |
| Content      |         *Long Cell*         ||
| Content      |    **Cell**   |         Cell |
| New section  |      More     |         Data |
| And more     |    And more   |              |
| :---------------------------------------: |||""".format(self.description)


class TextileAlignTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Textile Align Test", "Textile")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
|_.   Name  |_. Age |_. Custom Alignment Demo |
| Anna      | 20 |<. left                  |
| Alexander | 27 |>.                 right |
| Misha     | 42 |=.         center        |
|           |    |                         |"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- Textile Syntax
""".format(self.name)

    def expected_value(self):
        return """{0}
|_.   Name  |_. Age |_. Custom Alignment Demo |
| Anna      |    20 |<. left                  |
| Alexander |    27 |>.                 right |
| Misha     |    42 |=.         center        |
|           |       |                         |""".format(self.description)


class TextileColspanTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Textile Colspan Test", "Textile")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": r"""
|\2. spans two cols   |
| col 1    | col 2    |"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- Textile Syntax
""".format(self.name)

    def expected_value(self):
        return r"""{0}
|\2. spans two cols   |
| col 1    | col 2    |""".format(self.description)


class TextileRowspanTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Textile Rowspan Test", "Textile")
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": r"""
|/3. spans 3 rows | a |
| b |
| c |"""}))
        self.commands.append(CommandDef("table_editor_align"))

    @property
    def description(self):
        return """Test: {0}
- Textile Syntax
""".format(self.name)

    def expected_value(self):
        return r"""{0}
|/3. spans 3 rows | a |
| b               |
| c               |""".format(self.description)


class TableEditorTestSuite(sublime_plugin.TextCommand):
    COMMAND_TIMEOUT = 25
    TEST_TIMEOUT = 50

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)

    def run(self):
        tests = []
        tests.append(SimpleBasicEditingTest())
        tests.append(SimpleQuickTableCreateTest())
        tests.append(SimpleGridTableTest())
        tests.append(SimpleColumnsTest())
        tests.append(SimpleRowsTest())
        tests.append(SimpleLongRowsTest())
        tests.append(SimpleCustomAlignTest())
        tests.append(reStructuredTextKeepSpaceLeftTest())
        tests.append(reStructuredTextDisableDetectHeaderTest())
        tests.append(PandocAlignTest())
        tests.append(EmacsOrgModeAlignTest())
        tests.append(MarkdownColspanTest())
        tests.append(TextileAlignTest())
        tests.append(TextileColspanTest())
        tests.append(TextileRowspanTest())

        self.run_tests(tests, 0, 0)

    def run_tests(self, tests, test_ind, command_ind):
        if test_ind >= len(tests):
            self.view.run_command("select_all")
            self.view.run_command("cut")
            self.view.run_command("insert", {"characters": """
{0} tests ran sucessfully

Click ctrl+w to close this window""".format(len(tests))})
            return
        test = tests[test_ind]
        if command_ind == 0:
            print("run test", test.name)
        command = test.commands[command_ind]
        self.view.run_command(command.name, command.args)
        if command_ind + 1 < len(test.commands):
            sublime.set_timeout(lambda: self.run_tests(tests, test_ind, command_ind + 1),
                                TableEditorTestSuite.COMMAND_TIMEOUT)
        else:
            text = self.get_buffer_text()
            if text.strip() != tests[test_ind].expected_value().strip():
                self.view.run_command("move_to", {"extend": False, "to": "eof"})
                self.view.run_command("insert", {"characters": """
Test {0} failed:
Expected:
{1}<<<
Actual:
{2}<<<
""".format(tests[test_ind].name, tests[test_ind].expected_value(), text)})
            else:
                self.view.run_command("move_to", {"extend": False, "to": "eof"})
                self.view.run_command("insert", {"characters": """
Test {0} executed sucessfully
""".format(tests[test_ind].name)})

                sublime.set_timeout(lambda: self.run_tests(tests, test_ind + 1, 0),
                                    TableEditorTestSuite.TEST_TIMEOUT)

    def get_buffer_text(self):
        return self.view.substr(sublime.Region(0, self.view.size()))


class TableEditorFilmCommand(sublime_plugin.WindowCommand):

    def run(self):
        view = self.window.new_file()
        view.set_scratch(True)
        view.set_name("Sublime Table Editor Film")
        view.settings().set("table_editor_border_style", "simple")
        view.run_command("table_editor_enable_for_current_view", {"prop": "enable_table_editor"})
        suite = TableEditorTestSuite(view)
        suite.run()
