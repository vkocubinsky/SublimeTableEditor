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

import sublime
import sublime_plugin


class CommandDef:

    def __init__(self, name, args=None):
        self.name = name
        self.args = args


class CallbackTest:
    def __init__(self, name):
        self.name = name
        self.commands = []

    def expected_value(self):
        pass

    def test(actual_value):
        pass


class SimpleTableTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Simple table test")
        self.commands.append(CommandDef("select_all"))
        self.commands.append(CommandDef("cut"))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| column A | column B |
|-"""}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_next_field"))

    def expected_value(self):
        return """{0}
| column A | column B |
|----------|----------|
|        1 | one      |
|        2 | two      |
|          |          |""".format(self.description)

    @property
    def description(self):
        return """Test: {0}
- create table with separator
- navigate with tab key
- automatic row creation
""".format(self.name)


class MoveColumnTest(CallbackTest):

    def __init__(self):
        CallbackTest.__init__(self, "Move columns test")
        self.commands.append(CommandDef("select_all"))
        self.commands.append(CommandDef("cut"))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| column A | column B | column C |
|-"""}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "row A"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "row B"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "row C"}))
        self.commands.append(CommandDef("table_move_column_left"))
        self.commands.append(CommandDef("table_move_column_right"))
        self.commands.append(CommandDef("table_insert_column"))
        self.commands.append(CommandDef("table_delete_column"))

    @property
    def description(self):
        return """Test: {0}
- create table with separator
- navigate with tab key
- move column left/right
- insert/delete column
""".format(self.name)

    def expected_value(self):
        return """{0}
| column A | column B | column C |
|----------|----------|----------|
| row A    | row B    | row C    |""".format(self.description)


class CustomAlignTest(CallbackTest):

    def __init__(self):
        CallbackTest.__init__(self, "Custom align test")
        self.commands.append(CommandDef("select_all"))
        self.commands.append(CommandDef("cut"))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| column A | column B | column C |
| < | > | # |
|-"""}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'1'"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'2'"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": ">"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "<"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "#"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'1'"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "'2'"}))
        self.commands.append(CommandDef("table_next_field"))

    @property
    def description(self):
        return """Test: {0}
- create table with separator
- navigate with tab key
- custom align
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


class RowsTableTest(CallbackTest):
    def __init__(self):
        CallbackTest.__init__(self, "Row table test")
        self.commands.append(CommandDef("select_all"))
        self.commands.append(CommandDef("cut"))
        self.commands.append(CommandDef("insert", {"characters": self.description}))
        self.commands.append(CommandDef("insert", {"characters": """
| column A | column B |
|-"""}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "1"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "one"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "2"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "two"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "3"}))
        self.commands.append(CommandDef("table_next_field"))
        self.commands.append(CommandDef("insert", {"characters": "three"}))
        self.commands.append(CommandDef("table_align"))
        self.commands.append(CommandDef("table_previous_field"))
        self.commands.append(CommandDef("table_previous_field"))
        self.commands.append(CommandDef("table_kill_row"))
        self.commands.append(CommandDef("table_insert_row"))
        self.commands.append(CommandDef("table_next_row"))
        self.commands.append(CommandDef("table_next_row"))
        self.commands.append(CommandDef("table_next_row"))

    def expected_value(self):
        return """{0}
| column A | column B |
|----------|----------|
|          |          |
|        1 | one      |
|        3 | three    |
|          |          |""".format(self.description)

    @property
    def description(self):
        return """Test: {0}
- create table with separator
- navigate with tab key
- insert/delete row
""".format(self.name)


class TableEditorTestSuite(sublime_plugin.TextCommand):
    COMMAND_TIMEOUT = 250
    TEST_TIMEOUT = 500

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)

    def run(self):
        tests = []
        tests.append(SimpleTableTest())
        tests.append(MoveColumnTest())
        tests.append(CustomAlignTest())
        tests.append(RowsTableTest())
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
            print "run test", test.name
        command = test.commands[command_ind]
        self.view.run_command(command.name, command.args)
        if command_ind + 1 < len(test.commands):
            sublime.set_timeout(lambda: self.run_tests(tests, test_ind, command_ind + 1),
                        TableEditorTestSuite.COMMAND_TIMEOUT)
        else:
            text = self.get_buffer_text()
            if text != tests[test_ind].expected_value():
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
        view.run_command("table_editor_enable_for_current_view")
        view.set_name("Sublime Table Editor Film")
        suite = TableEditorTestSuite(view)
        suite.run()
