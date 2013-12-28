# table_simple_syntax.py - Support Simple table syntax

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

import re


try:
    from . import table_base as tbase
    from . import table_border_syntax as tborder
except ValueError:
    import table_base as tbase
    import table_border_syntax as tborder


def create_syntax(table_configuration=None):
    return SimpleTableSyntax(table_configuration)


class SimpleTableSyntax(tbase.TableSyntax):

    def __init__(self, table_configuration):
        tbase.TableSyntax.__init__(self, "Simple", table_configuration)
        self.custom_column_alignment = self.table_configuration.custom_column_alignment

        self.table_parser = SimpleTableParser(self)
        self.table_driver = tborder.BorderTableDriver(self)


        self.hline_out_border = '|'
        self.hline_in_border = '|'
        if self.table_configuration.hline_out_border is not None:
            self.hline_out_border = self.table_configuration.hline_out_border
        if self.table_configuration.hline_in_border is not None:
            self.hline_in_border = self.table_configuration.hline_in_border



class CustomAlignColumn(tbase.Column):
    ALIGN_MAP = {'<': tbase.Column.ALIGN_LEFT,
                 '>': tbase.Column.ALIGN_RIGHT,
                 '#': tbase.Column.ALIGN_CENTER}

    PATTERN = r"^\s*((?:[\<]+)|(?:[\>]+)|(?:[\#]+))\s*$"

    def __init__(self, row, data):
        tbase.Column.__init__(self, row)
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


class CustomAlignRow(tbase.Row):

    def new_empty_column(self):
        return CustomAlignColumn(self, '#')

    def create_column(self, text):
        return CustomAlignColumn(self, text)

    def is_align(self):
        return True


class SimpleTableParser(tborder.BorderTableParser):

    def _is_custom_align_row(self, str_cols):
        if len(str_cols) == 0:
            return False
        for col in str_cols:
            if not CustomAlignColumn.match_cell(col):
                return False
        return True

    def create_row(self, table, line):
        if (self.syntax.custom_column_alignment and
                self._is_custom_align_row(line.str_cols())):
            row = CustomAlignRow(table)
        else:
            row = tborder.BorderTableParser.create_row(self, table, line)
        return row
