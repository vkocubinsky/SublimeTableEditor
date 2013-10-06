# table_plugin.py - sublime plugins for pretty print text table

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
import re

try:
    from . import table_lib as tlib
    from . import table_base as tbase
except ValueError:
    import table_lib as tlib
    import table_base as tbase


class TableContext:

    def __init__(self, view, sel, syntax):
        self.view = view
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        self.syntax = syntax

        self.first_table_row = self._get_first_table_row(sel_row, sel_col)
        self.last_table_row = self._get_last_table_row(sel_row, sel_col)
        self.table_text = self._get_table_text(self.first_table_row, self.last_table_row)
        self.visual_field_num = self._visual_field_num(sel_row, sel_col)
        self.row_num = sel_row - self.first_table_row

        self.table_pos = tbase.TablePos(self.row_num, self.visual_field_num)

        self.table = self.syntax.table_parser.parse_text(self.table_text)
        self.table_driver = self.syntax.table_driver
        self.field_num = self.table_driver.visual_to_internal_index(self.table, self.table_pos).field_num

    def _get_table_text(self, first_table_row, last_table_row):
        begin_point = self.view.line(self.view.text_point(first_table_row, 0)
                                     ).begin()
        end_point = self.view.line(self.view.text_point(last_table_row, 0)
                                   ).end()
        return self.view.substr(sublime.Region(begin_point, end_point))

    def _get_last_table_row(self, sel_row, sel_col):
        row = sel_row
        last_table_row = sel_row
        last_line = self.view.rowcol(self.view.size())[0]
        while (row <= last_line and self._is_table_row(row)):
            last_table_row = row
            row = row + 1
        return last_table_row

    def _get_first_table_row(self, sel_row, sel_col):
        row = sel_row
        first_table_row = sel_row
        while (row >= 0 and self._is_table_row(row)):
            first_table_row = row
            row = row - 1
        return first_table_row

    def _is_table_row(self, row):
        text = self._get_text(row)
        return self.syntax.table_parser.is_table_row(text)

    def _visual_field_num(self, sel_row, sel_col):
        line_text = self._get_text(sel_row)
        line = self.syntax.line_parser.parse(line_text)
        return line.field_num(sel_col)

    def _get_text(self, row):
        point = self.view.text_point(row, 0)
        region = self.view.line(point)
        text = self.view.substr(region)
        return text


class AbstractTableCommand(sublime_plugin.TextCommand):

    def detect_syntax(self):
        if self.view.settings().has("table_editor_syntax"):
            syntax_name = self.view.settings().get("table_editor_syntax")
        else:
            syntax_name = self.auto_detect_syntax_name()

        table_configuration = tbase.TableConfiguration()

        border_style = (self.view.settings().get("table_editor_border_style", None)
                        or self.view.settings().get("table_editor_style", None))
        if border_style == "emacs":
            table_configuration.hline_out_border = '|'
            table_configuration.hline_in_border = '+'
        elif border_style == "grid":
            table_configuration.hline_out_border = '+'
            table_configuration.hline_in_border = '+'
        elif border_style == "simple":
            table_configuration.hline_out_border = '|'
            table_configuration.hline_in_border = '|'

        if self.view.settings().has("table_editor_custom_column_alignment"):
            table_configuration.custom_column_alignment = self.view.settings().get("table_editor_custom_column_alignment")

        if self.view.settings().has("table_editor_keep_space_left"):
            table_configuration.keep_space_left = self.view.settings().get("table_editor_keep_space_left")

        if self.view.settings().has("table_editor_align_number_right"):
            table_configuration.align_number_right = self.view.settings().get("table_editor_align_number_right")

        if self.view.settings().has("table_editor_detect_header"):
            table_configuration.detect_header = self.view.settings().get("table_editor_detect_header")

        if self.view.settings().has("table_editor_intelligent_formatting"):
            table_configuration.intelligent_formatting = self.view.settings().get("table_editor_intelligent_formatting")

        syntax = tlib.create_syntax(syntax_name, table_configuration)
        return syntax

    def auto_detect_syntax_name(self):
        view_syntax = self.view.settings().get('syntax')
        if (view_syntax == 'Packages/Markdown/MultiMarkdown.tmLanguage' or
                view_syntax == 'Packages/Markdown/Markdown.tmLanguage'):
            return "MultiMarkdown"
        elif view_syntax == 'Packages/Textile/Textile.tmLanguage':
            return "Textile"
        elif (view_syntax == 'Packages/RestructuredText/reStructuredText.tmLanguage'):
            return "reStructuredText"
        else:
            return "Simple"

    def merge(self, edit, ctx):
        table = ctx.table
        new_lines = table.render_lines()
        first_table_row = ctx.first_table_row
        last_table_row = ctx.last_table_row
        rows = range(first_table_row, last_table_row + 1)
        for row, new_text in zip(rows, new_lines):
            region = self.view.line(self.view.text_point(row, 0))
            old_text = self.view.substr(region)
            if old_text != new_text:
                self.view.replace(edit, region, new_text)

        #case 1: some lines inserted
        if len(rows) < len(new_lines):
            row = last_table_row
            for new_text in new_lines[len(rows):]:
                end_point = self.view.line(self.view.text_point(row, 0)).end()
                self.view.insert(edit, end_point, "\n" + new_text)
                row = row + 1
        #case 2: some lines deleted
        elif len(rows) > len(new_lines):
            for row in rows[len(new_lines):]:
                region = self.view.line(self.view.text_point(row, 0))
                self.view.erase(edit, region)

    def create_context(self, sel):
        return TableContext(self.view, sel, self.detect_syntax())

    def run(self, edit):
        new_sels = []
        for sel in self.view.sel():
            new_sel = self.run_one_sel(edit, sel)
            new_sels.append(new_sel)
        self.view.sel().clear()
        for sel in new_sels:
            self.view.sel().add(sel)
            self.view.show(sel, False)

    def run_one_sel(self, edit, sel):
        ctx = self.create_context(sel)
        try:
            msg, table_pos = self.run_operation(ctx)
            self.merge(edit, ctx)
            sublime.status_message("Table Editor: {0}".format(msg))
            return self.table_pos_sel(ctx, table_pos)
        except tbase.TableException as err:
            sublime.status_message("Table Editor: {0}".format(err))
            return self.table_pos_sel(ctx, ctx.table_pos)

    def visual_field_sel(self, ctx, row_num, visual_field_num):
        if ctx.table.empty():
            pt = self.view.text_point(ctx.first_table_row, 0)
        else:
            pos = tbase.TablePos(row_num, visual_field_num)
            col = ctx.table_driver.get_cursor(ctx.table, pos)
            pt = self.view.text_point(ctx.first_table_row + row_num, col)
        return sublime.Region(pt, pt)

    def table_pos_sel(self, ctx, table_pos):
        return self.visual_field_sel(ctx, table_pos.row_num,
                                     table_pos.field_num)

    def field_sel(self, ctx, row_num, field_num):
        if ctx.table.empty():
            visual_field_num = 0
        else:
            pos = tbase.TablePos(row_num, field_num)
            visual_field_num = ctx.table_driver.internal_to_visual_index(ctx.table, pos).field_num
        return self.visual_field_sel(ctx, row_num, visual_field_num)


