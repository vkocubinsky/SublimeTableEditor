==================
SublimeTableEditor
==================

--------
Overview
--------

**SublimeTableEditor** is a package for everyone who uses Sublime Editor for edit simple text tables in text mode, markdown mode, textile mode etc. SublimeTableEditor allow on easy way edit text table, it allows:

- insert/delete row
- insert/delete column
- navigate with tab/shift tab 
- auto align number cells to right and text cells to left
- move column left/right
- move row up/down
- specify column alignment
- show integration tests film
- temporary disable/enable table editor

For first time you should enable table editor with command palette 

* click Ctrl+Shift+P
* select Table Editor: Enable for current syntax or Table Editor: Enable for current view

Then when Table Editor is eabled just type
::
    | Name | Age |
    |-

Then press *Tab* key, you will get
::
    | Name | Age |
    |------|-----|
    | _    |     |

Then fill data and press *Tab* key to next field or add new row
::
    |    Name   | Age |
    |-----------|-----|
    | Anna      |  20 |
    | Alexander |  27 |
    | _         |     |


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


Press ctrl+x, ctrl+t and sublime show for you demo in new scratch view(just close this view after finish). It is integration test and demo at the same time. 

------------
Installation
------------

Using Sublime Package Control
=============================

It is preferred and simplest way for most users. 

- Install Package Control http://wbond.net/sublime_packages/package_control
- Open Package Control
- Select 'Install Package'
- Find and select 'Table Editor'

Using Git
=========

If you like work with HEAD you can locate SublimeTableEditor in your packages directory.

- Go to your Packages directory, you can locate to your Packages directory by using the menu item 
  Preferences ->   Browse Packages...
- Inside the Packages directory, clone the SublimeTableEditor repository using the command below: 
  git clone https://github.com/vkocubinsky/SublimeTableEditor.git SublimeTableEditor

Download Manually
=================

- Download the files using the GitHub .zip download option.
- Unzip the files and rename the folder to something like SublimeTableEditor.
- Copy the folder to your Sublime Text 2 Packages directory.

-----
Setup
-----

By default Table Editor is disable. You be able enable Table Editor for:

* specific synax
* specific view 
* all files scope

**Enable for syntax scope**

It is most usable option. Usually you like to enable Table Editor for Plain text, Markdown, Textile, reStructuredText syntax. 

For enable Table Editor for specific syntax

* Open file with specific syntax(for example .txt for Plain text)
* Click Ctrl+Shift+P for show command palette
* Select 'Table Editor: Enable for current syntax'

For disable Table Editor for specific syntax

* Open file with specific syntax(for example .txt for Plain text)
* Click Ctrl+Shift+P for show command palette
* Select 'Table Editor: Disable for current syntax'

You can do the same manually by

* Open file with specific syntax(for example .txt for Plain text)
* Click Preferences -> Settings - More -> Syntax Specific User
* put setting "enable_table_editor": true or put setting "enable_table_editor": false
* save Syntax Specific File

**Enable for view**

Some time you like temporary enable table editor and then disable it. It is usefull if you edit python or java code
and like to pretty print table

For do this you should:
* Click Ctrl+Shift+P for show command palette
* Select "Table Editor: Enable for current view"

Then after you edit table you can disable Table Editor
* Click Ctrl+Shift+P for show command palette
* Select "Table Editor: Disable for current view"

**Enable for all files**

* Click Preferences -> Settings - User
* put setting "enable_table_editor": true

-------
License
-------

Package is distributed by GPL v3.0 License.

-------
Testing
-------

I tested **SublimeTextEditor** package under Windows and quickly tested under Linux. It should work under Mac, but I did not test, because I do not have a mac.

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

alt+up
    Move current row up

alt+down 
    Move current row down

ctrl+c, -
    Insert a horizontal line below current row. 

ctrl+c, enter(This feature is not implemented)
    Insert a horizontal line below current row, and move the cursor into the row below that line. 

ctrl+x, ctrl+t
    Show Table Editor film in new scratch view


-------------------------------------------
Difference from emacs org-mode table editor
-------------------------------------------

SublimeTableEditor is very similar to emacs org-mode table editor with the same key binding. In fact I always run emacs and compare with Sublime Text Editor to get the same behavior.

But exists some differences. Most significant is Emacs use character '+' in separator line, sublime text editor use character '|'.

Emacs table:
::
    
    | col 1  | col2   | col3   |
    |--------+--------+--------|
    | data 1 | data 2 | data 3 |

Sublime text editor table:
::
    | col 1  |  col2  |  col3  |
    |--------|--------|--------|
    | data 1 | data 2 | data 3 |

I am more interested add support markup specific syntaxes, for example reStructured grid tables than get rid from this difference.

-----------
Know Issues
-----------

1. Move row up , move row down work correct only for single selection and doesn't work properly for multiple selection.
2. Ctrl+c, enter is doesn't work as expeted

These will be fixed for GA version. 



