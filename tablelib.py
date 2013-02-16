# tablelib.py - pretty print text table.

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

import re


class TableSyntax:

    def __init__(self, hline_out_border='|',
                       hline_in_border='|',
                       custom_column_alignment=False,
                       multi_markdown_column_alignment=False,
                       textile_cell_alignment=False):
        self.vline = '|'
        self.hline_out_border = hline_out_border
        self.hline_in_border = hline_in_border
        #characters from all styles correct switch from one style to other
        self.hline_borders = ['+', '|']
        self.custom_column_alignment = custom_column_alignment
        self.multi_markdown_column_alignment = multi_markdown_column_alignment
        self.textile_cell_alignment = textile_cell_alignment

    def __str__(self):
        return """
{0} a {0} b {0}
{1}---{2}---{1}
{0} c {0} d {0}
""".format(
                    self.vline,
                    self.hline_out_border,
                    self.hline_in_border
                    )

    def hline_border_pattern(self):
        return "(?:" + "|".join(["(?:" + re.escape(ch) + ")" for ch in self.hline_borders]) + ")"

    def vline_pattern(self):
        return "(?:" + re.escape(self.vline) + ")"

    def not_vline_pattern(self):
        return "([^" + re.escape(self.vline) + "])"

    def single_hline_pattern(self):
        return r"(^\s*({border}|{line})+\s*$)".format(border=self.hline_border_pattern(),
                                                line=r"(\s*[\-]+\s*)")

    def double_hline_pattern(self):
        return r"(^\s*({border}|{line})+\s*$)".format(border=self.hline_border_pattern(),
                                                line=r"(\s*[\=]+\s*)")

    def is_single_hline(self, text):
        return re.match(self.single_hline_pattern(), text) is not None

    def is_double_hline(self, text):
        return re.match(self.double_hline_pattern(), text) is not None

    def is_hline(self, text):
        return self.is_single_hline(text) or self.is_double_hline(text)


simple_syntax = TableSyntax(hline_out_border='|',
                          hline_in_border='|',
                          custom_column_alignment=True,
                          multi_markdown_column_alignment=False,
                          textile_cell_alignment=False)

emacs_org_mode_syntax = TableSyntax(hline_out_border='|',
                          hline_in_border='+',
                          custom_column_alignment=False,
                          multi_markdown_column_alignment=False,
                          textile_cell_alignment=False)

pandoc_syntax = TableSyntax(hline_out_border='+',
                          hline_in_border='+',
                          custom_column_alignment=False,
                          multi_markdown_column_alignment=False,
                          textile_cell_alignment=False)

re_structured_text_syntax = TableSyntax(hline_out_border='+',
                                      hline_in_border='+',
                                      custom_column_alignment=False,
                                      multi_markdown_column_alignment=False,
                                      textile_cell_alignment=False)

multi_markdown_syntax = TableSyntax(hline_out_border='|',
                                  hline_in_border='|',
                                  custom_column_alignment=False,
                                  multi_markdown_column_alignment=True,
                                  textile_cell_alignment=False)


textile_syntax = TableSyntax(hline_out_border='|',
                           hline_in_border='|',
                           custom_column_alignment=False,
                           multi_markdown_column_alignment=False,
                           textile_cell_alignment=True)

class Column:
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'
    ALIGN_CENTER = 'center'

    def __init__(self, row):
        self.row = row
        self.col_len = 0
        self.align =  Column.ALIGN_LEFT


class DataColumn(Column):

    def __init__(self, row, data):
        Column.__init__(self, row)
        self.data = self._norm(data)

    def _norm(self, col):
        col = col.strip()
        if len(col) == 0:
            return '   '
        if col[0] != ' ':
            col = ' ' + col
        if (col[-1] != ' '):
            col = col + ' '
        return col

    def new_empty_column(self):
        return DataColumn(self.row,'')

    def render(self):
        if data_alignment[col_ind] == Column.ALIGN_RIGHT:
            column.data = column.data.rjust(col_len, ' ')
        elif data_alignment[col_ind] == Column.ALIGN_LEFT:
            column.data = column.data.ljust(col_len, ' ')
        elif data_alignment[col_ind] == Column.ALIGN_CENTER:
            column.data = column.data.center(col_len, ' ')


