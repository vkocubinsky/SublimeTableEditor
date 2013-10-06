# table_pandoc_syntax.py - Pandoc table syntax

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


try:
    from . import table_base as tbase
    from . import table_border_syntax as tborder
except ValueError:
    import table_base as tbase
    import table_border_syntax as tborder


def create_syntax(table_configuration=None):
    return PandocTableSyntax(table_configuration)


class PandocTableSyntax(tbase.TableSyntax):

    def __init__(self, table_configuration):
        tbase.TableSyntax.__init__(self, "Pandoc", table_configuration)

        self.table_parser = tborder.BorderTableParser(self)
        self.table_driver = tborder.BorderTableDriver(self)

        self.hline_out_border = '+'
        self.hline_in_border = '+'
