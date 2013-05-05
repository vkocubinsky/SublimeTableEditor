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

from __future__ import print_function
from __future__ import division

import math
import re
import csv

try:
    from .tablebase import *
    from .multi_markdown_syntax import *
except ValueError:
    from tablebase import *
    from multi_markdown_syntax import *



class TextileTableSyntax(TableSyntax):

    def create_parser(self):
        return TextileTableParser(self)

class SimpleTableSyntax(TableSyntax):

    def create_parser(self):
        return SimpleTableParser(self)


class EmacsOrgModeTableSyntax(TableSyntax):

    def create_parser(self):
        return TableParser(self)


class PandocTableSyntax(TableSyntax):

    def create_parser(self):
        return TableParser(self)


class ReStructuredTextTableSyntax(TableSyntax):

    def create_parser(self):
        return TableParser(self)


def simple_syntax():
    return SimpleTableSyntax(syntax = TableSyntax.SIMPLE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='|',
                       custom_column_alignment=True)


def emacs_org_mode_syntax():
    return EmacsOrgModeTableSyntax(syntax = TableSyntax.EMACS_ORG_MODE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='+')

def pandoc_syntax():
    return PandocTableSyntax(syntax = TableSyntax.PANDOC_SYNTAX,
                       hline_out_border='+',
                       hline_in_border='+')

def re_structured_text_syntax():
    return ReStructuredTextTableSyntax(syntax = TableSyntax.RE_STRUCTURED_TEXT_SYNTAX,
                       hline_out_border='+',
                       hline_in_border='+')

def multi_markdown_syntax():
    return MultiMarkdownTableSyntax(syntax = TableSyntax.MUTLI_MARKDOWN_SYTAX,
                       hline_out_border='|',
                       hline_in_border='|')


def textile_syntax():
    return TextileTableSyntax(syntax = TableSyntax.TEXTILE_SYNTAX,
                       hline_out_border='|',
                       hline_in_border='|')




class CustomAlignColumn(Column):
    ALIGN_MAP = {'<': Column.ALIGN_LEFT,
                 '>': Column.ALIGN_RIGHT,
                 '#': Column.ALIGN_CENTER}

    PATTERN = r"^\s*((?:[\<]+)|(?:[\>]+)|(?:[\#]+))\s*$"

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

    @staticmethod
    def match_cell(str_col):
        return re.match(CustomAlignColumn.PATTERN, str_col)





class TextileCellColumn(Column):
    PATTERN = (
        r"\s*("
        # Sequence of one or more table cell terms
        r"(?:"
            # Single character modifiers
            r"[_<>=~^:-]|"
            # Row and col spans
            r"(?:[/\\]\d+)|"
            # Styling and classes
            r"(?:\{.*?\})|(?:\(.*?\))"
        r")+"
        # Terminated by a period
        r"\.)\s+(.*)$")
    COLSPAN_PATTERN = r"\\(\d+)"
    ROWSPAN_PATTERN = r"/(\d+)"

    def __init__(self, row, data):
        Column.__init__(self, row)
        cell_mo = re.match(TextileCellColumn.PATTERN, data)
        self.attr = cell_mo.group(1)
        self.data = cell_mo.group(2).strip()

        colspan_mo = re.search(TextileCellColumn.COLSPAN_PATTERN, self.attr)
        if colspan_mo:
            self.colspan = int(colspan_mo.group(1))

        rowspan_mo = re.search(TextileCellColumn.ROWSPAN_PATTERN, self.attr)
        if rowspan_mo:
            self.rowspan = int(rowspan_mo.group(1))



    def min_len(self):
        return int(math.ceil(self.total_min_len()/self.colspan))

    def total_min_len(self):
        # '<. data '
        return len(self.attr) + len(self.data) + 2

    def render(self):
        # colspan -1 is count of '|'
        total_col_len = self.col_len + (self.colspan - 1 )+ sum([col.col_len for col in self.pseudo_columns])

        if '>' in self.attr and not '<>' in self.attr:
            return self.attr + ' ' + self.data.rjust(total_col_len - len(self.attr) - 2, ' ') + ' '
        elif '=' in self.attr or '_' in self.attr:
            return self.attr + ' ' + self.data.center(total_col_len - len(self.attr) - 2, ' ') + ' '
        else:
            return self.attr + ' ' + self.data.ljust(total_col_len - len(self.attr) - 2, ' ') + ' '

    @staticmethod
    def match_cell(str_col):
        return re.match(TextileCellColumn.PATTERN, str_col)






class TextileRow(Row):

    def new_empty_column(self):
        return DataColumn(self,'')

    def create_column(self, text):
        if TextileCellColumn.match_cell(text):
            return TextileCellColumn(self, text)
        else:
            return DataColumn(self, text)

    def is_data(self):
        return True



class CustomAlignRow(Row):

    def new_empty_column(self):
        return CustomAlignColumn(self,'#')

    def create_column(self, text):
        return CustomAlignColumn(self,text)

    def is_align(self):
        return True






class TableParser(BaseTableParser):


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


    def create_row(self, table, line):
        if self._is_single_row_separator(line.str_cols()):
            row = SeparatorRow(table, '-')
        elif self._is_double_row_separator(line.str_cols()):
            row = SeparatorRow(table, '=')
        else:
            row = DataRow(table)
        return row


class SimpleTableParser(TableParser):

    def _is_custom_align_row(self, str_cols):
        for col in str_cols:
            if not CustomAlignColumn.match_cell(col):
                return False
        return True

    def create_row(self, table, line):
        if (self.syntax.custom_column_alignment and
              self._is_custom_align_row(line.str_cols())):
            row = CustomAlignRow(table)
        else:
            row = TableParser.create_row(self, table, line)
        return row



class TextileTableParser(BaseTableParser):

    def create_row(self, table, line):
        return TextileRow(table)



def parse_csv(syntax, text):
    lines = []
    try:
        table = TextTable(syntax)
        vline = syntax.vline
        dialect = csv.Sniffer().sniff(text)
        table_reader = csv.reader(text.splitlines(), dialect)
        for cols in table_reader:
            row = DataRow(table)
            for col in cols:
                row.columns.append(DataColumn(row,col))
            table.add_row(row)
    except csv.Error:
        table = TextTable(syntax)
        for line in text.splitlines():
            row = Row(table, Row.ROW_DATA)
            row.columns.append(DataColumn(row,line))
            table.add_row(self, row)
    table.pack()
    return table







if __name__ == '__main__':
    # each line begin from '|'

    text = """   |                 |          Grouping           ||
 |   First Header  | Second Header | Third Header |
 |    ------------ | :-------: | --------: |
 |   Content       |          *Long Cell*        ||
 |   Content       |   **Cell**    |         Cell |
 |   New section   |     More      |         Data |
 |   And more      |            And more          |
 | :---: |||
"""


    syntax = multi_markdown_syntax()
    syntax.intelligent_formatting = True
    t = syntax.table_parser.parse_text(text.strip())
    print("Table:'\n{0}\n'".format(t.render()))
    #print("visual to internal for 1", t.internal_to_visual_index(1,2))

