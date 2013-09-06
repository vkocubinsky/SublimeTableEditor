# Table Editor

## Overview

*Table Editor* is a package for the *Sublime Text 2* and *Sublime Text 3* 
editor for edit text tables. 
*Table Editor* is has almost the same keys as Emacs-org mode table editor. 

*Table Editor* allow on easy way edit text table, it allows:

- navigate with tab/shift tab 
- insert/delete row
- insert/delete column
- auto align number cells to right, text cells to left, header cells to center
- move column left/right
- move row up/down
- split long cell
- join two rows into one
- convert selected CSV region into table
- direct support subset of wiki table syntax
    - Simple
    - EmacsOrgMode
    - Pandoc(Grid Tables, Pipe Tables)
    - Multi Markdown(support colspan in alpha status)
    - reStructuredText
    - Textile(support colspan and rowspan in alpha status)
- auto detect table syntax by view syntax
- switch between different table syntax on the fly
- temporary disable/enable table editor for current view
- customize table syntax with settings
- support CJK : Chinese, Japanese, Korean(alpha status)
- show demo film in scratch view

## Usage

### Basic editing

For first time you should enable table editor with command palette:

* click *ctrl+shift+p*
* select *Table Editor: Enable for current syntax* or *Table Editor: Enable for current view* or "Table Editor: Set table syntax ... for current view"

Then when *Table Editor* is enabled, type

    | Name | Phone |
    |-

Then press *Tab* key, you will get pretty printed table

    | Name | Phone |
    |------|-------|
    | _    |       |

Then fill a data and press *Tab* key to navigate to next field or add new row if necessary 

    |    Name   |   Phone   |
    |-----------|-----------|
    | Anna      | 123456789 |
    | Alexander | 987654321 |
    | _         |           |

For make table a bit faster faster type only

    |Name|Phone

And then click *ctrl+k,enter*. 

    | Name | Phone |
    |------|-------|
    | _    |       |

*Table Editor* support double hline with character '='. Type bellow 

    | Name | Phone |
    |=

and click *tab* key

    | Name | Phone |
    |======|=======|
    | _    |       |

Then fill rows and click *ctrl+k,enter* each time when cursor in *Phone* position

    |    Name   |   Phone   |
    |===========|===========|
    | Anna      | 123456789 |
    |-----------|-----------|
    | Alexander | 987654321 |
    |-----------|-----------|
    | _         |           |


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

Now cursor position in the *| Age |* column, when you click *alt+shift+left*, column *| Age |* will be deleted

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


### Convert CSV into table

Select some text with CSV data

    Name,Age
    Anna,20
    Alexander,27

 and then click *ctrl+k, |* to convert CSV data into table, you will get

    | Name      | Age |
    | Anna      | 20  |
    | Alexander | 27  |

*Convert CSV into table* command automatically recognize CSV dialect, for example you can enter data separated by *tab*. If *Convert CSV into table* command can not recognize CSV dialect you will get one row table where selected line is a row in the table.


### Temporary Enable/Disable *Table Editor* for current view

Some time you like temporary enable table editor and then disable it. It is useful if you edit *Python* or *Java* code and like to pretty print table, then continue edit your code.
For do this you should:

* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Enable for current view*

Then after you edit table you can disable Table Editor

* Click *ctrl+shift+p* for show command palette
* Select *Table Editor: Disable for current view*

### Supported Syntaxes

Table editor support next table syntax:

- Simple
- EmacsOrgMode
- Pandoc
- Multi Markdown
- reStructuredText
- Textile

**Simple**

    |    Name   | Age |
    |-----------|-----|
    | Anna      |  20 |
    | Alexander |  27 |

**EmacsOrgMode**

    |    Name   | Age |
    |-----------+-----|
    | Anna      |  20 |
    | Alexander |  27 |

**Pandoc Grid Tables**

    +-----------+-----+
    |    Name   | Age |
    +===========+=====+
    | Anna      |  20 |
    +-----------+-----+
    | Alexander |  27 |
    +-----------+-----+

**Pandoc Pipe tables**

Pandoc Pipe tables is the same as Multi Markdown, you have to switch into 
Multi Markdown if you use this table style.

**Multi Markdown/Pandoc Pipe tables**

Alignment:

    |    Name   | Phone | Age Column |
    | :-------- | :---: | ---------: |
    | Anna      |   12  |         20 |
    | Alexander |   13  |         27 |


    | Right | Left | Default | Center |
    | ----: | :--- | ------- | :----: |
    |    12 | 12   |      12 |   12   |
    |   123 | 123  |     123 |  123   |
    |     1 | 1    |       1 |   1    |


Colspan(alpha status):

    |              |           Grouping          ||
    | First Header | Second Header | Third Header |
    | ------------ | :-----------: | -----------: |
    | Content      |         *Long Cell*         ||
    | Content      |    **Cell**   |         Cell |
    | New section  |      More     |         Data |
    | And more     |    And more   |              |
    | :---------------------------------------: |||


**RestructuredText**

    |    Name   | Age |
    +-----------+-----+
    | Anna      |  20 |
    | Alexander |  27 |

**Textile**


Alignment:

    |_.   Name  |_. Age |_. Custom Alignment Demo |
    | Anna      |    20 |<. left                  |
    | Alexander |    27 |>.                 right |
    | Misha     |    42 |=.         center        |
    |           |       |                         |

Colspan(alpha status):

    |\2. spans two cols   |
    | col 1    | col 2    |
   
Rowspan(alpha status):

    |/3. spans 3 rows | a |
    | b               |
    | c               |


Compound Textile table cell specifiers:

    |_\2.  spans two cols |
    |_<. col 1 |_>. col 2 |


Note: Formatting and work with textile tables with colspan and rowspan has alpha status. 



### Switch table syntax on the fly


