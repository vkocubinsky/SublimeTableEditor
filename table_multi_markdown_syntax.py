# table_multi_markdown_syntax.py - Support MultiMarkdown table syntax

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
    from .table_base import *
except ValueError:
    from table_base import *


class MultiMarkdownTableSyntax(TableSyntax):

    def create_parser(self):
        return MultiMarkdownTableParser(self)


class MultiMarkdownAlignColumn(Column):
    PATTERN = r"^\s*([\:]?[\-]+[\:]?)\s*$"

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
        return int(math.ceil(self.total_min_len()/self.colspan))

    def total_min_len(self):
        # ' :-: ' or ' :-- ' or ' --: ' or ' --- '
        return 5 + self.colspan - 1


    def render(self):
        total_col_len = self.col_len + (self.colspan - 1 )+ sum([col.col_len for col in self.pseudo_columns])
        total_col_len = total_col_len - (self.colspan - 1)

        if self._align_follow == Column.ALIGN_CENTER:
            return ' :' + '-' * (total_col_len - 4) + ': '
        elif self._align_follow == Column.ALIGN_LEFT:
            return ' :' + '-' * (total_col_len - 4) + '- '
        elif self._align_follow == Column.ALIGN_RIGHT:
            return ' -' + '-' * (total_col_len - 4) + ': '
        else:
            return ' -' + '-' * (total_col_len - 4) + '- '

    def align_follow(self):
        return self._align_follow

    @staticmethod
    def match_cell(str_col):
        return re.match(MultiMarkdownAlignColumn.PATTERN, str_col)



class MultiMarkdownAlignRow(Row):

    def new_empty_column(self):
        return MultiMarkdownAlignColumn(self,'-')

    def create_column(self, text):
        return MultiMarkdownAlignColumn(self, text)


    def is_header_separator(self):
        return True

    def is_align(self):
        return True



class MultiMarkdownTableParser(BaseTableParser):


    def _is_multi_markdown_align_row(self, str_cols):
        for col in str_cols:
            if not MultiMarkdownAlignColumn.match_cell(col):
                return False
        return True

    def create_row(self, table, line):
        if self._is_multi_markdown_align_row(line.str_cols()):
            row = MultiMarkdownAlignRow(table)
        else:
            row = DataRow(table)
        return row

    def create_column(self, table, row, line_cell):
        column = BaseTableParser.create_column(self, table, row, line_cell)
        if len(line_cell.right_border_text) > 1:
            column.colspan = len(line_cell.right_border_text)
        return column
