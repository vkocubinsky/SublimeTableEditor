# tablebase.py - Key classes and methods for pretty print text table.

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
        if syntax == TableSyntax.TEXTILE_SYNTAX:
            self.intelligent_formatting = True
        else:
            self.intelligent_formatting = False

        self.table_parser = self.create_parser()


    def create_parser(self):
        raise NotImplementedError

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
        self.colspan = 1
        self.rowspan = 1
        self.pseudo_columns = []
        self.left_border_text = self.syntax.vline
        self.right_border_text = self.syntax.vline


    def min_len(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def align_follow(self):
        return None

    def pseudo(self):
        return False


class PseudoColumn(Column):

    def __init__(self, row, master_column):
        Column.__init__(self, row)
        self.master_column = master_column
        self.data = ''

    def render(self):
        return ''

    def min_len(self):
        return self.master_column.min_len()

    def pseudo(self):
        return True

class Row:

    def __init__(self, table):
        self.table = table
        self.syntax = table.syntax
        self.columns = []

    def __getitem__(self, index):
        return self.columns[index]

    def __len__(self):
        return len(self.columns)

    def is_header_separator(self):
        return False

    def is_separator(self):
        return False

    def is_data(self):
        return False

    def is_align(self):
        return False

    def append(self, column):
        self.columns.append(column)
        for i in range(0, column.colspan - 1):
            psedo_column = PseudoColumn(self, column)
            column.pseudo_columns.append(psedo_column)
            self.columns.append(psedo_column)


    def new_empty_column(self):
        raise NotImplementedError

    def create_column(self, text):
        raise NotImplementedError


    def render(self):

        def str_cols():
            return [column.render() for column in self.columns if not column.pseudo()]

        syntax = self.table.syntax
        if self.is_separator():
            return (syntax.hline_out_border
                + syntax.hline_in_border.join(str_cols())
                + syntax.hline_out_border)
        else:
            r = ""
            for ind, column in enumerate(self.columns):
                if column.pseudo():
                    continue
                if ind == 0:
                    r += column.left_border_text
                r += column.render()
                r += column.right_border_text
            return r


class SeparatorRow(Row):

    def __init__(self, table, separator = '-', size = 0):
        Row.__init__(self, table)
        self.separator = separator
        for i in range(size):
            self.columns.append(SeparatorColumn(self, self.separator))

    def new_empty_column(self):
        return SeparatorColumn(self,self.separator)

    def create_column(self, text):
        return SeparatorColumn(self,self.separator)

    def is_header_separator(self):
        return True

    def is_separator(self):
        return True


class DataRow(Row):

    def new_empty_column(self):
        return DataColumn(self,'')

    def create_column(self, text):
        return DataColumn(self, text)

    def is_data(self):
        return True


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
        return int(math.ceil(self.total_min_len()/self.colspan))


    def total_min_len(self):
        # min of '   ' or ' xxxx '
        space_len = len(self.left_space) + len(self.right_space)
        total_min_len = max(space_len + 1, len(self._norm()) + space_len)
        if self.syntax.multi_markdown_syntax():
            total_min_len += self.colspan - 1
        return total_min_len


    def render(self):
        # colspan -1 is count of '|'
        total_col_len = self.col_len + (self.colspan - 1 )+ sum([col.col_len for col in self.pseudo_columns])

        if self.syntax.multi_markdown_syntax():
            total_col_len = total_col_len - (self.colspan - 1)


        norm = self._norm()
        space_len = len(self.left_space) + len(self.right_space)

        if self.header and self.syntax.detect_header:
            align_value =  norm.center(total_col_len - space_len, ' ')
        elif self.align == Column.ALIGN_RIGHT:
            align_value = norm.rjust(total_col_len - space_len, ' ')
        elif self.align == Column.ALIGN_CENTER:
            align_value = norm.center(total_col_len - space_len, ' ')
        else:
            align_value = norm.ljust(total_col_len - space_len, ' ')
        return self.left_space + align_value + self.right_space


class SeparatorColumn(Column):
    def __init__(self, row, separator):
        Column.__init__(self, row)
        self.separator = separator


    def min_len(self):
        # '---' or '==='
        return 3

    def render(self):
        return self.separator * self.col_len



class TextTable:


    def __init__(self, syntax):
        self.syntax = syntax
        self.prefix = ""
        self._rows = []
        self.pack()


    def add_row(self, row):
        self._rows.append(row)


    def __len__(self):
        return len(self._rows)

    def empty(self):
        return len(self._rows) == 0

    def __getitem__(self, index):
        return self._rows[index]

    def _max_column_count(self):
        return max([len(row) for row in self._rows])

    def _rstrip(self):
        if len(self._rows) <= 1:
            return
        max_column_count = self._max_column_count()
        long_lines_count = 0
        long_line_ind = 0
        for row_ind, row in enumerate(self._rows):
            if len(row) == max_column_count:
                long_lines_count += 1
                long_line_ind = row_ind

        if long_lines_count == 1:
            row = self._rows[long_line_ind]
            overspans = sum([column.colspan - 1 for column in row.columns])
            if row.is_data() and overspans > 0:
                shift = 0
                for shift, column in enumerate(row[::-1]):
                    if column.pseudo() or len(column.data.strip()) > 0:
                        break
                if shift > 0:
                    if len(self._rows) == 2:
                        if shift != overspans:
                            return

                    row.columns = row.columns[:-shift]


    def pack(self):
        if len(self._rows) == 0:
            return

        column_count = self._max_column_count()

        if column_count == 0:
            self._rows = []
            return

        #intelligent formatting
        if self.syntax.intelligent_formatting:
            self._rstrip()
            column_count = self._max_column_count()



        #adjust/extend column count

        rowspans = [0] * column_count
        for row in self._rows:
            overcols = sum([rowspan for rowspan in rowspans if rowspan > 0])

            diff_count = column_count - len(row) - overcols
            for i in range(diff_count):
                row.columns.append(row.new_empty_column())
            if len(row) == 0:
                row.columns.append(row.new_empty_column())

            #prepare rowspans for next row
            for col_ind, rowspan in enumerate(rowspans):
                if rowspan > 0:
                    rowspans[col_ind] = rowspans[col_ind] - 1

            for col_ind, column in enumerate(row.columns):
                rowspans[col_ind] = rowspans[col_ind] + column.rowspan - 1

        #calculate column lens
        col_lens = [0] * column_count
        for row in self._rows:
            for col_ind,column in enumerate(row.columns):
                col_lens[col_ind] = max(col_lens[col_ind], column.min_len())

        #set column len
        for row in self._rows:
            for column, col_len in zip(row.columns, col_lens):
                column.col_len = col_len

        #header
        header_separator_index = -1
        first_data_index = -1
        if self.syntax.detect_header:
            for row_ind,row in enumerate(self._rows):
                if first_data_index == -1 and row.is_data():
                    first_data_index = row_ind
                if (first_data_index != -1 and header_separator_index == -1 and
                    row.is_header_separator()):
                    header_separator_index = row_ind
                    for header_index in range(first_data_index, header_separator_index):
                        if self._rows[header_index].is_data():
                            for column in self._rows[header_index].columns:
                                column.header = True


        #set column alignment
        data_alignment = [None] * len(col_lens)
        for row_ind,row in enumerate(self._rows):
            if row_ind < header_separator_index:
                if row.is_align():
                    for col_ind,column in enumerate(row.columns):
                        data_alignment[col_ind] = column.align_follow()
                continue
            elif row.is_align():
                for col_ind,column in enumerate(row.columns):
                    data_alignment[col_ind] = column.align_follow()
            elif row.is_data():
                for col_ind,column in enumerate(row.columns):
                    if data_alignment[col_ind] is None:
                        if self.syntax.align_number_right and self._is_number_column(row_ind, col_ind):
                            data_alignment[col_ind] = Column.ALIGN_RIGHT
                        else:
                            data_alignment[col_ind] = Column.ALIGN_LEFT
                    column.align = data_alignment[col_ind]


    def delete_column(self, i):
        assert self.is_col_colspan(i) == False

        for row in self._rows:
            if i < len(row):
                del row.columns[i]
        self.pack()


    def swap_columns(self, i, j):
        assert self.is_col_colspan(i) == False
        assert self.is_col_colspan(j) == False

        for row in self._rows:
            if i < len(row) and j < len(row):
                row.columns[i], row.columns[j] = row.columns[j], row.columns[i]
        self.pack()

    def insert_empty_column(self, i):
        assert i >= 0
        assert self.is_col_colspan(i) == False

        for row in self._rows:
            row.columns.insert(i, row.new_empty_column())
        self.pack()


    def insert_empty_row(self, i):
        assert i >= 0

        self._rows.insert(i, DataRow(self))
        self.pack()

    def insert_single_separator_row(self, i):
        assert i >= 0

        self._rows.insert(i, SeparatorRow(self, '-'))
        self.pack()

    def insert_double_separator_row(self, i):
        assert i >= 0

        self._rows.insert(i, SeparatorRow(self, '='))
        self.pack()


    def swap_rows(self, i, j):
        assert 0 <= i < len(self._rows) and 0 <= j < len(self._rows)

        self._rows[i], self._rows[j] = self._rows[j], self._rows[i]
        self.pack()

    def delete_row(self, i ):
        assert 0 <= i < len(self._rows)

        del self._rows[i]
        self.pack()

    def visual_column_count(self, row):
        return sum([1 for col in self[row].columns if not col.pseudo()])

    def is_col_colspan(self, col):
        for row in self._rows:
            if col < len(row):
                if row[col].pseudo() or row[col].colspan > 1:
                    return True
        return False

    def is_row_colspan(self, row):
        for column in self[row].columns:
            if column.pseudo() or column.colspan > 1:
                    return True
        return False

    def internal_to_visual_index(self, row, internal_index):
        visual_ind = internal_index
        for col in range(internal_index + 1):
            if self[row][col].pseudo():
                visual_ind -= 1
        return visual_ind

    def visual_to_internal_index(self, row, visual_index):
        count_visual = 0
        internal_ind = 0
        for col in range(len(self[row])):
            if not self[row][col].pseudo():
                count_visual += 1
                internal_ind = col
            if count_visual == visual_index + 1:
                break
        else:
            print("WARNING: Visual Index Not found")
        return internal_ind


    def get_cursor(self, row_ind, visual_col_ind):
        #
        # '   |  1 |  2  |  3_| 4 |'
        col_ind = self.visual_to_internal_index(row_ind, visual_col_ind)
        base_len = (len(self.prefix) +
                   sum([column.col_len for column, ind
                                in zip(self[row_ind].columns, range(col_ind))]) +
                   col_ind + 1 # count of '|'
                   )
        text = self[row_ind][col_ind].render()
        match = re.search(r"([^\s])\s*$",text)
        if match:
            col_pos = match.end(1)
        else:
            col_pos = 1
        return base_len + col_pos




    def _is_number_column(self, start_row_ind, col_ind):
        assert self._rows[start_row_ind].is_data()
        for row in self._rows[start_row_ind:]:
            if (row.is_data()
                and col_ind < len(row.columns)
                and len(row.columns[col_ind].data.strip()) > 0
                and not re.match("^\s*[0-9]*[.,]?[0-9]+\s*$", row.columns[col_ind].data)):
                return False
        return True

    def render_lines(self):
        return [self.prefix + row.render() for row in self._rows]

    def render(self):
        return "\n".join(self.render_lines())




class BaseTableParser:

    def __init__(self, syntax):
        self.syntax = syntax


    def parse_row(self, table, line):
        row = self.create_row(table, line)

        for line_cell in line.cells:
            column = self.create_column(table, row, line_cell)
            row.append(column)
        return row

    def create_row(self, table, line):
        raise NotImplementedError

    def create_column(self, table, row, line_cell):
        column = row.create_column(line_cell.text)
        column.left_border_text = line_cell.left_border_text
        column.right_border_text = line_cell.right_border_text
        return column

    def is_table_row(self, row):
        return re.match(r"^\s*" + self.syntax.hline_border_pattern(),
                        row) is not None


    def parse_text(self, text):
        table = TextTable(self.syntax)
        lines = text.splitlines()
        lineParser = LineParser(self.syntax)
        for ind, line in enumerate(lines):

            line = lineParser.parse(line)
            if ind == 0 :
                table.prefix = line.prefix
            row = self.parse_row(table, line)
            table.add_row(row)
        table.pack()
        return table



class LineRegion:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

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
    def __init__(self, syntax):
        self.syntax = syntax

    def parse(self, line_text):

        line = Line()

        mo = re.search(r"[^\s]", line_text)
        if mo:
            line.prefix = line_text[:mo.start()]
        else:
            line.prefix = ""

        if self.syntax.multi_markdown_syntax():
            pattern = "(?:{0}{0}+)|{1}".format(re.escape(self.syntax.vline ),
                                              self.syntax.hline_border_pattern()
                                             )
        else:
            pattern = self.syntax.hline_border_pattern()


        borders = []

        last_border_end = 0
        for m in re.finditer(pattern, line_text):
            borders.append(LineRegion(m.start(),m.end()))
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

