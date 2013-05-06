# re_structured_text_syntax.py - Support reStructuredText table syntax

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


def create_syntax(table_configuration=None):
    return ReStructuredTextTableSyntax(table_configuration)


class ReStructuredTextTableSyntax(TableSyntax):

    def __init__(self, table_configuration):
        TableSyntax.__init__(self, table_configuration)
        self.table_parser = ReStructuredTextParser(self)
        self.hline_out_border='+'
        self.hline_in_border='+'
        self.keep_space_left = self.table_configuration.keep_space_left or False


class ReStructuredTextRow(Row):

    def new_empty_column(self):
        return ReStructuredTextColumn(self,'')

    def create_column(self, text):
        return ReStructuredTextColumn(self, text)

    def is_data(self):
        return True


class ReStructuredTextColumn(DataColumn):

    def norm(self):
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


class ReStructuredTextParser(TableParser):

    def create_data_row(self, table, line):
        return ReStructuredTextRow(table)


