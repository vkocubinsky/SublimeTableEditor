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
import csv
import re
import tablelib


class AbstractTableCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        sublime_plugin.TextCommand.__init__(self, view)
        style_name = self.view.settings().get("table_editor_style")
        if style_name == "emacs":
            self.style = tablelib.emacs_style
        elif style_name == "grid":
            self.style = tablelib.grid_style
        else:
            self.style = tablelib.simple_style

    def csv2table(self, text):
        lines = []
        try:
            vline = self.style.vline
            dialect = csv.Sniffer().sniff(text)
            table_reader = csv.reader(text.splitlines(), dialect)
            for row in table_reader:
                lines.append(vline + vline.join(row) + vline)
        except csv.Error:
            for row in text.splitlines():
                lines.append(vline + row + vline)
        return "\n".join(lines)

    def find_border(self, text, num):
        if self.style.is_hline(text):
            pattern = self.style.hline_border_pattern()
        else:
            pattern = self.style.vline_pattern()
        it = re.finditer(pattern, text)
        index = -1
        for i in range(num):
            try:
                mo = it.next()
                index = mo.start()
            except StopIteration:
                index = -1
        return index

    def hline_count(self, text, start, end):
        if self.style.is_hline(text):
            return sum([text.count(ch, start, end)
                                            for ch in self.style.hline_borders])
        else:
            return text.count(self.style.vline, start, end)

    def get_text(self, row):
        point = self.view.text_point(row, 0)
        region = self.view.line(point)
        text = self.view.substr(region)
        return text

    def get_full_text(self, row):
        point = self.view.text_point(row, 0)
        region = self.view.full_line(point)
        text = self.view.substr(region)
        return text

    def get_row(self, point):
        return self.view.rowcol(point)[0]

    def is_hline_row(self, row):
        return self.style.is_hline(self.get_text(row))

    def is_table_row(self, row):
        return re.match(r"^\s*" + self.style.hline_border_pattern(), self.get_text(row)) is not None

    def get_field_num(self, row, col):
        return self.hline_count(self.get_text(row), 0, col) - 1

    def get_field_count(self, row):
        text = self.get_text(row)
        return self.hline_count(text, 0, len(text)) - 1

    def get_last_buffer_row(self):
        return self.view.rowcol(self.view.size())[0]

    def get_field_default_point(self, row, field_num):
        text = self.get_text(row)
        i1 = self.find_border(text, field_num + 1)
        i2 = self.find_border(text, field_num + 2)
        match = re.compile(r"([^\s])\s*$").search(text, i1 + 1, i2)
        if match:
            return self.view.text_point(row, match.start(1) + 1)
        else:
            return self.view.text_point(row, i1 + 2)

    def get_field_begin_point(self, row, field_num):
        text = self.get_text(row)
        i1 = self.find_border(text, field_num + 1)
        i2 = self.find_border(text, field_num + 2)
        match = re.compile(r"\s*([^\s]).*$").match(text, i1 + 1, i2)
        if match:
            return self.view.text_point(row, match.start(1))
        else:
            return self.view.text_point(row, i1 + 2)

    def get_last_table_row(self, row):
        last_table_row = row
        last_line = self.get_last_buffer_row()
        while (row <= last_line and self.is_table_row(row)):
            last_table_row = row
            row = row + 1
        return last_table_row

    def get_first_table_row(self, row):
        first_table_row = row
        while (row >= 0 and self.is_table_row(row)):
            first_table_row = row
            row = row - 1
        return first_table_row

    def clone_as_empty_line(self, text):
        if self.style.is_hline(text):
            text = re.sub(self.style.hline_border_pattern(), self.style.vline, text)

        i1 = self.find_border(text, 1)
        return text[:i1] + re.sub(self.style.not_vline_pattern(), ' ', text[i1:])

    def clone_as_hline(self, text, hline='-'):
        if self.style.is_hline(text):
            return text[:]
        i1 = text.find(self.style.vline)
        i2 = text.rfind(self.style.vline)
        in_text = text[i1 + 1:i2]
        in_text = re.sub(self.style.not_vline_pattern(), hline, in_text)
        in_text = re.sub(self.style.vline_pattern(), self.style.hline_in_border, in_text)
        return (text[:i1]
                + self.style.hline_out_border
                + in_text
                + self.style.hline_out_border
                + text[i2 + 1:])

    def duplicate_as_hrow(self, edit, row, hline='-'):
        point = self.view.text_point(row, 0)
        region = self.view.line(point)
        text = self.view.substr(region)
        new_text = "\n" + self.clone_as_hline(text, hline)
        self.view.insert(edit, region.end(), new_text)

    def duplicate_as_empty_row(self, edit, row):
        point = self.view.text_point(row, 0)
        region = self.view.line(point)
        text = self.view.substr(region)
        new_text = "\n" + self.clone_as_empty_line(text)
        self.view.insert(edit, region.end(), new_text)