class TableEditorAlignCommand(AbstractTableCommand):
    """
    Key: ctrl+shift+a
    Re-align the table without change the current table field.
    Move cursor to begin of the current table field.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_align(ctx.table, ctx.table_pos)


class TableEditorNextField(AbstractTableCommand):
    """
    Key: tab
    Re-align the table, move to the next field.
    Creates a new row if necessary.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_next_field(ctx.table, ctx.table_pos)


class TableEditorPreviousField(AbstractTableCommand):
    """
    Key: shift+tab
    Re-align, move to previous field.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_previous_field(ctx.table, ctx.table_pos)


class TableEditorNextRow(AbstractTableCommand):
    """
    Key: enter
    Re-align the table and move down to next row.
    Creates a new row if necessary.
    At the beginning or end of a line, enter still does new line.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_next_row(ctx.table, ctx.table_pos)


class TableEditorMoveColumnLeft(AbstractTableCommand):
    """
    Key: alt+left
    Move the current column left.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_move_column_left(ctx.table,
                                                        ctx.table_pos)


class TableEditorMoveColumnRight(AbstractTableCommand):
    """
    Key: alt+right
    Move the current column right.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_move_column_right(ctx.table,
                                                         ctx.table_pos)


class TableEditorDeleteColumn(AbstractTableCommand):
    """
    Key: alt+shift+left
    Kill the current column.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_delete_column(ctx.table,
                                                     ctx.table_pos)


class TableEditorInsertColumn(AbstractTableCommand):
    """
    Keys: alt+shift+right
    Insert a new column to the left of the cursor position.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_insert_column(ctx.table,
                                                     ctx.table_pos)


class TableEditorKillRow(AbstractTableCommand):
    """
    Key : alt+shift+up
    Kill the current row.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_kill_row(ctx.table, ctx.table_pos)


class TableEditorInsertRow(AbstractTableCommand):
    """
    Key: alt+shift+down
    Insert a new row above the current row.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_insert_row(ctx.table, ctx.table_pos)


class TableEditorMoveRowUp(AbstractTableCommand):
    """
    Key: alt+up
    Move the current row up.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_move_row_up(ctx.table, ctx.table_pos)


class TableEditorMoveRowDown(AbstractTableCommand):
    """
    Key: alt+down
    Move the current row down.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_move_row_down(ctx.table,
                                                     ctx.table_pos)


class TableEditorInsertSingleHline(AbstractTableCommand):
    """
    Key: ctrl+k,-
    Insert single horizontal line below current row.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_insert_single_hline(ctx.table,
                                                           ctx.table_pos)


class TableEditorInsertDoubleHline(AbstractTableCommand):
    """
    Key: ctrl+k,=
    Insert double horizontal line below current row.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_insert_double_hline(ctx.table,
                                                           ctx.table_pos)


