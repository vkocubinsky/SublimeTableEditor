# widechar_support.py - Wide character support for SublimeTableEditor.

# Copyright (C) 2013  Free Software Foundation, Inc.

# Author: Zealic Zeng, Valery Kocubinsky
# Package: SublimeTableEditor
# Homepage: https://github.com/zealic/contrib-SublimeTableEditor

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

import unicodedata
import sys

def wcount(text):
    if sys.version_info[0] == 2 and isinstance(text, str):
        return 0
    else:
        return len([x for x in text if unicodedata.east_asian_width(x) == 'W'])


def wlen(text):
    return len(text) + wcount(text)
