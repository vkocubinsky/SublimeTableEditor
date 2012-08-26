==================
SublimeTableEditor
==================

--------
Overview
--------

This package provide functionality similar to Emacs org-mode built-in table editor.

--------
Settings
--------

For disable table auto format you should set **disable_auto_table_edit=true**. 

---------
Alignment
---------

By default text data is left justified, numeric data is right justified, column header is centered.
::
    |     column 1     |      column 2      |
    |  second line 1   |   second line 2    |
    |------------------|--------------------|
    | text value row 1 | 0.9999999999999999 |
    | tv row 2         |                 99 |

But you can explicit set justification with format characters '<','>','#'. 
::
    | column 1 | column 2 | column 3 |
    | <<<<<<<< | >>>>>>>> | ######## |
    |----------|----------|----------|
    | 1        |    row 1 |    c1    |
    | 2        |    row 2 |    c2    |
    | 3        |    row 3 |    c3    |
    | ######## | <<<<<<<< | >>>>>>>> |
    |    1     | row 1    |       c1 |
    |    2     | row 2    |       c2 |
    |    3     | row 3    |       c3 |

You can change justification several times
::
    | column 1 | column 2 | column 3 |
    | <<<<<<<< | >>>>>>>> | ######## |
    |----------|----------|----------|
    | 1        |    row 1 |    c1    |
    | 2        |    row 2 |    c2    |
    | 3        |    row 3 |    c3    |
    | ######## | <<<<<<<< | >>>>>>>> |
    |    1     | row 1    |       c1 |
    |    2     | row 2    |       c2 |
    |    3     | row 3    |       c3 |

-----------
Key binding
-----------


ctrl+c, ctrl+c
    Re-align the table without moving the cursor.

tab
    Re-align the table, move to the next field. Creates a new row if necessary.

shift+tab
    Re-align, move to previous field.

alt + enter or enter
    Re-align the table and move down to next row. Creates a new row if necessary.
    At the beginning or end of a line, "enter" still does NEWLINE,
    so it can be used to split a table.

alt+a
    Move to beginning of the current table field, or on to the previous field.

alt+e
    Move to end of the current table field, or on to the next field.

alt+left
    Move the current column left/right.

alt+right
    Move the current column right.

alt+shift+left
    Kill the current column.

alt+shift+right
    Insert a new column to the left of the cursor position.

alt+up
    Move the current row up.

alt+down
    Move the current row down.

alt+shift+up
    Kill the current row or horizontal line.

alt+shift+down
    Insert a new row above the current row. With a prefix argument, the line is
    created below the current one.
