# table_border_syntax.py - Base classes for table with borders: Pandoc,
# Emacs Org mode, Simple, reStrucutredText

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
except ValueError:
    import table_base as tbase


class SeparatorRow(tbase.Row):

    def __init__(self, table, separator='-', size=0):
        tbase.Row.__init__(self, table)
        self.separator = separator
        for i in range(size):
            self.columns.append(SeparatorColumn(self, self.separator))

    def new_empty_column(self):
        return SeparatorColumn(self, self.separator)

    def create_column(self, text):
        return SeparatorColumn(self, self.separator)

    def is_header_separator(self):
        return True

    def is_separator(self):
        return True

    def render(self):
        r = self.syntax.hline_out_border
        for ind, column in enumerate(self.columns):
            if ind != 0:
                r += self.syntax.hline_in_border
            r += column.render()
        r += self.syntax.hline_out_border
        return r


class SeparatorColumn(tbase.Column):
    def __init__(self, row, separator):
        tbase.Column.__init__(self, row)
        self.separator = separator

    def min_len(self):
        # '---' or '==='
        return 3

    def render(self):
        return self.separator * self.col_len


class BorderTableDriver(tbase.TableDriver):

    def editor_insert_single_hline(self, table, table_pos):
        table.rows.insert(table_pos.row_num + 1, SeparatorRow(table, '-'))
        table.pack()
        return ("Single separator row inserted",
                tbase.TablePos(table_pos.row_num, table_pos.field_num))

    def editor_insert_double_hline(self, table, table_pos):
        table.rows.insert(table_pos.row_num + 1, SeparatorRow(table, '='))
        table.pack()
        return ("Double separator row inserted",
                tbase.TablePos(table_pos.row_num, table_pos.field_num))

    def editor_insert_hline_and_move(self, table, table_pos):
        table.rows.insert(table_pos.row_num + 1, SeparatorRow(table, '-'))
        table.pack()
        if table_pos.row_num + 2 < len(table):
            if table[table_pos.row_num + 2].is_separator():
                table.insert_empty_row(table_pos.row_num + 2)
        else:
            table.insert_empty_row(table_pos.row_num + 2)
        return("Single separator row inserted",
               tbase.TablePos(table_pos.row_num + 2, 0))


class BorderTableParser(tbase.BaseTableParser):

    def _is_single_row_separator(self, str_cols):
        if len(str_cols) == 0:
            return False
        for col in str_cols:
            if not re.match(r"^\s*[\-]+\s*$", col):
                return False
        return True

    def _is_double_row_separator(self, str_cols):
        if len(str_cols) == 0:
            return False
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
            row = self.create_data_row(table, line)
        return row

    def create_data_row(self, table, line):
        return tbase.DataRow(table)
