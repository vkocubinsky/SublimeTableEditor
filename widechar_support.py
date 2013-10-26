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

import sys
import locale

breakable_char_ranges = [
    #http://en.wikipedia.org/wiki/Han_unification
    (0x4E00, 0x9FFF),   # CJK Unified Ideographs
    (0x3400, 0x4DBF),   # CJK Unified Ideographs Extension A
    (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
    (0x2E80, 0x2EFF),   # CJK Radicals Supplement
    (0x3000, 0x303F),   # CJK Symbols and Punctuation
    (0x31C0, 0x31EF),   # CJK Strokes
    (0x2FF0, 0x2FFF),   # Ideographic Description Characters
    (0x2F00, 0x2FDF),   # Kangxi Radicals
    (0x3200, 0x32FF),   # Enclosed CJK Letters and Months
    (0x3300, 0x33FF),   # CJK Compatibility
    (0xF900, 0xFAFF),   # CJK Compatibility Ideographs
    (0xFE30, 0xFE4F),   # CJK Compatibility Forms
    # See http://en.wikipedia.org/wiki/Hiragana
    (0x3040, 0x309F),   # Hiragana
    # See http://en.wikipedia.org/wiki/Katakana
    (0x30A0, 0x30FF),   # Katakana
    # See http://en.wikipedia.org/wiki/Hangul
    (0x1100, 0x11FF),   # Hangul Jamo
    (0x3130, 0x318F),   # Hangul Compatibility Jamo
    (0xA960, 0xA97F),   # Hangul Jamo Extended-A
    (0xD7B0, 0xD7FF),   # Hangul Jamo Extended-B
    (0xAC00, 0xD7A3),   # Hangul syllables
    # See http://en.wikipedia.org/wiki/Kanbun
    (0x3190, 0x319F),   # Kanbun
    # See http://en.wikipedia.org/wiki/Halfwidth_and_Fullwidth_Forms
    (0xFF00, 0xFFEF),    # Halfwidth and Fullwidth Forms
]



def _is_widechar(c):
    c = ord(c)
    for i in breakable_char_ranges:
        if isinstance(i, tuple):
            start, end = i
            if c >= start and c <= end:
                return True
        else:
            if i == c:
                return True
    return False


def _norm_text(text):
    if sys.version_info[0] == 2 and isinstance(text, str):
        text = unicode(text, locale.getpreferredencoding())
    return text


def wcount(text):
    text = _norm_text(text)
    count = 0
    for c in text:
        if _is_widechar(c):
            count = count + 1
    return count


def wlen(text):
    text = _norm_text(text)
    return len(text) + wcount(text)