Table Editor syntax detected by user settings and if it is not specified recognized automatically by view syntax. But you can change table syntax on the fly with command palette:

- Table Editor: Set table syntax 'Simple' for current view
- Table Editor: Set table syntax 'EmacsOrgMode' for current view
- Table Editor: Set table syntax 'Pandoc' for current view
- Table Editor: Set table syntax 'MultiMarkdown' for current view
- Table Editor: Set table syntax 'reStructuredText' for current view
- Table Editor: Set table syntax 'Textile' for current view

Above commands automatically enable table editor for current view.

### CJK support

Table Editor supports CJK languages. If you use CJK language you have to set 
monospaced fonts which supports CJK characters. For example next fonts work
on my windows computer 

- NSimSun
- FangSong
- SimHei


```javascript
"font_face": "NSimSun",
```


```
| column A | column B |     column C    |
+----------+----------+-----------------+
| 这家伙   | 真的     | 棒极了！        |
| この男   | 本当に   | 素晴らしいです! |
```

Size of CJK glyph in monospaced font equals 2 normal characters.

### Demo 

Press *ctrl+shift+p* to launch command palette and select *Table Editor: Show demo film in new scratch view*. It is integration test and demo at the same time. 


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

You can customize *Table Editor* by change settings. For do this you have to modify settings file (see http://docs.sublimetext.info/en/latest/customization/settings.html).

For apply changes for all files you can open user settings with menu "Preferences -> Settings - User". For apply changes for specific syntax you can open syntax settings with menu "Preferences -> Settings - More -> Syntax Specific - User". 

### Enable Table Editor

By default *Table Editor* is disabled. For enable *Table Editor* you have to set

```javascript
{
    "enable_table_editor": true
}
```

Usually you will enable *Table Editor* for specific syntax.
You can do this very easy if launch command palette by *ctrl+shift+p* and select 
*Table Editor: Enable for current syntax*. 


### Set Table Syntax

You can control table syntax with settings

```javascript
{
    // Set table syntax for Table Editor.
    // Valid options are: "Auto", "Simple", "EmacsOrgMode", "Pandoc", "MultiMarkdown",
    //                    "reStructuredText", "Textile"
    "table_editor_syntax": "Auto"
}
```

"Auto" settings detect table syntax by view syntax with next rules:

- Markdown, MultiMarkdown -> MultiMarkdown
- reStructuredText -> reStructuredText
- Textile -> Textile
- Other -> Simple


### Override Table Border For Simple Syntax

You can override table border style for Simple Syntax. Table editor supports next table border styles:

* simple: *|---|---|*
* emacs: org mode *|---+---|*
* grid: *+---+---+* 

```javascript
{
    // Override border style for Table Editor
    // Valid options are: "simple", "grid", "emacs"
    "table_editor_border_style": "simple"
}
```

### Override custom column alignment for Simple Syntax

This settings by default is enabled, but you can disable  it 

```javascript
{
    // If table_editor_custom_column_alignment is true, supports '<', '>', '#' column alignment
    "table_editor_custom_column_alignment": false
}
```

With this feature you can explicit set justification with format characters 

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



### Auto align number column to right

By default a number column aligns to right, if you do not like this you can disable it 


```javascript
{

    "table_editor_align_number_right": false
}
```

Also you can temporary switch this setting with command palette:

* Table Editor: Enable 'align_number_right' for current view
* Table Editor: Disable 'align_number_right' for current view


### Detect header column to center

By default a header column aligns to center, if you do not like this you can disable it 

```javascript
{

    "table_editor_detect_header": false
}
```

Also you can temporary switch this setting with command palette :

* Table Editor: Enable 'detect_header' for current view
* Table Editor: Disable 'detect_header' for current view

### Keep space left

Some time you do not like remove leading space from a data in a column, as in next
example


    | Unordered  List |   Order List  |
    |-----------------|---------------|
    | - item 1        | # item 1      |
    |   - subitem 1   |   # subitem 1 |
    |   - subitem 2   | # item 2      |
    | - item 2        |   # subitem 2 |
    |                 |               |


```javascript
{
    "table_editor_keep_space_left": true
}
```

Also you can temporary switch this setting with command palette:

* Table Editor: Enable 'keep_space_left' for current view
* Table Editor: Disable 'keep_space_left' for current view


### Intelligent Formating

Intelligent Formatting is an configuration option for table editor. 
Currently this option have effect only for textiles and multimarkdown tables. 
It is true by default for textile syntax. You can disable it if you want
```json
{
    "table_editor_intelligent_formatting":false
}
``` 

Let you have a table

    |_. Attribute Name |_. Required |_. Value Type |
    |                  |            |              |

and want a row spanning all 3 columns

    |_. Attribute Name |_. Required |_. Value Type |
    | \3. All Events                 |            |              |

after click tab table editor will format table as

    |_. Attribute Name |_. Required |_. Value Type |
    |\3. All Events                                |

Probably it is expected result and this result of Table Editor with 
"table_editor_intelligent_formatting":true.

But probably you expected

    |_. Attribute Name |_. Required |_. Value Type |   |   |
    |\3. All Events                                |   |   |

and this result of Table Editor with 
"table_editor_intelligent_formatting":false.

## Keybinding

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

        Insert single horizontal line below current row. 
        Doesn't make sense and doesn't supported for Textile syntax

**ctrl+k, =**

        Insert double horizontal line below current row. 
        Doesn't make sense and doesn't supported for Textile syntaxes


**ctrl+k, enter**

        Insert a horizontal line below current row, and move the cursor into the row below that line. 
        Doesn't make sense and doesn't supported for Textile syntaxes


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

Test environment

- Ubuntu 12.04 64bit on VirtualBox
- Windows 7 64bit
- OS X 10.8.4
