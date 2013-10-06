# table_textile_syntax.py - Support Textile table syntax

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


try:
    from . import table_base as tbase
    from .widechar_support import wlen, wcount
except ValueError:
    import table_base as tbase
    from widechar_support import wlen, wcount

def create_syntax(table_configuration=None):
    return TextileTableSyntax(table_configuration)


class TextileTableSyntax(tbase.TableSyntax):

    def __init__(self, table_configuration):
        tbase.TableSyntax.__init__(self, "Textile", table_configuration)

        self.table_parser = TextileTableParser(self)
        self.table_driver = tbase.TableDriver(self)


class TextileCellColumn(tbase.Column):
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
        tbase.Column.__init__(self, row)
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
        return len(self.attr) + wlen(self.data) + 2

    def render(self):
        # colspan -1 is count of '|'
        total_col_len = self.col_len + (self.colspan - 1) + sum([col.col_len for col in self.pseudo_columns])

        total_align_len = total_col_len - wcount(self.data)
        if '>' in self.attr and not '<>' in self.attr:
            return self.attr + ' ' + self.data.rjust(total_align_len - len(self.attr) - 2, ' ') + ' '
        elif '=' in self.attr or '_' in self.attr:
            return self.attr + ' ' + self.data.center(total_align_len - len(self.attr) - 2, ' ') + ' '
        else:
            return self.attr + ' ' + self.data.ljust(total_align_len - len(self.attr) - 2, ' ') + ' '

    @staticmethod
    def match_cell(str_col):
        return re.match(TextileCellColumn.PATTERN, str_col)


class TextileRow(tbase.Row):

    def new_empty_column(self):
        return tbase.DataColumn(self, '')

    def create_column(self, text):
        if TextileCellColumn.match_cell(text):
            return TextileCellColumn(self, text)
        else:
            return tbase.DataColumn(self, text)

    def is_data(self):
        return not self.is_header_separator()

    def is_header_separator(self):
        for column in self.columns:
            if not isinstance(column, TextileCellColumn):
                return False
            if '_' not in column.attr:
                return False
        return True


class TextileTableParser(tbase.BaseTableParser):

    def create_row(self, table, line):
        return TextileRow(table)