class SeparatorColumn(Column):
    def __init__(self, row, separator):
        Column.__init__(self, row)
        self.separator = separator
        self.data = separator * 3

    def new_empty_column(self):
        return SeparatorColumn(self.row,self.separator)

    def render(self):
        column.data = self.separator * col_len


class CustomAlignColumn(Column):
    ALIGN_MAP = {'<': Column.ALIGN_LEFT,
                 '>': Column.ALIGN_RIGHT,
                 '#': Column.ALIGN_CENTER}

    def __init__(self, row, data):
        Column.__init__(self, row)
        self.align_char = re.search(r"[\<]|[\>]|[\#]", self.data).group(0)
        self.data = ' ' + self.align_char + ' '

    def align_follow(self):
        return CustomAlignColumn.ALIGN_MAP[self.align_char]

    def new_empty_column(self):
        return CustomAlignColumn(self.row,'#')

    def render(self):
        column.data = ' ' + self.align_char * (col_len - 2) + ' '




class MultiMarkdownAlignColumn(Column):
    def __init__(self, row, data):
        Column.__init__(self, row)
        self.data = ' ' + self._norm(data) + ' '

    def _norm(self, col):
        col = col.strip()
        if col.count(':') == 2:
            return ':-:'
        elif col[0] == ':':
            return ':-'
        elif col[-1] == ':':
            return '-:'
        else:
            return '-'


    def new_empty_column(self):
        return MultiMarkdownAlignColumn(self.row,'-')

    def render(self):
        if column.data.count(':') == 2:
            data_alignment[col_ind] = Column.ALIGN_CENTER
            column.data = ' :' + '-' * (col_len - 4) + ': '
        elif column.data[1] == ':':
            data_alignment[col_ind] = Column.ALIGN_LEFT
            column.data = ' :' + '-' * (col_len - 3) + ' '
        elif column.data[-2] == ':':
            data_alignment[col_ind] = Column.ALIGN_RIGHT
            column.data = ' ' + '-' * (col_len - 3) + ': '
        else:
            column.data = ' ' + '-' * (col_len - 2) + ' '


class Row:
    ROW_DATA = 'd'
    ROW_SINGLE_SEPARATOR = '-'
    ROW_DOUBLE_SEPARATOR = '='
    ROW_CUSTOM_ALIGN = '<>#'
    ROW_MULTI_MARKDOWN_ALIGN = ':-:'


    def __init__(self, table, str_cols):
        self.table = table
        self._row_type = None
        self.index = 0

        if self._is_single_row_separator(str_cols):
            self._row_type = Row.ROW_SINGLE_SEPARATOR
            self.columns = [SeparatorColumn(self,'-') for col in str_cols]
        elif self._is_double_row_separator(str_cols):
            self._row_type = Row.ROW_DOUBLE_SEPARATOR
            self.columns = [SeparatorColumn(self,'=') for col in str_cols]
        elif (self.table.syntax.custom_column_alignment and
              self._is_custom_align_row(str_cols)):
            self._row_type = Row.ROW_CUSTOM_ALIGN
            self.columns = [CustomAlignColumn(self,col) for col in str_cols]
        elif (self.table.syntax.multi_markdown_column_alignment
              and self._is_multi_markdown_align_row(str_cols)):
            self._row_type = Row.ROW_MULTI_MARKDOWN_ALIGN
            self.columns = [MultiMarkdownAlignColumn(self,col) for col in str_cols]
        else:
            self._row_type = Row.ROW_DATA
            self.columns = [DataColumn(self,col) for col in str_cols]


    @property
    def row_type(self):
        return self._row_type

    @property
    def header(self):
        return self.index < self.table.header_separator_index

    def _is_single_row_separator(self, str_cols):
        for col in str_cols:
            if not re.match(r"^\s*[\-]+\s*$", col):
                return False
        return True


    def _is_double_row_separator(self, str_cols):
        for col in str_cols:
            if not re.match(r"^\s*[\=]+\s*$", col):
                return False
        return True

    def _is_custom_align_row(self, str_cols):
        for col in str_cols:
            if not re.match(r"^\s*([\<]+|[\>]+|[\#]+)\s*$", col):
                return False
        return True

    def _is_multi_markdown_align_row(self, str_cols):
        for col in str_cols:
            if not re.match(r"^\s*([\:]?[\-]+[\:]?)\s*$", col):
                return False
        return True


    @property
    def str_cols(self):
        return [column.data for column in self.columns]

    def render(self):
        syntax = self.table.syntax
        if (self.row_type == Row.ROW_SINGLE_SEPARATOR or
            self.row_type == Row.ROW_DOUBLE_SEPARATOR):
            return (syntax.hline_out_border
                + syntax.hline_in_border.join(self.str_cols)
                + syntax.hline_out_border)
        else:
            vline = syntax.vline
            return vline + vline.join(self.str_cols) + vline


