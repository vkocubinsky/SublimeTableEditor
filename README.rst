==================
SublimeTableEditor
==================

--------
Overview
--------

This package provide functionality similar to Emacs org-mode built-in table editor.

Type 
::
    | column 1 | column 2 |
    |-

Then use "tab" key for switch between cells and add new line you can easy populate the table
::
    | column 1 | column 2 |
    |----------|----------|
    |        1 | foo      |
    |        2 | bar      |


------------
Installation
------------

Use Package Control.

--------
Settings
--------

For disable table auto format you should set **disable_auto_table_edit=true**. 

-----------------
License and Price
-----------------
Package is distributed by Apache 2.0 License.

-------
Testing
-------

I tested **SublimeTextEditor** package only for windows. It should work under Linux and Mac, but I did not test.

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


-------------------------------------------
Difference from emacs org-mode table editor
-------------------------------------------

1. Emacs use character '+' in separator line, sublime text editor use character '|'.
::
    Emacs table:
    | col 1  | col2   | col3   |
    |--------+--------+--------|
    | data 1 | data 2 | data 3 |

    Sublime text editor table:
    | col 1  |  col2  |  col3  |
    |--------|--------|--------|
    | data 1 | data 2 | data 3 |

2. Commands next field, previous filed in emacs skip separator lines, sublime table editor doesn't skip.


These difference is for current version and I am going to get rid from some of them.


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
