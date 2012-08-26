==================
SublimeTableEditor
==================

--------
Overview
--------

This package provide functionality similar to Emacs org-mode built-in table editor.



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