class TextTable:


    def __init__(self, text, syntax):
        self.text = text
        self.syntax = syntax
        self._rows = []
        self._col_lens = []

        self._header_found = False
        self.header_separator_index = -1
        self.first_data_index = -1


    @property
    def col_lens(self):
        return self.col_lens

    def add_row(self, row):
        row.index = len(self._rows)
        self._rows.append(row)
        if self.first_data_index == -1 and row.row_type == Row.ROW_DATA:
            self.first_data_index = row.index
        if (self.first_data_index != -1 and
            self.header_separator_index != -1 and
            (row.row_type == Row.ROW_SINGLE_SEPARATOR
                or
             row.row_type == Row.ROW_DOUBLE_SEPARATOR)
            ):
            self.header_separator_index = row.index

        new_col_lens = [len(column.data) for column in row.columns]
        if len(new_col_lens) < len(self._col_lens):
            new_col_lens.extend([0] * (len(self._col_lens) - len(new_col_lens)))
        elif len(self._col_lens) < len(new_col_lens):
            self._col_lens.extend([0] * (len(new_col_lens) - len(self._col_lens)))
        self._col_lens = [max(x, y) for x, y in zip(self._col_lens, new_col_lens)]


    def pack(self):

        self._adjust_column_count()

        for row in self._rows:
            for column, col_len in zip(row.columns, self._col_lens):
                column.col_len = col_len

        self._adjust_column_width()


    def _adjust_column_count(self):
        column_count = len(self._col_lens)
        for row in self._rows:
            column = row.columns[0]
            row.columns.extend([column.new_empty_column()] * (column_count - len(row.columns)))

    def _auto_detect_column(self, start_row_ind, col_ind):
        for row in self._rows[start_row_ind:]:
            if row.header:
                continue
            elif row.row_type == Row.ROW_CUSTOM_ALIGN:
                break
            elif row.row_type == Row.ROW_SINGLE_SEPARATOR:
                continue
            elif row.row_type == Row.ROW_DOUBLE_SEPARATOR:
                continue
            if len(row.columns[col_ind].data.strip()) > 0 and not re.match("^\s*[0-9]*[.,]?[0-9]+\s*$", row.columns[col_ind].data):
                return Column.ALIGN_LEFT
        return Column.ALIGN_RIGHT

    def _adjust_column_width(self):
        column_count = len(self._col_lens)
        row_count = len(self._rows)
        data_alignment = [None] * len(self._col_lens)
        for row_ind in range(row_count):
            row = self._rows[row_ind]
            for col_ind in range(column_count):
                column = row.columns[col_ind]
                col_len = self._col_lens[col_ind]
                if row.row_type == Row.ROW_SINGLE_SEPARATOR:
                    column.data = '-' * col_len
                elif row.row_type == Row.ROW_DOUBLE_SEPARATOR:
                    column.data = '=' * col_len
                elif row.header:
                    column.data = column.data.center(col_len, ' ')
                elif row.row_type == Row.ROW_CUSTOM_ALIGN:
                    if '<' in column.data:
                        data_alignment[col_ind] = Column.ALIGN_LEFT
                        column.data = ' ' + '<' * (col_len - 2) + ' '
                    elif '>' in column.data:
                        data_alignment[col_ind] = Column.ALIGN_RIGHT
                        column.data = ' ' + '>' * (col_len - 2) + ' '
                    elif '#' in column.data:
                        data_alignment[col_ind] = Column.ALIGN_CENTER
                        column.data = ' ' + '#' * (col_len - 2) + ' '
                elif row.row_type == Row.ROW_MULTI_MARKDOWN_ALIGN:
                    if column.data.count(':') == 2:
                        data_alignment[col_ind] = Column.ALIGN_CENTER
                        column.data = ' :' + '-' * (col_len - 4) + ': '
                    elif column.data[1] == ':':
                        data_alignment[col_ind] = Column.ALIGN_LEFT
                        column.data = ' :' + '-' * (col_len - 3) + ' '
                    elif column.data[-2] == ':':
                        data_alignment[col_ind] = Column.ALIGN_RIGHT
                        column.data = ' ' + '-' * (col_len - 3) + ': '
                    else:
                        column.data = ' ' + '-' * (col_len - 2) + ' '

                elif row.row_type == Row.ROW_DATA:
                    if (data_alignment[col_ind] is None):
                        data_alignment[col_ind] = self._auto_detect_column(row_ind, col_ind)
                    if data_alignment[col_ind] == Column.ALIGN_RIGHT:
                        column.data = column.data.rjust(col_len, ' ')
                    elif data_alignment[col_ind] == Column.ALIGN_LEFT:
                        column.data = column.data.ljust(col_len, ' ')
                    elif data_alignment[col_ind] == Column.ALIGN_CENTER:
                        column.data = column.data.center(col_len, ' ')


    def parse_row(self, line):
        line = line.strip()
        assert line[0] in self.syntax.hline_borders
        #remove first '|' character
        line = line[1:]
        #remove last '|' character
        if len(line) > 0 and line[-1] in self.syntax.hline_borders:
            line = line[:-1]
        if self.syntax.is_hline(line):
            cols = re.split(self.syntax.hline_border_pattern(), line)
        else:
            cols = line.split(self.syntax.vline)
        row = Row(self, cols)
        return row


    def format_to_lines(self):
        lines = self.text.splitlines()
        assert len(lines) > 0, "Table is empty"
        mo = re.search(r"[^\s]", lines[0])
        if mo:
            prefix = lines[0][:mo.start()]
        else:
            prefix = ""
        for line in lines:
            row = self.parse_row(line)
            self.add_row(row)
        self.pack()
        return [prefix + row.render() for row in self._rows]

    def format_to_text(self):
        return "\n".join(self.format_to_lines())


def format_to_text(text, syntax=simple_syntax):
    table = TextTable(text, syntax)
    return table.format_to_text()


def format_to_lines(text, syntax):
    table = TextTable(text, syntax)
    return table.format_to_lines()


if __name__ == '__main__':
    # each line begin from '|'

    raw_text = """      |-
                | header 1 | header 2 |header 3 | header 4 |
                | ------------ | ----------- | ---------- | ----- |
              |a  |   b   | c |1 |
              |1  |   2   | 3 |4 |
              |>|<|<|>|
              |=
              |:-|
              |-"""
    syntax = multi_markdown_syntax
    print "Table:\n", format_to_text(raw_text, syntax)
