# table_base.py - Key classes and methods for pretty print text table.

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
    from . import table_line_parser as tparser
    from .widechar_support import wlen, wcount
except ValueError:
    import table_line_parser as tparser
    from widechar_support import wlen, wcount


class TableConfiguration:
    def __init__(self):
        self.keep_space_left = False
        self.align_number_right = True
        self.detect_header = True
        self.intelligent_formatting = True

        #only for simple syntax
        self.hline_out_border = None
        self.hline_in_border = None
        self.custom_column_alignment = True


class TableSyntax:

    def __init__(self, name, table_configuration):
        self.name = name
        self.table_configuration = table_configuration or TableConfiguration()

        self.align_number_right = self.table_configuration.align_number_right
        self.detect_header = self.table_configuration.detect_header
        self.keep_space_left = self.table_configuration.keep_space_left
        self.intelligent_formatting = self.table_configuration.intelligent_formatting

        self.line_parser = tparser.LineParserPlus("(?:[|])")
        # Must be set in sublass constructor
        self.table_parser = None
        self.table_driver = None




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
        self.left_border_text = '|'
        self.right_border_text = '|'

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
        r = ""
        for ind, column in enumerate(self.columns):
            if column.pseudo():
                continue
            if ind == 0:
                r += self.convert_border(column.left_border_text)
            r += column.render()
            r += self.convert_border(column.right_border_text)
        return r

    def convert_border(self, border_text):
        # if separator converts to data
        return border_text.replace('+', '|')


class DataRow(Row):

    def new_empty_column(self):
        return DataColumn(self, '')

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
        total_min_len = max(space_len + 1, wlen(self._norm()) + space_len)
        total_min_len = (total_min_len
                         + (len(self.left_border_text) - 1)
                         + (len(self.right_border_text) - 1))
        return total_min_len

    def render(self):
        # colspan -1 is count of '|'
        total_col_len = (self.col_len
                         + (self.colspan - 1)
                         + sum([col.col_len for col in self.pseudo_columns]))

        #if self.syntax.multi_markdown_syntax():
        #    total_col_len = total_col_len - (self.colspan - 1)
        total_col_len = (total_col_len
                         # left border already calculated
                         # - (len(self.left_border_text) - 1)
                         - (len(self.right_border_text) - 1))

        norm = self._norm()
        space_len = len(self.left_space) + len(self.right_space)

        total_align_len = total_col_len - wcount(norm)
        if self.header and self.syntax.detect_header:
            align_value = norm.center(total_align_len - space_len, ' ')
        elif self.align == Column.ALIGN_RIGHT:
            align_value = norm.rjust(total_align_len - space_len, ' ')
        elif self.align == Column.ALIGN_CENTER:
            align_value = norm.center(total_align_len - space_len, ' ')
        else:
            align_value = norm.ljust(total_align_len - space_len, ' ')
        return self.left_space + align_value + self.right_space


def check_condition(condition, message):
    if not condition:
        raise TableException(message)


