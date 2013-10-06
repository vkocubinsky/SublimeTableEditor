# table_line_parser.py - Parse one line in a table.

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


class LineRegion:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __repr__(self):
        return "LineRegion(begin={0.begin}, end={0.end})".format(self)

    def __str__(self):
        return self.__repr__()


class LineCell:
    def __init__(self, line_text, left_border, right_border):
        self.cell_region = LineRegion(left_border.end, right_border.begin)
        self.left_border = left_border
        self.right_border = right_border
        self.text = line_text[self.cell_region.begin:self.cell_region.end]
        if self.right_border.begin == self.right_border.end:
            self.right_border_text = '|'
        else:
            self.right_border_text = line_text[self.right_border.begin:self.right_border.end]
        self.left_border_text = line_text[self.left_border.begin:self.left_border.end]


class Line:
    def __init__(self):
        self.cells = []
        self.prefix = ""

    def str_cols(self):
        return [cell.text for cell in self.cells]

    def field_num(self, pos):
        for ind, cell in enumerate(self.cells):
            if cell.right_border.end > pos:
                return ind
        else:
            return len(self.cells) - 1


class LineParser:
    def __init__(self, border_pattern):
        self.border_pattern = border_pattern

    def parse(self, line_text):

        line = Line()

        mo = re.search(r"[^\s]", line_text)
        if mo:
            line.prefix = line_text[:mo.start()]
        else:
            line.prefix = ""

        borders = []

        last_border_end = 0
        for m in re.finditer(self.border_pattern, line_text):
            borders.append(LineRegion(m.start(), m.end()))
            last_border_end = m.end()

        if last_border_end < len(line_text.rstrip()):
            borders.append(LineRegion(len(line_text), len(line_text)))

        left_border = None
        for right_border in borders:
            if left_border is None:
                left_border = right_border
            else:
                line.cells.append(LineCell(line_text, left_border, right_border))
                left_border = right_border
        return line


class LineParserPlus:

    def __init__(self, border_pattern):
        self.plus_line_parser = LineParser("(?:[+|])")

        self.plus_line_pattern = re.compile("^\s*[+]")
        self.single_hline_pattern = re.compile('^\s*[|+]\s*-[\s|+-]+$')
        self.double_hline_pattern = re.compile('^\s*[|+]\s*=[\s|+=]+$')

        self.data_line_parser = LineParser(border_pattern)

    def parse(self, line_text):
        if (self.single_hline_pattern.match(line_text) or
                self.double_hline_pattern.match(line_text) or
                self.plus_line_pattern.match(line_text)):
            return self.plus_line_parser.parse(line_text)
        else:
            return self.data_line_parser.parse(line_text)

