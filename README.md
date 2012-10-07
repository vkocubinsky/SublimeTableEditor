# Table Editor

## Overview

*Table Editor* is a package for edit simple text tables in text mode, markdown mode, textile mode, reStructuredText mode etc. *Table Editor* is very similar to Emacs-org mode table editor with almost the same keys. *Table Editor* allow on easy way edit text table, it allows:

- navigate with tab/shift tab 
- insert/delete row
- insert/delete column
- auto align number cells to right, text cells to left, header cells to center
- move column left/right
- move row up/down
- split long cell
- join two rows into one
- specify column alignment
- convert selected CSV region into table
- temporary disable/enable table editor
- show integration tests film

## Usage

### Basic editing

For first time you should enable table editor with command palette:

* click *ctrl+shift+p*
* select *Table Editor: Enable for current syntax* or *Table Editor: Enable for current view*

Then when *Table Editor* is enabled, type

    | Name | Phone |
    |-

Then press *Tab* key, you will get pretty printed table

    | Name | Phone |
    |------|-------|
    | _    |       |

Then fill a data and press *Tab* key to next field or add new row if necessary 

    |    Name   |   Phone   |
    |-----------|-----------|
    | Anna      | 123456789 |
    | Alexander | 987654321 |
    | _         |           |

For make table a bit faster faster type only

    |Name|Phone

And then click *ctrl+k,enter*. 

Additional to *tab* and *shift+tab* use *enter*  for move cursor down and insert new row if necessary.

### Work with columns

Let's we have a table with columns *| Name | Phone |*, and you decide insert column *| Age |* before column *| Phone |*.
For do this set cursor position into any rows in column Phone

    |    Name   |   Phone   |
    |-----------|-----------|
    | Anna      | 123456789 |
    | Alexander | 987654321 |
    |           | _         |

Click *alt+shift+right*

    |    Name   |   |   Phone   |
    |-----------|---|-----------|
    | Anna      |   | 123456789 |
    | Alexander |   | 987654321 |
    |           | _ |           |

Fill *| Age |* column

    |    Name   | Age |   Phone   |
    |-----------|-----|-----------|
    | Anna      |  32 | 123456789 |
    | Alexander |  28_| 987654321 |
    |           |     |           |

Then after some thought you decide switch columns *| Age |* and *| Phone |*. For do this, you can click *alt+right* when 
cursor in the *| Age |* column or you can click *alt+left* when cursor position in the *| Phone |* column

    |    Name   |   Phone   | Age |
    |-----------|-----------|-----|
    | Anna      | 123456789 | 32  |
    | Alexander | 987654321 | 28_ |
    |           |           |     |

Now cursor position in the *| Age |* column, when you click *ctrl+shift+left*, column *| Age |* will be deleted

    |    Name   |   Phone    |
    |-----------|------------|
    | Anna      | 123456789  |
    | Alexander | 987654321_ |
    |           |            |


### Work with rows

Let's we have a table

    |    Name   |   Phone   | Age |
    |-----------|-----------|-----|
    | Anna      | 123456789 | 32_ |
    | Alexander | 987654321 | 28  |
    |           |           |     |

For insert row bellow current cursor position click *alt+shift+down*

    |    Name   |   Phone   | Age |
    |-----------|-----------|-----|
    |           |           | _   |
    | Anna      | 123456789 | 32  |
    | Alexander | 987654321 | 28  |
    |           |           |     |

For delete row click *alt_shift+up*

    |    Name   |   Phone   | Age |
    |-----------|-----------|-----|
    | Anna      | 123456789 | 32_ |
    | Alexander | 987654321 | 28  |
    |           |           |     |

Some time you cell value became to long as in next example column *| Position |*

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior Software Engineer_        |
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |           |           |     |                                  |

You like to split value of column *| Position |* into several rows.
First let's click *ctrl+k,-* for insert hline after cursor position

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior Software Engineer_        |
    |-----------|-----------|-----|----------------------------------|
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |           |           |     |                                  |

Then let's move cursor to before word *Engineer* in the first row and click *alt+enter*

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior Software                  |
    |           |           |     | Engineer_                        |
    |-----------|-----------|-----|----------------------------------|
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |           |           |     |                                  |

Move cursor before word *Software* in the first row and click *alt+enter* again

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior                           |
    |           |           |     | Software Engineer_               |
    |-----------|-----------|-----|----------------------------------|
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |           |           |     |                                  |

Move cursor to the first row after word *Senior* and click *ctrl+j*

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior Software Engineer_        |
    |-----------|-----------|-----|----------------------------------|
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |           |           |     |                                  |

Let's move cursor with tab key to second row(hlines skipped automatically) and click *ctrl+k,enter*

    |    Name   |   Phone   | Age |             Position             |
    |-----------|-----------|-----|----------------------------------|
    | Anna      | 123456789 |  32 | Senior Software Engineer         |
    |-----------|-----------|-----|----------------------------------|
    | Alexander | 987654321 |  28 | Senior Software Testing Engineer |
    |-----------|-----------|-----|----------------------------------|
    | _         |           |     |                                  |



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

**enter**

        Re-align the table and move down to next row. Creates a new row if necessary.
        At the beginning or end of a line, enter still does new line.

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

**alt+enter**
    
        Split rest of cell down from current cursor position,
        insert new line bellow if current row is last row in the table or if next line is hline

 **ctrl+j**
        
        Join current row and next row into one if next row is not hline
 

## License

Package is distributed by GNU General Public License v3.0.

## Donation

You can make a donation online, using the link below with PayPal service

[Donate](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=CBL373WUKNTZW 
                "Make a Donation to the Table Editor")

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

