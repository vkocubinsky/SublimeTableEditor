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
import csv

class TableSyntax:
    MUTLI_MARKDOWN_SYTAX = 'Multi Markdown'
    TEXTILE_SYNTAX = "Textile"
    EMACS_ORG_MODE_SYNTAX = "Emacs Org Mode"
    RE_STRUCTURED_TEXT_SYNTAX = "Re Structured Text Syntax"
    PANDOC_SYNTAX = "Pandoc Syntax"
    SIMPLE_SYNTAX = "Simple Syntax"

    def __init__(self, syntax,
                       hline_out_border='|',
                       hline_in_border='|',
                       custom_column_alignment=False):
        self.syntax = syntax
        self.vline = '|'
        self.hline_out_border = hline_out_border
        self.hline_in_border = hline_in_border
        #characters from all styles correct switch from one style to other
        self.hline_borders = ['+', '|']

        self.custom_column_alignment = custom_column_alignment
        self.keep_space_left = False
        self.align_number_right = True
        self.detect_header = True

    def multi_markdown_syntax(self):
        return self.syntax == TableSyntax.MUTLI_MARKDOWN_SYTAX

    def textile_syntax(self):
        return self.syntax == TableSyntax.TEXTILE_SYNTAX

    def emacs_org_mode_syntax(self):
        return self.syntax == TableSyntax.EMACS_ORG_MODE_SYNTAX

    def re_structured_text_syntax(self):
        return self.syntax == TableSyntax.RE_STRUCTURED_TEXT_SYNTAX

    def pandoc_syntax(self):
        return self.syntax == TableSyntax.PANDOC_SYNTAX

    def simple_syntax(self):
        return self.syntax == TableSyntax.SIMPLE_SYNTAX


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



def simple_syntax():
    return TableSyntax(syntax = TableSyntax.SIMPLE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='|',
                       custom_column_alignment=True)


def emacs_org_mode_syntax():
    return TableSyntax(syntax = TableSyntax.EMACS_ORG_MODE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='+')

def pandoc_syntax():
    return TableSyntax(syntax = TableSyntax.PANDOC_SYNTAX,
                       hline_out_border='+',
                       hline_in_border='+')

def re_structured_text_syntax():
    return TableSyntax(syntax = TableSyntax.RE_STRUCTURED_TEXT_SYNTAX,
                       hline_out_border='+',
                       hline_in_border='+')

def multi_markdown_syntax():
    return TableSyntax(syntax = TableSyntax.MUTLI_MARKDOWN_SYTAX,
                       hline_out_border='|',
                       hline_in_border='|')


def textile_syntax():
    return TableSyntax(syntax = TableSyntax.TEXTILE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='|')