class TableEditorHlineAndMove(AbstractTableCommand):
    """
    Key: ctrl+k, enter
    Insert a horizontal line below current row,
    and move the cursor into the row below that line.
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_insert_hline_and_move(ctx.table,
                                                             ctx.table_pos)


class TableEditorSplitColumnDown(AbstractTableCommand):
    """
    Key: alt+enter
    Split rest of cell down from current cursor position,
    insert new line bellow if current row is last row in the table
    or if next line is hline
    """
    def remove_rest_line(self, edit, sel):
        end_region = self.view.find("\|",
                                    sel.begin())
        rest_region = sublime.Region(sel.begin(), end_region.begin())
        rest_data = self.view.substr(rest_region)
        self.view.replace(edit, rest_region, "")
        return rest_data.strip()

    def run_one_sel(self, edit, sel):
        ctx = self.create_context(sel)
        field_num = ctx.field_num
        row_num = ctx.row_num
        if (ctx.table[row_num].is_separator() or
                ctx.table[row_num].is_header_separator()):
            sublime.status_message("Table Editor: Split column is not "
                                   "permitted for separator or header "
                                   "separator line")
            return self.table_pos_sel(ctx, ctx.table_pos)
        if row_num + 1 < len(ctx.table):
            if len(ctx.table[row_num + 1]) - 1 < field_num:
                sublime.status_message("Table Editor: Split column is not "
                                       "permitted for short line")
                return self.table_pos_sel(ctx, ctx.table_pos)
            elif ctx.table[row_num + 1][field_num].pseudo():
                sublime.status_message("Table Editor: Split column is not "
                                       "permitted to colspan column")
                return self.table_pos_sel(ctx, ctx.table_pos)

        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        rest_data = self.remove_rest_line(edit, sel)

        ctx = self.create_context(sel)

        field_num = ctx.field_num
        row_num = ctx.row_num

        if row_num + 1 == len(ctx.table) or ctx.table[row_num + 1].is_separator():
            ctx.table.insert_empty_row(row_num + 1)

        row_num = row_num + 1
        ctx.table[row_num][field_num].data = rest_data + " " + ctx.table[row_num][field_num].data.strip()
        ctx.table.pack()
        self.merge(edit, ctx)
        sublime.status_message("Table Editor: Column splitted down")
        return self.field_sel(ctx, row_num, field_num)


class TableEditorJoinLines(AbstractTableCommand):
    """
    Key: ctrl+j
    Join current row and next row into one if next row is not hline
    """
    def run_operation(self, ctx):
        return ctx.table_driver.editor_join_lines(ctx.table, ctx.table_pos)


class TableEditorCsvToTable(AbstractTableCommand):
    """
    Command: table_csv_to_table
    Key: ctrl+k, |
    Convert selected CSV region into table
    """

    def run_one_sel(self, edit, sel):
        if sel.empty():
            return sel
        else:
            syntax = self.detect_syntax()
            text = self.view.substr(sel)
            table = syntax.table_driver.parse_csv(text)
            self.view.replace(edit, sel, table.render())

            first_row = self.view.rowcol(sel.begin())[0]

            pt = self.view.text_point(first_row, syntax.table_driver.get_cursor(table, tbase.TablePos(0, 0)))
            sublime.status_message("Table Editor: Table created from CSV")
            return sublime.Region(pt, pt)


class TableEditorDisableForCurrentView(sublime_plugin.TextCommand):

    def run(self, args, prop):
        self.view.settings().set(prop, False)


class TableEditorEnableForCurrentView(sublime_plugin.TextCommand):

    def run(self, args, prop):
        self.view.settings().set(prop, True)


class TableEditorDisableForCurrentSyntax(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax = self.view.settings().get('syntax')
        if syntax is not None:
            m = re.search("([^/]+)[.]tmLanguage$", syntax)
            if m:
                base_name = m.group(1) + ".sublime-settings"
                settings = sublime.load_settings(base_name)
                settings.erase("enable_table_editor")
                sublime.save_settings(base_name)


class TableEditorEnableForCurrentSyntax(sublime_plugin.TextCommand):

    def run(self, edit):
        syntax = self.view.settings().get('syntax')
        if syntax is not None:
            m = re.search("([^/]+)[.]tmLanguage$", syntax)
            if m:
                base_name = m.group(1) + ".sublime-settings"
                settings = sublime.load_settings(base_name)
                settings.set("enable_table_editor", True)
                sublime.save_settings(base_name)


class TableEditorSetSyntax(sublime_plugin.TextCommand):

    def run(self, edit, syntax):
        self.view.settings().set("enable_table_editor", True)
        self.view.settings().set("table_editor_syntax", syntax)
        sublime.status_message("Table Editor: set syntax to '{0}'"
                               .format(syntax))