class TextTable:

    def __init__(self, syntax):
        self.syntax = syntax
        self.prefix = ""
        self.rows = []
        self.pack()

    def __len__(self):
        return len(self.rows)

    def empty(self):
        return len(self.rows) == 0

    def __getitem__(self, index):
        return self.rows[index]

    def _max_column_count(self):
        return max([len(row) for row in self.rows])

    def _rstrip(self):
        if len(self.rows) <= 1:
            return
        max_column_count = self._max_column_count()
        long_lines_count = 0
        long_line_ind = 0
        for row_ind, row in enumerate(self.rows):
            if len(row) == max_column_count:
                long_lines_count += 1
                long_line_ind = row_ind

        if long_lines_count == 1:
            row = self.rows[long_line_ind]
            overspans = sum([column.colspan - 1 for column in row.columns])
            if row.is_data() and overspans > 0:
                shift = 0
                for shift, column in enumerate(row[::-1]):
                    if column.pseudo() or len(column.data.strip()) > 0:
                        break
                if shift > 0:
                    if len(self.rows) == 2:
                        if shift != overspans:
                            return

                    row.columns = row.columns[:-shift]

    def pack(self):
        if len(self.rows) == 0:
            return

        column_count = self._max_column_count()

        if column_count == 0:
            self.rows = []
            return

        #intelligent formatting
        if self.syntax.intelligent_formatting:
            self._rstrip()
            column_count = self._max_column_count()

        #adjust/extend column count
        rowspans = [0] * column_count
        for row in self.rows:
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
        for row in self.rows:
            for col_ind, column in enumerate(row.columns):
                col_lens[col_ind] = max(col_lens[col_ind], column.min_len())

        #set column len
        for row in self.rows:
            for column, col_len in zip(row.columns, col_lens):
                column.col_len = col_len

        #header
        header_separator_index = -1
        first_data_index = -1
        if self.syntax.detect_header:
            for row_ind, row in enumerate(self.rows):
                if first_data_index == -1 and row.is_data():
                    first_data_index = row_ind
                if (first_data_index != -1 and header_separator_index == -1
                        and row.is_header_separator()):
                    header_separator_index = row_ind
                    for header_index in range(first_data_index, header_separator_index):
                        if self.rows[header_index].is_data():
                            for column in self.rows[header_index].columns:
                                column.header = True

        #set column alignment
        data_alignment = [None] * len(col_lens)
        for row_ind, row in enumerate(self.rows):
            if row_ind < header_separator_index:
                if row.is_align():
                    for col_ind, column in enumerate(row.columns):
                        data_alignment[col_ind] = column.align_follow()
                continue
            elif row.is_align():
                for col_ind, column in enumerate(row.columns):
                    data_alignment[col_ind] = column.align_follow()
            elif row.is_data():
                for col_ind, column in enumerate(row.columns):
                    if data_alignment[col_ind] is None:
                        if self.syntax.align_number_right and self._is_number_column(row_ind, col_ind):
                            data_alignment[col_ind] = Column.ALIGN_RIGHT
                        else:
                            data_alignment[col_ind] = Column.ALIGN_LEFT
                    column.align = data_alignment[col_ind]

    def _is_number_column(self, start_row_ind, col_ind):
        assert self.rows[start_row_ind].is_data()
        for row in self.rows[start_row_ind:]:
            if (row.is_data()
                    and col_ind < len(row.columns)
                    and len(row.columns[col_ind].data.strip()) > 0):
                        try:
                            float(row.columns[col_ind].data)
                        except ValueError:
                            return False
        return True

    def render_lines(self):
        return [self.prefix + row.render() for row in self.rows]

    def render(self):
        return "\n".join(self.render_lines())

    def is_col_colspan(self, col):
        for row in self.rows:
            if col < len(row):
                if row[col].pseudo() or row[col].colspan > 1:
                    return True
        return False

    def is_row_colspan(self, row):
        for column in self[row].columns:
            if column.pseudo() or column.colspan > 1:
                    return True
        return False

    def assert_not_col_colspan(self, col):
        check_condition(self.is_col_colspan(col) is False,
                        "Expected not colspan column, but column {0}"
                        " is colspan".format(col))

    def delete_column(self, col):
        self.assert_not_col_colspan(col)
        for row in self.rows:
            if col < len(row):
                del row.columns[col]
        self.pack()

    def swap_columns(self, i, j):
        self.assert_not_col_colspan(i)
        self.assert_not_col_colspan(j)
        for row in self.rows:
            if i < len(row) and j < len(row):
                row.columns[i], row.columns[j] = row.columns[j], row.columns[i]
        self.pack()

    def delete_row(self, i):
        assert 0 <= i < len(self.rows)

        del self.rows[i]
        self.pack()

    def swap_rows(self, i, j):
        check_condition((0 <= i < len(self.rows) and
                        0 <= j < len(self.rows)),
                        "Index out of range")

        self.rows[i], self.rows[j] = self.rows[j], self.rows[i]
        for column in self.rows[i].columns:
            column.header = False
        for column in self.rows[j].columns:
            column.header = False

        self.pack()

    def insert_empty_row(self, i):
        check_condition(i >= 0, "Index should be more than zero")

        self.rows.insert(i, DataRow(self))
        self.pack()

    def insert_empty_column(self, i):
        check_condition(i >= 0, "Index should be more than zero")
        self.assert_not_col_colspan(i)

        for row in self.rows:
            row.columns.insert(i, row.new_empty_column())
        self.pack()


class TableException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TablePos:

    def __init__(self, row_num, field_num):
        self.row_num = row_num
        self.field_num = field_num

    def __repr__(self):
        return "TablePos({self.row_num}, {self.field_num})".format(self=self)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return (self.row_num == other.row_num
                and self.field_num == other.field_num)


