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
except ValueError:
    from table_base import *


def simple_syntax(table_configuration=None):
    return create_syntax("Simple", table_configuration)

def emacs_org_mode_syntax(table_configuration=None):
    return create_syntax("EmacsOrgMode",table_configuration)

def pandoc_syntax(table_configuration=None):
    return create_syntax("Pandoc",table_configuration)

def re_structured_text_syntax(table_configuration=None):
    return create_syntax("reStructuredText",table_configuration)

def multi_markdown_syntax(table_configuration=None):
    return create_syntax("MultiMarkdown",table_configuration=table_configuration)

def textile_syntax(table_configuration=None):
    return create_syntax("Textile",table_configuration=table_configuration)


def create_syntax(syntax_name, table_configuration=None):
    modules = {
        "Simple" : "table_simple_syntax",
        "EmacsOrgMode" : "table_emacs_org_mode_syntax",
        "Pandoc" : "table_pandoc_syntax",
        "MultiMarkdown" : "table_multi_markdown_syntax",
        "reStructuredText" : "table_re_structured_text_syntax",
        "Textile" : "table_textile_syntax"
    }
    module_name = modules[syntax_name]
    if module_name is None:
        raise ValueError('Unsupported syntax',syntax_name)

    try:
        module = __import__("." + module_name)
    except ValueError:
        module = __import__(module_name)

    syntax = module.create_syntax(table_configuration)
    return syntax



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


    syntax = create_syntax("MultiMarkdown")
    syntax.intelligent_formatting = True
    t = syntax.table_parser.parse_text(text.strip())
    print("Table:'\n{0}\n'".format(t.render()))
    #print("visual to internal for 1", t.internal_to_visual_index(1,2))