class AbstractTableMultiSelect(AbstractTableCommand):

    def get_unformatted_field_num(self, sel_row, sel_col):
        line_text = self.get_text(sel_row)
        sel_field_num = self.hline_count(line_text, 0, sel_col) - 1
        if self.style.is_hline(line_text):
            pattern = self.style.hline_border_pattern() + r"\s*$"
        else:
            pattern = self.style.vline_pattern() + r"\s*$"
        if sel_field_num > 0 and re.search(pattern, line_text):
            sel_field_num = sel_field_num - 1
        return sel_field_num

    def align_one_sel(self, edit, sel):
        (sel_row, sel_col) = self.view.rowcol(sel.begin())

        first_table_row = self.get_first_table_row(self.get_row(sel.begin()))
        last_table_row = self.get_last_table_row(self.get_row(sel.begin()))

        begin_point = self.view.line(
                            self.view.text_point(first_table_row, 0)
                                    ).begin()
        end_point = self.view.line(
                            self.view.text_point(last_table_row, 0)
                                    ).end()

        table_region = sublime.Region(begin_point, end_point)
        text = self.view.substr(table_region)
        sel_field_num = self.get_unformatted_field_num(sel_row, sel_col)
        new_text_lines = tablelib.format_to_lines(text, self.style)
        row = first_table_row
        while row <= last_table_row:
            if row - first_table_row >= len(new_text_lines):
                break
            point = self.view.text_point(row, 0)
            region = self.view.line(point)
            line_text = self.view.substr(region)
            new_line_text = new_text_lines[row - first_table_row]
            if line_text != new_line_text:
                self.view.replace(edit, region, new_line_text)
            row = row + 1
        if len(new_text_lines) != last_table_row - first_table_row + 1:
            print "WARN", "len formatted table", len(new_text_lines),
            print "len sublime table", last_table_row - first_table_row + 1
        pt = self.get_field_default_point(sel_row, sel_field_num)
        return sublime.Region(pt, pt)

    def run(self, edit):
        new_sels = []
        for sel in self.view.sel():
            if not self.is_table_row(self.get_row(sel.begin())):
                new_sels.append(sel)
                continue
            new_sel = self.run_one_sel(edit, sel)
            new_sels.append(new_sel)
        self.view.sel().clear()
        for sel in new_sels:
            self.view.sel().add(sel)
            self.view.show(sel, False)

    def run_one_sel(self, edit, sel):
        return sel


class TableEditorAlignCommand(AbstractTableMultiSelect):
    """
    Key: ctrl+shift+a
    Re-align the table without change the current table field.
    Move cursor to begin of the current table field.
    """

    def run_one_sel(self, edit, sel):
        return self.align_one_sel(edit, sel)


