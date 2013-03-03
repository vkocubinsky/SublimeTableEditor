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

    def new_empty_column(self):
        raise NotImplementedError


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

    def new_empty_column(self):
        return DataColumn(self.row,'')

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

    def new_empty_column(self):
        return SeparatorColumn(self.row,self.separator)

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

    def new_empty_column(self):
        return CustomAlignColumn(self.row,'#')

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

    def new_empty_column(self):
        return MultiMarkdownAlignColumn(self.row,'-')

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

    def new_empty_column(self):
        return DataColumn(self.row,"")

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

class TextileHeaderColumn(TextileCellColumn):
    def new_empty_column(self):
        return TextileHeaderColumn(self.row,"_. ")




class Row:
    ROW_DATA = 'd'
    ROW_SINGLE_SEPARATOR = '-'
    ROW_DOUBLE_SEPARATOR = '='
    ROW_CUSTOM_ALIGN = '<>#'
    ROW_MULTI_MARKDOWN_ALIGN = ':-:'
    ROW_TEXTILE_HEADER_syntax = "._"


    def __init__(self, table, str_cols):
        self.table = table
        self._row_type = None

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
        elif (self.table.syntax.multi_markdown_syntax()
              and self._is_multi_markdown_align_row(str_cols)):
            self._row_type = Row.ROW_MULTI_MARKDOWN_ALIGN
            self.columns = [MultiMarkdownAlignColumn(self,col) for col in str_cols]
        elif (self.table.syntax.textile_syntax() and
              self._is_textile_header_syntax(str_cols)):
              self._row_type = Row.ROW_TEXTILE_HEADER_syntax
              self.columns = [TextileHeaderColumn(self,col) for col in str_cols]
        else:
            self._row_type = Row.ROW_DATA
            self.columns = []
            for col in str_cols:
                if (self.table.syntax.textile_syntax() and
                   TextileCellColumn.is_textile_cell(col)):
                    column = TextileCellColumn(self, col)
                else:
                    column = DataColumn(self,col)
                self.columns.append(column)


    @property
    def row_type(self):
        return self._row_type

    def is_header_separator(self):
        return self._row_type in (Row.ROW_SINGLE_SEPARATOR,
                                  Row.ROW_DOUBLE_SEPARATOR,
                                  Row.ROW_MULTI_MARKDOWN_ALIGN)


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

    def _is_textile_header_syntax(self, str_cols):
        for col in str_cols:
            if not re.match(r"^\s*\_\..*$", col):
                return False
        return True



    @property
    def str_cols(self):
        return [column.render() for column in self.columns]

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


    def add_row(self, row):
        self._rows.append(row)

    def pack(self):
        column_count = max([len(row.columns) for row in self._rows])
        #adjust/extend column count
        for row in self._rows:
            column = row.columns[0]
            diff_count = column_count - len(row.columns)
            for i in range(diff_count):
                row.columns.append(column.new_empty_column())

        if self.syntax.textile_syntax():
            textile_sizes = [0] * column_count
            for row in self._rows:
                for col_ind, column in enumerate(row.columns):
                    if isinstance(column, TextileCellColumn):
                        textile_sizes[col_ind] = max(textile_sizes[col_ind], len(column.attr))
            for row in self._rows:
                for left_size, column in zip(textile_sizes, row.columns):
                    if isinstance(column, DataColumn):
                        column.left_space = ' ' * (left_size + 1)

        #calculate column lens
        col_lens = [0] * column_count
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
                if first_data_index == -1 and row.row_type == Row.ROW_DATA:
                    first_data_index = row_ind
                if (first_data_index != -1 and header_separator_index == -1 and
                    row.is_header_separator()):
                    header_separator_index = row_ind
                    for header_index in range(first_data_index, header_separator_index):
                        if self._rows[header_index].row_type == Row.ROW_DATA:
                            for column in self._rows[header_index].columns:
                                column.header = True


        #set column alignment
        data_alignment = [None] * len(col_lens)
        for row_ind,row in enumerate(self._rows):
            if row_ind < header_separator_index:
                if row.row_type in (Row.ROW_CUSTOM_ALIGN, Row.ROW_MULTI_MARKDOWN_ALIGN):
                    for col_ind,column in enumerate(row.columns):
                        data_alignment[col_ind] = column.align_follow()
                continue
            elif row.row_type in (Row.ROW_CUSTOM_ALIGN, Row.ROW_MULTI_MARKDOWN_ALIGN):
                for col_ind,column in enumerate(row.columns):
                    data_alignment[col_ind] = column.align_follow()
            elif row.row_type == Row.ROW_DATA:
                for col_ind,column in enumerate(row.columns):
                    if data_alignment[col_ind] is None:
                        if self.syntax.align_number_right and self._is_number_column(row_ind, col_ind):
                            data_alignment[col_ind] = Column.ALIGN_RIGHT
                        else:
                            data_alignment[col_ind] = Column.ALIGN_LEFT
                    column.align = data_alignment[col_ind]



    def _is_number_column(self, start_row_ind, col_ind):
        assert self._rows[start_row_ind].row_type == Row.ROW_DATA
        for row in self._rows[start_row_ind:]:
            if (row.row_type == Row.ROW_DATA
                and len(row.columns[col_ind].data.strip()) > 0
                and not re.match("^\s*[0-9]*[.,]?[0-9]+\s*$", row.columns[col_ind].data)):
                return False
        return True


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
    raw_text = """\
    |_. attribute list |
|<. align left |
| cell|
|>. align right|
|=. center |
|<>. justify |
|^. valign top |
|~. bottom |"""
    syntax = textile_syntax()
    syntax.detect_header = False
    print "Table:\n", format_to_text(raw_text, syntax)