class TableDriver:

    def __init__(self, syntax):
        self.syntax = syntax

    def visual_column_count(self, table, row_ind):
        return sum([1 for column in table[row_ind].columns
                   if not column.pseudo()])

    def internal_to_visual_index(self, table, internal_pos):
        visual_pos = TablePos(internal_pos.row_num, internal_pos.field_num)
        for col_ind in range(internal_pos.field_num + 1):
            if table[internal_pos.row_num][col_ind].pseudo():
                visual_pos.field_num -= 1
        return visual_pos

    def visual_to_internal_index(self, table, visual_pos):
        internal_pos = TablePos(visual_pos.row_num, 0)
        count_visual = 0
        internal_pos.field_num = 0
        for col_ind in range(len(table[visual_pos.row_num])):
            if not table[visual_pos.row_num][col_ind].pseudo():
                count_visual += 1
                internal_pos.field_num = col_ind
            if count_visual == visual_pos.field_num + 1:
                break
        else:
            print("WARNING: Visual Index Not found")
        return internal_pos

    def get_cursor(self, table, visual_pos):
        #
        # '   |  1 |  2  |  3_| 4 |'
        internal_pos = self.visual_to_internal_index(table, visual_pos)
        base_len = (len(table.prefix)
                    + sum([column.col_len - wcount(column.render()) for column, ind
                          in zip(table[visual_pos.row_num].columns,
                                 range(internal_pos.field_num))])
                    + internal_pos.field_num + 1  # count of '|'
                    )
        text = table[internal_pos.row_num][internal_pos.field_num].render()
        match = re.search(r"([^\s])\s*$", text)
        if match:
            col_pos = match.end(1)
        else:
            col_pos = 1
        return base_len + col_pos

    def editor_move_column_left(self, table, table_pos):
        internal_pos = self.visual_to_internal_index(table, table_pos)
        field_num = internal_pos.field_num
        if field_num > 0:
            if (table.is_col_colspan(field_num) or
                    table.is_col_colspan(field_num - 1)):
                raise TableException("Move Column Left is not "
                                     "permitted for colspan column")
            else:
                table.swap_columns(field_num, field_num - 1)
                return ("Column moved to left",
                        TablePos(table_pos.row_num, table_pos.field_num - 1))
        else:
            raise TableException("Move Column Left doesn't "
                                 "make sence for the first column in the "
                                 "table.")

    def editor_move_column_right(self, table, table_pos):
        internal_pos = self.visual_to_internal_index(table, table_pos)
        field_num = internal_pos.field_num

        if field_num < len(table[table_pos.row_num]) - 1:
            if (table.is_col_colspan(field_num) or
                    table.is_col_colspan(field_num + 1)):
                raise TableException("Move Column Right is not "
                                     "permitted for colspan column")
            else:
                table.swap_columns(field_num, field_num + 1)
                return ("Column moved to right",
                        TablePos(table_pos.row_num, table_pos.field_num + 1))
        else:
            raise TableException("Move Column Right doesn't "
                                 "make sense for the last column in the "
                                 "table.")

    def editor_move_row_up(self, table, table_pos):
        if table_pos.row_num > 0:
            table.swap_rows(table_pos.row_num, table_pos.row_num - 1)
            return("Row moved up",
                   TablePos(table_pos.row_num - 1, table_pos.field_num))
        else:
            raise TableException("Move Row Up doesn't make sense for the "
                                 "first row in the table")

    def editor_move_row_down(self, table, table_pos):
        if table_pos.row_num + 1 < len(table):
            table.swap_rows(table_pos.row_num, table_pos.row_num + 1)
            return ("Row moved down",
                    TablePos(table_pos.row_num + 1, table_pos.field_num))
        else:
            raise TableException("Move Row Down doesn't make sense for the "
                                 "last row in the table")

    def editor_next_row(self, table, table_pos):
        if table_pos.row_num + 1 < len(table):
            if table[table_pos.row_num + 1].is_header_separator():
                table.insert_empty_row(table_pos.row_num + 1)
        else:
            table.insert_empty_row(len(table))
        return ("Moved to next row",
                TablePos(table_pos.row_num + 1, table_pos.field_num))

    def editor_delete_column(self, table, table_pos):
        internal_pos = self.visual_to_internal_index(table, table_pos)
        field_num = internal_pos.field_num

        if table.is_col_colspan(field_num):
            raise TableException("Delete column is not permitted for "
                                 "colspan column")
        else:
            table.delete_column(field_num)
            new_table_pos = TablePos(table_pos.row_num,
                                     table_pos.field_num)
            if (not table.empty() and
                    table_pos.field_num == len(table[table_pos.row_num])):
                new_table_pos.field_num = new_table_pos.field_num - 1
            return("Column deleted", new_table_pos)

    def editor_insert_column(self, table, table_pos):
        internal_pos = self.visual_to_internal_index(table, table_pos)
        field_num = internal_pos.field_num

        if table.is_col_colspan(field_num):
            raise TableException("Insert column is not permitted for "
                                 "colspan column")
        else:
            table.insert_empty_column(field_num)
            return ("Column inserted",
                    TablePos(table_pos.row_num, table_pos.field_num))

    def editor_kill_row(self, table, table_pos):
        table.delete_row(table_pos.row_num)
        new_table_pos = TablePos(table_pos.row_num, table_pos.field_num)
        if table_pos.row_num == len(table):
            new_table_pos.row_num = new_table_pos.row_num - 1
        return ("Row deleted", new_table_pos)

    def editor_insert_row(self, table, table_pos):
        table.insert_empty_row(table_pos.row_num)
        return ("Row inserted",
                TablePos(table_pos.row_num, table_pos.field_num))

    def editor_insert_single_hline(self, table, table_pos):
        raise TableException("Syntax {0} doesn't support insert single line"
                             .format(self.syntax.name))

    def editor_insert_double_hline(self, table, table_pos):
        raise TableException("Syntax {0} doesn't support insert double line"
                             .format(self.syntax.name))

    def editor_insert_hline_and_move(self, table, table_pos):
        raise TableException("Syntax {0} doesn't support insert single line "
                             "and move".format(self.syntax.name))

    def editor_align(self, table, table_pos):
        return ("Table aligned",
                TablePos(table_pos.row_num, table_pos.field_num))

    def editor_join_lines(self, table, table_pos):
        if (table_pos.row_num + 1 < len(table)
            and table[table_pos.row_num].is_data()
            and table[table_pos.row_num + 1].is_data()
            and not table.is_row_colspan(table_pos.row_num)
                and not table.is_row_colspan(table_pos.row_num + 1)):

            for curr_col, next_col in zip(table[table_pos.row_num].columns,
                                          table[table_pos.row_num + 1].columns):
                curr_col.data = curr_col.data.strip() + " " + next_col.data.strip()

            table.delete_row(table_pos.row_num + 1)
            return ("Rows joined",
                    TablePos(table_pos.row_num, table_pos.field_num))
        else:
            raise TableException("Join columns is not permitted")

    def editor_next_field(self, table, table_pos):
        pos = TablePos(table_pos.row_num, table_pos.field_num)

        moved = False
        while True:
            if table[pos.row_num].is_separator():
                if pos.row_num + 1 < len(table):
                    pos.field_num = 0
                    pos.row_num += 1
                    moved = True
                    continue
                else:
                    #sel_row == last_table_row
                    table.insert_empty_row(len(table))
                    pos.field_num = 0
                    pos.row_num += 1
                    break
            elif moved:
                break
            elif pos.field_num + 1 < self.visual_column_count(table, pos.row_num):
                pos.field_num += 1
                break
            elif pos.row_num + 1 < len(table):
                pos.field_num = 0
                pos.row_num += 1
                moved = True
                continue
            else:
                #sel_row == last_table_row
                table.insert_empty_row(len(table))
                pos.field_num = 0
                pos.row_num += 1
                break
        return ("Cursor position changed", pos)

    def editor_previous_field(self, table, table_pos):
        pos = TablePos(table_pos.row_num, table_pos.field_num)
        moved = False
        while True:
            if table[pos.row_num].is_separator():
                if pos.row_num > 0:
                    pos.row_num -= 1
                    pos.field_num = self.visual_column_count(table, pos.row_num) - 1
                    moved = True
                    continue
                else:
                    #row_num == 0
                    pos.field_num = 0
                    break
            elif moved:
                break
            elif pos.field_num > 0:
                pos.field_num -= 1
                break
            elif pos.row_num > 0:
                pos.row_num -= 1
                pos.field_num = self.visual_column_count(table, pos.row_num) - 1
                moved = True
                continue
            else:
                #row_num == 0
                break
        return ("Cursor position changed", pos)

    def parse_csv(self, text):
        try:
            table = TextTable(self.syntax)
            bytetext = text.encode('utf-8')
            dialect = csv.Sniffer().sniff(bytetext)
            table_reader = csv.reader(bytetext.splitlines(), dialect)
            for cols in table_reader:
                row = DataRow(table)
                for col in cols:
                    row.columns.append(DataColumn(row, unicode(col,'utf-8')))
                table.rows.append(row)
        except csv.Error:
            table = TextTable(self.syntax)
            for line in text.splitlines():
                row = DataRow(table)
                row.columns.append(DataColumn(row, line))
                table.rows.append(row)
        table.pack()
        return table


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
        return re.match(r"^\s*[|+]",row) is not None

    def parse_text(self, text):
        table = TextTable(self.syntax)
        lines = text.splitlines()
        for ind, line in enumerate(lines):

            line = self.syntax.line_parser.parse(line)
            if ind == 0:
                table.prefix = line.prefix
            row = self.parse_row(table, line)
            table.rows.append(row)
        table.pack()
        return table