class TableEditorNextField(AbstractTableMultiSelect):
    """
    Key: tab
    Re-align the table, move to the next field.
    Creates a new row if necessary.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        last_table_row = self.get_last_table_row(sel_row)
        field_count = self.get_field_count(sel_row)
        moved = False
        while True:
            if self.is_hline_row(sel_row):
                if sel_row < last_table_row:
                    sel_row = sel_row + 1
                    field_num = 0
                    moved = True
                    continue
                else:
                    #sel_row == last_table_row
                    self.duplicate_as_empty_row(edit, sel_row)
                    field_num = 0
                    sel_row += 1
                    break
            elif moved:
                break
            elif field_num + 1 < field_count:
                field_num = field_num + 1
                break
            elif sel_row < last_table_row:
                field_num = 0
                sel_row = sel_row + 1
                moved = True
                continue
            else:
                #sel_row == last_table_row
                self.duplicate_as_empty_row(edit, sel_row)
                field_num = 0
                sel_row += 1
                break
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorPreviousField(AbstractTableMultiSelect):
    """
    Key: shift+tab
    Re-align, move to previous field.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        first_table_row = self.get_first_table_row(sel_row)
        moved = False
        while True:
            if self.is_hline_row(sel_row):
                if sel_row > first_table_row:
                    sel_row = sel_row - 1
                    field_num = self.get_field_count(sel_row) - 1
                    moved = True
                    continue
                else:
                    #sel_row == first_table_row:
                    field_num = 0
                    break
            elif moved:
                break
            elif field_num > 0:
                field_num = field_num - 1
                break
            elif sel_row > first_table_row:
                sel_row = sel_row - 1
                field_num = self.get_field_count(sel_row) - 1
                moved = True
                continue
            else:
                #sel_row == first_table_row:
                break
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorNextRow(AbstractTableMultiSelect):
    """
    Key: enter
    Re-align the table and move down to next row.
    Creates a new row if necessary.
    At the beginning or end of a line, enter still does new line.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        if sel_row < self.get_last_table_row(sel_row):
            if self.is_hline_row(sel_row + 1):
                self.duplicate_as_empty_row(edit, sel_row)
        else:
            self.duplicate_as_empty_row(edit, sel_row)
        sel_row += 1
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorMoveColumnLeft(AbstractTableMultiSelect):
    """
    Key: alt+left
    Move the current column right.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        if field_num == 0:
            return sel
        start_row = self.get_first_table_row(sel_row)
        end_row = self.get_last_table_row(sel_row)
        row = start_row
        while row <= end_row:
            if self.is_hline_row(row):
                in_border = self.style.hline_in_border
            else:
                in_border = self.style.vline

            text = self.get_text(row)
            i1 = self.find_border(text, field_num + 0)
            i2 = self.find_border(text, field_num + 1)
            i3 = self.find_border(text, field_num + 2)
            new_text = (text[0:i1 + 1]
                        + text[i2 + 1:i3]
                        + in_border
                        + text[i1 + 1:i2]
                        + text[i3:]
                        )
            self.view.replace(edit,
                        self.view.line(self.view.text_point(row, sel_col)),
                        new_text
                            )
            row += 1
        pt = self.get_field_default_point(sel_row, field_num - 1)
        return sublime.Region(pt, pt)


