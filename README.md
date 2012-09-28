# Table Editor

## Overview

*Table Editor* is a package for edit simple text tables in text mode, markdown mode, textile mode, reStructuredText mode etc. *Table Editor* is very similar to Emacs-org mode table editor with almost the same keys. *Table Editor* allow on easy way edit text table, it allows:

- insert/delete row
- insert/delete column
- navigate with tab/shift tab 
- auto align number cells to right, text cells to left, header cells to center
- move column left/right
- move row up/down
- specify column alignment
- convert selected CSV region into table
- temporary disable/enable table editor
- show integration tests film

## Usage

### Create and edit table

For first time you should enable table editor with command palette:

* click *ctrl+shift+p*
* select *Table Editor: Enable for current syntax* or *Table Editor: Enable for current view*

Then when *Table Editor* is eabled just type

    | Name | Age |
    |-

Then press *Tab* key, you will get pretty printed table

    | Name | Age |
    |------|-----|
    | _    |     |

Then fill data and press *Tab* key to next field or add new row

    |    Name   | Age |
    |-----------|-----|
    | Anna      |  20 |
    | Alexander |  27 |
    | _         |     |

For make table faster type only

    |Name|Age

And then click **ctrl+k,enter**, you will get 

    | Name | Age |
    |------|-----|
    | _    |     |

### Column alignment

By default text data is left justified, numeric data is right justified, column header is centered.

    |     column 1     |      column 2      |
    |  second line 1   |   second line 2    |
    |------------------|--------------------|
    | text value row 1 | 0.9999999999999999 |
    | tv row 2         |                 99 |

But you can explicit set justification with format characters 

* '<' - left 
* '>' - right
* '#' - center

as in next example

    | column 1 | column 2 | column 3 |
    | <<<<<<<< | >>>>>>>> | ######## |
    |----------|----------|----------|
    | 1        |    row 1 |    c1    |
    | 2        |    row 2 |    c2    |
    | 3        |    row 3 |    c3    |

You can change justification several times

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


### Convert CSV into table

Select some text with CSV data

    Name,Age
    Anna,20
    Alexander,27

 and then click *ctrl+k, |* to convert CSV data into table, you will get

    | Name      | Age |
    | Anna      | 20  |
    | Alexander | 27  |

*Convert CSV into table* command aumatically recognize CSV dialect, for example you can enter data separated by *tab*. If *Convert CSV into table* command can not regonize CSV dialect you will get one row table where selected line is a row in the table.


### Demo 

Press *ctrl+shift+p* to launch command palette and select *Table Editor: Show demo film in new scratch view* . It is integration test and demo at the same time. 


## Installation


### Using Sublime Package Control

It is preferred and simplest way for most users. 

- Install Package Control http://wbond.net/sublime_packages/package_control
- Open Package Control
- Select *Install Package*
- Find and select *Table Editor*

### Using Git

If you like work with HEAD you can locate *Table Editor* in your packages directory.

- Go to your Packages directory, you can locate to your Packages directory by using the menu item 
  *Preferences -> Browse Packages...*
- Inside the Packages directory, clone the SublimeTableEditor repository using the command below: 

  *git clone https://github.com/vkocubinsky/SublimeTableEditor.git "Table Editor"*
  

### Download Manually

- Download the files using the GitHub .zip download option.
- Unzip the files and rename the folder to *Table Editor*.
- Copy the folder to your Sublime Text 2 Packages directory.

## Settings

By default *Table Editor* is disable. You be able enable *Table Editor* for:

* specific synax
* current view 
* all files

You can ebable *Table Editor* with setting *"enable_table_editor": true* on a standard sublime way descrubed 
in http://docs.sublimetext.info/en/latest/customization/settings.html. But *Table Editor* out of the box contains
feature for set this property on a more simple way.

### Enable for specific syntax

It is most usable option. Usually you like to enable Table Editor for Plain text, Markdown, Textile, reStructuredText syntax. 

For enable Table Editor for specific syntax

* Open file with specific syntax(for example .txt for Plain text)
* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Enable for current syntax*

For disable Table Editor for specific syntax

* Open file with specific syntax(for example .txt for Plain text)
* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Disable for current syntax*

You can do the same manually by

* Open file with specific syntax(for example .txt for Plain text)
* Click *Preferences -> Settings - More -> Syntax Specific User*
* put setting *"enable_table_editor": true* or put setting *"enable_table_editor": false* 
  or delete line with propert *enable_table_editor*
* save Syntax Specific File

### Enable for current view

Some time you like temporary enable table editor and then disable it. It is usefull if you edit *Python* or *Java* code and like to pretty print table, then contine edit your code. For do this you should:

* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Enable for current view*

Then after you edit table you can disable Table Editor

* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Disable for current view*

### Enable for all files

Probably this option is usable if you work only with text or wiki markup files

* Click *Preferences -> Settings - User*
* put setting *"enable_table_editor": true*

## Key binding

**ctrl+shift+a**

        Re-align the table without change the current table field. Move cursor to begin of the current table field.

**tab**

        Re-align the table, move to the next field. Creates a new row if necessary. 

**shift+tab**

        Re-align, move to previous field.

**alt + enter or enter**

        Re-align the table and move down to next row. Creates a new row if necessary.

**alt+left**

        Move the current column left.

**alt+right**

        Move the current column right.

**alt+shift+left**

        Kill the current column.

**alt+shift+right**

        Insert a new column to the left of the cursor position.

**alt+shift+up**

        Kill the current row or horizontal line.

**alt+shift+down**

        Insert a new row above the current row. 

**alt+up**

        Move current row up

**alt+down**

        Move current row down

**ctrl+k, -**

        Insert a horizontal line below current row. 

**ctrl+k, enter**

        Insert a horizontal line below current row, and move the cursor into the row below that line. 

**ctrl+k, |**

        Convert selected CSV region into table




## License

Package is distributed by GNU General Public License v3.0.

## Donation

You can make a donation online, using the link below with PayPal service

[Donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CBL373WUKNTZW "Make a Donation to the Table Editor")

## Testing

I tested *Table Editor* package under Windows and quickly tested under Linux. It should work under Mac, but I did not test, because I do not have a mac.


## Difference from emacs org-mode table editor

*Table Editor* is very similar to emacs org-mode table editor with the same key binding. In fact I always run *Emacs*
and compare with *Table Editor* to get similiar behavior.

But exists some differences. One of this is Emacs use character '+' in separator line, sublime text editor use character '|'.

Emacs table:

    
    | col 1  | col2   | col3   |
    |--------+--------+--------|
    | data 1 | data 2 | data 3 |

Sublime text editor table:

    | col 1  |  col2  |  col3  |
    |--------|--------|--------|
    | data 1 | data 2 | data 3 |


Second one is navigation between field. Emacs set pointer to begin of field indepent of alignment, additionally 
*Emacs* has keys *alt-a* to navigate to the begin of field, *alt-e* to navigate to the end of field.
*Table Editor* combine it into one and set point to the end of data in field. 

