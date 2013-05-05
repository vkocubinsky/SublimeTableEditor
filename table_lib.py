# table_lib.py - pretty print text table.

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
    from .table_base import *
    from .table_multi_markdown_syntax import *
    from .table_textile_syntax import *
    from .table_simple_syntax import *
except ValueError:
    from table_base import *
    from table_multi_markdown_syntax import *
    from table_textile_syntax import *
    from table_simple_syntax import *






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