class TableEditorMoveColumnRight(AbstractTableMultiSelect):
    """
    Key: alt+right
    Move the current column right.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        if field_num == self.get_field_count(sel_row) - 1:
            return sel
        first_table_row = self.get_first_table_row(sel_row)
        last_table_row = self.get_last_table_row(sel_row)
        row = first_table_row

        while row <= last_table_row:
            if self.is_hline_row(row):
                in_border = self.style.hline_in_border
            else:
                in_border = self.style.vline

            text = self.get_text(row)
            i1 = self.find_border(text, field_num + 1)
            i2 = self.find_border(text, field_num + 2)
            i3 = self.find_border(text, field_num + 3)
            new_text = (text[0:i1 + 1]
                        + text[i2 + 1:i3]
                        + in_border
                        + text[i1 + 1:i2]
                        + text[i3:])
            self.view.replace(edit,
                        self.view.line(self.view.text_point(row, sel_col)),
                        new_text
                            )
            row += 1
        pt = self.get_field_default_point(sel_row, field_num + 1)
        return sublime.Region(pt, pt)


class TableEditorDeleteColumn(AbstractTableMultiSelect):
    """
    Key: alt+shift+left
    Kill the current column.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)

        first_table_row = self.get_first_table_row(sel_row)
        last_table_row = self.get_last_table_row(sel_row)
        row = first_table_row
        field_count = self.get_field_count(sel_row)
        while row <= last_table_row:
            text = self.get_text(row)
            i1 = self.find_border(text, field_num + 1)
            i2 = self.find_border(text, field_num + 2)
            if field_count > 1:
                if self.style.is_hline(text):
                    if field_num == 0 or field_num == field_count - 1:
                        vline = self.style.hline_out_border
                    else:
                        vline = self.style.hline_in_border
                else:
                    vline = self.style.vline
                self.view.replace(edit,
                        self.view.line(self.view.text_point(row, sel_col)),
                        text[0:i1] + vline + text[i2 + 1:])
            else:
                self.view.replace(edit,
                        self.view.line(self.view.text_point(row, sel_col)),
                        text[0:i1] + text[i2 + 1:])

            row += 1
        if field_num == self.get_field_count(sel_row):
            field_num -= 1
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorInsertColumn(AbstractTableMultiSelect):
    """
    Keys: alt+shift+right
    Insert a new column to the left of the cursor position.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)

        first_table_row = self.get_first_table_row(sel_row)
        last_table_row = self.get_last_table_row(sel_row)
        row = first_table_row
        while row <= last_table_row:
            text = self.get_text(row)
            if self.style.is_single_hline(text):
                cell = "---"
            elif self.style.is_double_hline(text):
                cell = "==="
            else:
                cell = "   "
            i1 = self.find_border(text, field_num + 1)
            if self.style.is_hline(text):
                if field_num == 0:
                    vline = self.style.hline_out_border
                else:
                    vline = self.style.hline_in_border
                new_text = (text[0:i1]
                            + vline
                            + cell
                            + self.style.hline_in_border
                            + text[i1 + 1:])
            else:
                new_text = (text[0:i1]
                            + self.style.vline
                            + cell
                            + self.style.vline
                            + text[i1 + 1:])
            self.view.replace(edit,
                    self.view.line(self.view.text_point(row, sel_col)),
                    new_text)

            row += 1
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorKillRow(AbstractTableMultiSelect):
    """
    Key : alt+shift+up
    Kill the current row or horizontal line.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        if (self.get_first_table_row(sel_row) ==
                                            self.get_last_table_row(sel_row)):
            self.view.erase(edit, self.view.full_line(sel))
            pt = self.view.text_point(sel_row, 0)
        elif sel_row == self.get_last_table_row(sel_row):
            self.view.erase(edit, self.view.full_line(sel))
            sel_row = sel_row - 1
            pt = self.get_field_default_point(sel_row, field_num)
        else:
            self.view.erase(edit, self.view.full_line(sel))
            pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorInsertRow(AbstractTableMultiSelect):
    """
    Key: alt+shift+down
    Insert a new row above the current row.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        field_num = self.get_field_num(sel_row, sel_col)
        line_region = self.view.line(sel)
        text = self.view.substr(line_region)
        new_text = self.clone_as_empty_line(text) + "\n"
        self.view.insert(edit, line_region.begin(), new_text)
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorMoveRowUp(AbstractTableCommand):
    """
    Key: alt+up
    Move the current row up.
    """

    def run(self, edit):
        allow = True
        for sel in self.view.sel():
            row = self.get_row(sel.begin())
            if row == self.get_first_table_row(row):
                allow = False
                break
        if allow:
            self.view.run_command("swap_line_up")


class TableEditorMoveRowDown(AbstractTableCommand):
    """
    Key: alt+down
    Move the current row down.
    """

    def run(self, edit):
        allow = True
        for sel in self.view.sel():
            row = self.get_row(sel.begin())
            if row == self.get_last_table_row(row):
                allow = False
                break
        if allow:
            self.view.run_command("swap_line_down")


class TableEditorInsertSingleHline(AbstractTableMultiSelect):
    """
    Key: ctrl+k,-
    Insert single horizontal line below current row.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        self.duplicate_as_hrow(edit, sel_row)
        field_num = self.get_field_num(sel_row, sel_col)
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorInsertDoubleHline(AbstractTableMultiSelect):
    """
    Key: ctrl+k,=
    Insert double horizontal line below current row.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        self.duplicate_as_hrow(edit, sel_row, "=")
        field_num = self.get_field_num(sel_row, sel_col)
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorHlineAndMove(AbstractTableMultiSelect):
    """
    Key: ctrl+k, enter
    Insert a horizontal line below current row,
    and move the cursor into the row below that line.
    """

    def run_one_sel(self, edit, sel):
        sel = self.align_one_sel(edit, sel)
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        self.duplicate_as_hrow(edit, sel_row)
        if sel_row + 1 < self.get_last_table_row(sel_row):
            if self.is_hline_row(sel_row + 2):
                self.duplicate_as_empty_row(edit, sel_row + 1)
        else:
            self.duplicate_as_empty_row(edit, sel_row + 1)
        sel_row = sel_row + 2
        pt = self.get_field_default_point(sel_row, 0)
        return sublime.Region(pt, pt)


class TableEditorSplitColumnDown(AbstractTableMultiSelect):
    """
    Key: alt+enter
    Split rest of cell down from current cursor position,
    insert new line bellow if current row is last row in the table
    or if next line is hline
    """
    def remove_rest_line(self, edit, sel):
        end_region = self.view.find(r'\|', sel.begin())
        rest_region = sublime.Region(sel.begin(), end_region.begin())
        rest_data = self.view.substr(rest_region)
        self.view.replace(edit, rest_region, "")
        return rest_data.strip()

    def run_one_sel(self, edit, sel):
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        rest_data = self.remove_rest_line(edit, sel)
        sel = self.align_one_sel(edit, sel)
        if (sel_row == self.get_last_table_row(sel_row)
                or self.is_hline_row(sel_row + 1)):
            self.duplicate_as_empty_row(edit, sel_row)
            sel_row = sel_row + 1
        else:
            sel_row = sel_row + 1
        field_num = self.get_field_num(sel_row, sel_col)
        pt = self.get_field_begin_point(sel_row, field_num)
        self.view.insert(edit, pt, rest_data + " ")
        sel = self.align_one_sel(edit, sel)
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorJoinLines(AbstractTableMultiSelect):
    """
    Key: ctrl+j
    Join current row and next row into one if next row is not hline
    """
    def run_one_sel(self, edit, sel):
        (sel_row, sel_col) = self.view.rowcol(sel.begin())
        sel = self.align_one_sel(edit, sel)
        field_num = self.get_field_num(sel_row, sel_col)
        vline = self.style.vline
        if (sel_row < self.get_last_table_row(sel_row)
                and not self.is_hline_row(sel_row)
                and not self.is_hline_row(sel_row + 1)):
            curr_line = self.get_text(sel_row)
            next_line = self.get_text(sel_row + 1)
            cols = [f1.strip() + " " + f2.strip()
                for f1, f2 in zip(curr_line.split(vline), next_line.split(vline))]
            new_line = vline.join(cols) + "\n"

            curr_region = self.view.full_line(
                                self.view.text_point(sel_row, 0))
            next_region = self.view.full_line(
                    self.view.text_point(sel_row + 1, 0))

            self.view.erase(edit, sublime.Region(
                                                curr_region.begin(),
                                                next_region.end()
                                                ))
            self.view.insert(edit, curr_region.begin(), new_line)
            self.align_one_sel(edit, sublime.Region(
                                                curr_region.begin(),
                                                curr_region.begin()
                                                    ))
        pt = self.get_field_default_point(sel_row, field_num)
        return sublime.Region(pt, pt)


class TableEditorDisableForCurrentView(sublime_plugin.TextCommand):

    def run(self, args):
        self.view.settings().erase("enable_table_editor")


class TableEditorEnableForCurrentView(sublime_plugin.TextCommand):

    def run(self, args):
        self.view.settings().set("enable_table_editor", True)


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


class TableEditorCsvToTable(AbstractTableCommand):
    """
    Command: table_csv_to_table
    Key: ctrl+k, |
    Convert selected CSV region into table
    """
    def run(self, edit):
        new_sels = []
        for sel in self.view.sel():
            (sel_row, sel_col) = self.view.rowcol(sel.begin())
            if sel.empty():
                new_sels.append(sel)
            else:
                text = self.view.substr(sel)
                new_text = self.csv2table(text)
                self.view.replace(edit, sel, new_text)
                pt = self.get_field_default_point(sel_row, 0)
                new_sels.append(sublime.Region(pt, pt))
        self.view.sel().clear()
        for sel in new_sels:
            self.view.sel().add(sel)
            self.view.show(sel, False)
        self.view.run_command("table_editor_align")
