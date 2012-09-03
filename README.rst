==================
SublimeTableEditor
==================

--------
Overview
--------

SublimeTableEditor is a package for everyone who uses Sublime Editor for edit simple text tables in text mode, markdown mode, textile mode etc. SublimeTableEditor allow on easy way edit text table, it allow:
- add/delete row
- add/delete column
- navigate with tab/shift tab
- auto align number cells and text cells
- move column left/right
- specify column alignment

SublimeTableEditor is very similar to emacs org-mode table editor with the same key binding. 


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


Using Sublime Package Control
=============================

Through Package Control http://wbond.net/sublime_packages/package_control

- Open Package Control
- Select 'Install Package'
- Find and select 'Table Editor'

Using Git
=========

You can locate your Sublime Text 2 Packages directory by using the menu item Preferences -> Browse Packages....
While inside the Packages directory, clone the theme repository using the command below:
git clone https://github.com/vkocubinsky/SublimeTableEditor.git SublimeTableEditor

Download Manually
==========================

- Download the files using the GitHub .zip download option.
- Unzip the files and rename the folder to SublimeTableEditor.
- Copy the folder to your Sublime Text 2 Packages directory.


--------
Settings
--------

For disable table auto format you should set **disable_auto_table_edit=true**. The main case is 
use this setting for some languages. For example you can disable SublimeTableEditor for python language if you add
this setting to Python.sublime-settings.

-------
License
-------
Package is distributed by GPL v3.0 License.

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

I am more interested add support reStructured grid tables than get rid from this difference.

2. Commands next field, previous filed in emacs skip separator lines, sublime table editor doesn't skip.
These difference is for current version and I am going to get rid from this difference.

3. Move to beginning of the current table field and move to end of the current table field has differnt keybinding and emacs has additional feature move to previous/next table field if cursor already in begin/end of the table column.

4. Move row up / Move row down is standard sublime feature and can be done with ctrl+shift+up, ctrl+shift+down.

-----------
Key binding
-----------


ctrl+c, ctrl+c
    Re-align the table without change the current table field. Move cursor to begin of the current table field.

tab
    Re-align the table, move to the next field. Creates a new row if necessary. 

shift+tab
    Re-align, move to previous field.

alt + enter or enter
    Re-align the table and move down to next row. Creates a new row if necessary.

ctrl+left
    Re-align the table and move to beginning of the current table field.

ctrl+right
    Re-align the table and move to end of the current table field.

alt+left
    Move the current column left.

alt+right
    Move the current column right.

alt+shift+left
    Kill the current column.

alt+shift+right
    Insert a new column to the left of the cursor position.

alt+shift+up
    Kill the current row or horizontal line.

alt+shift+down
    Insert a new row above the current row. 