class Column(object):
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'
    ALIGN_CENTER = 'center'

    def __init__(self, row):
        self.row = row
        self.table = row.table
        self.syntax = row.table.syntax
        self.col_len = 0
        self.align = None
        self.header = None

    def min_len(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def align_follow(self):
        return None

class DataColumn(Column):

    def __init__(self, row, data):
        Column.__init__(self, row)
        self.data = data
        self.left_space = ' '
        self.right_space = ' '

    def _norm(self):
        if self.syntax.keep_space_left:
            if self.header:
                norm = self.data.strip()
            else:
                norm = self.data.rstrip()
                if norm[:1] == ' ':
                     norm = norm[1:]
        else:
            norm = self.data.strip()
        return norm


    def min_len(self):
        # min of '   ' or ' xxxx '
        space_len = len(self.left_space) + len(self.right_space)
        return max(space_len + 1, len(self._norm()) + space_len)


    def render(self):
        norm = self._norm()
        space_len = len(self.left_space) + len(self.right_space)

        if self.header and self.syntax.detect_header:
            align_value =  norm.center(self.col_len - space_len, ' ')
        elif self.align == Column.ALIGN_RIGHT:
            align_value = norm.rjust(self.col_len - space_len, ' ')
        elif self.align == Column.ALIGN_CENTER:
            align_value = norm.center(self.col_len - space_len, ' ')
        else:
            align_value = norm.ljust(self.col_len - space_len, ' ')
        return self.left_space + align_value + self.right_space


class SeparatorColumn(Column):
    def __init__(self, row, separator):
        Column.__init__(self, row)
        self.separator = separator


    def min_len(self):
        # '---' or '==='
        return 3

    def render(self):
        return self.separator * self.col_len


class CustomAlignColumn(Column):
    ALIGN_MAP = {'<': Column.ALIGN_LEFT,
                 '>': Column.ALIGN_RIGHT,
                 '#': Column.ALIGN_CENTER}

    def __init__(self, row, data):
        Column.__init__(self, row)
        self.align_char = re.search(r"[\<]|[\>]|[\#]", data).group(0)

    def align_follow(self):
        return CustomAlignColumn.ALIGN_MAP[self.align_char]

    def min_len(self):
        # ' < ' or ' > ' or ' # '
        return 3


    def render(self):
        return ' ' + self.align_char * (self.col_len - 2) + ' '


class MultiMarkdownAlignColumn(Column):
    def __init__(self, row, data):
        Column.__init__(self, row)
        col = data.strip()
        if col.count(':') == 2:
            self._align_follow = Column.ALIGN_CENTER
        elif col[0] == ':':
            self._align_follow = Column.ALIGN_LEFT
        elif col[-1] == ':':
            self._align_follow = Column.ALIGN_RIGHT
        else:
            self._align_follow = None

    def min_len(self):
        # ' :-: ' or ' :-- ' or ' --: ' or ' --- '
        return 5

    def render(self):
        if self._align_follow == Column.ALIGN_CENTER:
            return ' :' + '-' * (self.col_len - 4) + ': '
        elif self._align_follow == Column.ALIGN_LEFT:
            return ' :' + '-' * (self.col_len - 4) + '- '
        elif self._align_follow == Column.ALIGN_RIGHT:
            return ' -' + '-' * (self.col_len - 4) + ': '
        else:
            return ' -' + '-' * (self.col_len - 4) + '- '

    def align_follow(self):
        return self._align_follow

class TextileCellColumn(Column):
    PATTERN = r"\s*((?:\_\.)|(?:\<\.)|(?:\>\.)|(?:\=\.)|(?:\<\>\.)|(?:\^\.)|(?:\~\.))(.*)$"

    def __init__(self, row, data):
        Column.__init__(self, row)
        mo = re.match(TextileCellColumn.PATTERN, data)
        self.attr = mo.group(1)
        self.data = mo.group(2).strip()


    def min_len(self):
        # '<. data '
        return len(self.attr) + len(self.data) + 2

    def render(self):
        if self.attr == '>.':
            return self.attr + ' ' + self.data.rjust(self.col_len - len(self.attr) - 2, ' ') + ' '
        elif self.attr in ['_.','=.']:
            return self.attr + ' ' + self.data.center(self.col_len - len(self.attr) - 2, ' ') + ' '
        else:
            return self.attr + ' ' + self.data.ljust(self.col_len - len(self.attr) - 2, ' ') + ' '

    @staticmethod
    def is_textile_cell(str_col):
        return re.match(TextileCellColumn.PATTERN, str_col)

class Row:

    def __init__(self, table):
        self.table = table
        self.columns = []

    def __getitem__(self, index):
        return self.columns[index]

    def __len__(self):
        return len(self.columns)

    def is_header_separator(self):
        return False

    def is_separator(self):
        return False

    def is_data(self):
        return False

    def is_align(self):
        return False

    @property
    def str_cols(self):
        return [column.render() for column in self.columns]

    def new_empty_column(self):
        raise NotImplementedError

    def append(column):
        self.columns.append(column)

    def render(self):
        syntax = self.table.syntax
        if self.is_separator():
            return (syntax.hline_out_border
                + syntax.hline_in_border.join(self.str_cols)
                + syntax.hline_out_border)
        else:
            vline = syntax.vline
            return vline + vline.join(self.str_cols) + vline


class SeparatorRow(Row):

    def __init__(self, table, separator = '-', size = 0):
        Row.__init__(self, table)
        self.separator = separator
        for i in range(size):
            self.columns.append(SeparatorColumn(self, self.separator))

    def new_empty_column(self):
        return SeparatorColumn(self,self.separator)

    def is_header_separator(self):
        return True

    def is_separator(self):
        return True


class DataRow(Row):

    def new_empty_column(self):
        return DataColumn(self,'')

    def is_data(self):
        return True

class CustomAlignRow(Row):

    def new_empty_column(self):
        return CustomAlignColumn(self,'#')

    def is_align(self):
        return True


class MultiMarkdownAlignRow(Row):

    def new_empty_column(self):
        return MultiMarkdownAlignColumn(self.row,'-')

    def is_header_separator(self):
        return True

    def is_align(self):
        return True


class TextTable:


    def __init__(self, syntax):
        self.syntax = syntax
        self.prefix = ""
        self._rows = []
        self.column_count = 0
        self.pack()


    def add_row(self, row):
        self._rows.append(row)


    @property
    def row_count(self):
        return len(self._rows)

    def empty(self):
        return self.column_count == 0

    def __getitem__(self, index):
        return self._rows[index]

    def pack(self):
        if len(self._rows) == 0:
            self.column_count = 0
            return

        self.column_count = max([len(row) for row in self._rows])

        if self.column_count == 0:
            self._rows = []
            return

        #adjust/extend column count
        for row in self._rows:
            diff_count = self.column_count - len(row.columns)
            for i in range(diff_count):
                row.columns.append(row.new_empty_column())

        if self.syntax.textile_syntax():
            textile_sizes = [0] * self.column_count
            for row in self._rows:
                for col_ind, column in enumerate(row.columns):
                    if isinstance(column, TextileCellColumn):
                        textile_sizes[col_ind] = max(textile_sizes[col_ind], len(column.attr))
            for row in self._rows:
                for left_size, column in zip(textile_sizes, row.columns):
                    if isinstance(column, DataColumn):
                        column.left_space = ' ' * (left_size + 1)

        #calculate column lens
        col_lens = [0] * self.column_count
        for row in self._rows:
            new_col_lens = [column.min_len() for column in row.columns]
            col_lens = [max(x, y) for x, y in zip(col_lens, new_col_lens)]

        #set column len
        for row in self._rows:
            for column, col_len in zip(row.columns, col_lens):
                column.col_len = col_len

        #header
        header_separator_index = -1
        first_data_index = -1
        if self.syntax.detect_header:
            for row_ind,row in enumerate(self._rows):
                if first_data_index == -1 and row.is_data():
                    first_data_index = row_ind
                if (first_data_index != -1 and header_separator_index == -1 and
                    row.is_header_separator()):
                    header_separator_index = row_ind
                    for header_index in range(first_data_index, header_separator_index):
                        if self._rows[header_index].is_data():
                            for column in self._rows[header_index].columns:
                                column.header = True


        #set column alignment
        data_alignment = [None] * len(col_lens)
        for row_ind,row in enumerate(self._rows):
            if row_ind < header_separator_index:
                if row.is_align():
                    for col_ind,column in enumerate(row.columns):
                        data_alignment[col_ind] = column.align_follow()
                continue
            elif row.is_align():
                for col_ind,column in enumerate(row.columns):
                    data_alignment[col_ind] = column.align_follow()
            elif row.is_data():
                for col_ind,column in enumerate(row.columns):
                    if data_alignment[col_ind] is None:
                        if self.syntax.align_number_right and self._is_number_column(row_ind, col_ind):
                            data_alignment[col_ind] = Column.ALIGN_RIGHT
                        else:
                            data_alignment[col_ind] = Column.ALIGN_LEFT
                    column.align = data_alignment[col_ind]


    def delete_column(self, i):
        assert i < self.column_count
        for row in self._rows:
            del row.columns[i]
        self.pack()


    def swap_columns(self, i, j):
        assert i < self.column_count and j < self.column_count
        for row in self._rows:
            row.columns[i], row.columns[j] = row.columns[j], row.columns[i]

    def insert_empty_column(self, i):
        assert i >= 0
        for row in self._rows:
            row.columns.insert(i, row.new_empty_column())
        self.pack()


    def insert_empty_row(self, i):
        assert i >= 0
        self._rows.insert(i, DataRow(self))
        self.pack()

    def insert_single_separator_row(self, i):
        assert i >= 0
        self._rows.insert(i, SeparatorRow(self, '-'))
        self.pack()

    def insert_double_separator_row(self, i):
        assert i >= 0
        self._rows.insert(i, SeparatorRow(self, '='))
        self.pack()


    def swap_rows(self, i, j):
        assert 0 <= i < len(self._rows) and 0 <= j < len(self._rows)
        self._rows[i], self._rows[j] = self._rows[j], self._rows[i]
        self.pack()

    def delete_row(self, i ):
        assert 0 <= i < len(self._rows)
        del self._rows[i]
        self.pack()

    def get_cursor(self, row_ind, col_ind):
        #
        # '   |  1 |  2  |  3_| 4 |'
        assert col_ind < self.column_count
        base_len = (len(self.prefix) +
                   sum([column.col_len for column, ind
                                in zip(self[row_ind].columns, range(col_ind))]) +
                   col_ind + 1 # count of '|'
                   )
        text = self[row_ind][col_ind].render()
        match = re.search(r"([^\s])\s*$",text)
        if match:
            col_pos = match.end(1)
        else:
            col_pos = 1
        #print base_len, col_pos
        return base_len + col_pos




    def _is_number_column(self, start_row_ind, col_ind):
        assert self._rows[start_row_ind].is_data()
        for row in self._rows[start_row_ind:]:
            if (row.is_data()
                and len(row.columns[col_ind].data.strip()) > 0
                and not re.match("^\s*[0-9]*[.,]?[0-9]+\s*$", row.columns[col_ind].data)):
                return False
        return True

    def render_lines(self):
        return [self.prefix + row.render() for row in self._rows]

    def render(self):
        return "\n".join(self.render_lines())


class TableParser:

    def __init__(self, syntax):
        self.syntax = syntax

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


    def _parse_row(self, table, str_cols):
        if self._is_single_row_separator(str_cols):
            row = SeparatorRow(table, '-', len(str_cols))
        elif self._is_double_row_separator(str_cols):
            row = SeparatorRow(table, '=', len(str_cols))
        elif (self.syntax.custom_column_alignment and
              self._is_custom_align_row(str_cols)):
            row = CustomAlignRow(table)
            row.columns = [CustomAlignColumn(row,col) for col in str_cols]
        elif (self.syntax.multi_markdown_syntax()
              and self._is_multi_markdown_align_row(str_cols)):
            row = MultiMarkdownAlignRow(table)
            row.columns = [MultiMarkdownAlignColumn(row,col) for col in str_cols]
        else:
            row = DataRow(table)
            for col in str_cols:
                if (self.syntax.textile_syntax() and
                   TextileCellColumn.is_textile_cell(col)):
                    column = TextileCellColumn(row, col)
                else:
                    column = DataColumn(row,col)
                row.columns.append(column)
        return row


    def _split_row(self, table, line):
        line = line.strip()
        #remove first '|' character
        if line[:1] in self.syntax.hline_borders:
            line = line[1:]
        #remove last '|' character
        if line[-1:] in self.syntax.hline_borders:
            line = line[:-1]
        if self.syntax.is_hline(line):
            cols = re.split(self.syntax.hline_border_pattern(), line)
        else:
            cols = line.split(self.syntax.vline)
        return cols

    def is_table_row(self, row):
        return re.match(r"^\s*" + self.syntax.hline_border_pattern(),
                        row) is not None


    def parse_text(self, text):
        table = TextTable(self.syntax)
        mo = re.search(r"[^\s]", text)
        if mo:
            table.prefix = text[:mo.start()]
        else:
            table.prefix = ""
        lines = text.strip().splitlines()
        for line in lines:
            cols = self._split_row(table, line)
            row = self._parse_row(table, cols)
            table.add_row(row)
        table.pack()
        return table

    def parse_csv(self, text):
        lines = []
        try:
            table = TextTable(syntax)
            vline = self.syntax.vline
            dialect = csv.Sniffer().sniff(text)
            table_reader = csv.reader(text.splitlines(), dialect)
            for cols in table_reader:
                row = Row(table, Row.ROW_DATA)
                row.columns = [DataColumn(row,col) for col in cols]
                table.add_row(row)
        except csv.Error:
            table = TextTable(syntax)
            for line in text.splitlines():
                row = Row(table, Row.ROW_DATA)
                row.columns.append(DataColumn(row,line))
                table.add_row(self, row)
        table.pack()
        return table

def parse_table(syntax, text):
    parser = TableParser(syntax)
    table = parser.parse_text(text)
    return table


if __name__ == '__main__':
    # each line begin from '|'
    text = """\
|  a  |  b  |   c   |
|-----|-----|-------|
| 1   | 2   | 3     |
| one | two | three |
"""

    csv_text = """\
1,2,3
a,b,c
"""
    syntax = pandoc_syntax()
    p = TableParser(syntax)
    t = p.parse_text(text)
#    t = p.parse_csv(csv_text)
    print "Table:'\n{0}\n'".format(t.render())
    print t.get_cursor(0,1)
