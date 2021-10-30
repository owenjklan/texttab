# texttab - Creating nice tables for text output

Note: References to this as creating "ASCII tables" might _technically_ be a
bit of a misnomer. ASCII might imply the long-used 7-bit (8-bits, with extensions)
character encoding. `texttab`, on the other hand, makes use of Unicode characters
to draw classic "line-drawing" and "box-characters", where appropriate.

Now that the pedantry is out of the way, let's move on to demonstrate how to
actually use this library to great effect.

## Basic example
To demonstrate the use of `texttab`, take a look at the `testprog` script in
the `examples/` directory:

### Imports
Getting started with `texttab` requires importing the `BasicTable` class, at
the very minimum. In the example, `AVAILABLE_BORDERS` has also been imported.
This is so that the program can demonstrate all possible border style options.

Note that `click` has been imported, simply because Click is an excellent
library. Adding familiarity with Click would never be a bad thing for even the
semi-serious Python programmers out there.
```python
#!/usr/bin/env python3
import click

from texttab.const import AVAILABLE_BORDERS
from texttab.table import BasicTable
```

### Custom Formatters
As far as tutorial sections and progression goes, it probably seems strange to
bring up customisation options so early. The simple fact is that we are following
the flow of the `testprog` source, explaining things as they are encountered.

The `TestFormatter` class is intended to demonstrate the basic expectations for
a custom formatter class (note that the base object is still the Python 
`object` class). It's functionality selects differing "format strings",
which are nothing more than pre-canned, ANSI Terminal control characters. This
allows the output in the table to have different colours, based on arbitrary
business logic.

```python
class TestFormatter(object):
    @classmethod
    def format(cls, value, col):
        format_string = "\033[0m"
        reset = False
        rv = int(value)
        if rv >= 10:
            format_string += "\033[5m"  # Blink
            format_string += "\033[1m"  # Bold
            format_string += "\033[32;47m"  # Green
            reset = True
        elif rv < 10 and rv > 1:
            format_string += "\033[34;47m"  # Blue??
            reset = True
        else:
            format_string += "\033[31;47m"  # Red
            reset = True
        return format_string, str(value), reset
```

The very last line of `TestFormatter`'s definition shows the expected values
that are required in the returned tuple. Format string is optional, but if not
used, then an empty string should be returned. Format strings will usually be
ANSI terminal control sequences, especially those for colour and attributes.
The returned format string value will be _rendered_ (ie: printed to the
terminal) but _does not count to the length of the value string_.

The value string is the actual string-representation for
what you want to appear in the table cell.

The last element of the tuple, `reset`, is a boolean and indicates whether an
ANSI "reset attributes" control sequence should be output.  This is usually
needed (ie: returned as `True`) if control sequences that manipulate colour or
other text attributes, were used in the returned format string.

### Column Specifications
Next in the example `testprog` source, comes the column definitions for the
table we are going to create. Hopefully, the keys for configuration options
are self-explanatory.

```python
example_columns = [
    {
        "label": "Name",
        "width": 25,
        "align": "left",
        "bg":    "white",
        "fg":    "black",
        "head_bg": "white",
        "head_fg": "blue",
    },
    {
        "label": "Email",
        "width": 32,
        "align": "centre",
        "bg":    "white",
        "fg":    "black",
        "head_bg": "white",
        "head_fg": "blue",
    },
    {
        "label": "Years-of-Service",
        "align": "right",
        "bg":    "white",
        "fg":    "black",
        "head_bg": "white",
        "head_fg": "blue",
        "formatter": TestFormatter,
    }
]
```

For names to use for colour options (`fg`, `bg`, `head_fg`, `head_bg`), look
in the `texttab.const` module. In particular, the `FG_COLOURS` and `BG_COLOURS`
dictionaries.

Of particular interest is the `formatter` key, in the last specification
dictionary. This value is the (unquoted!) name of a class that implements a
customer cell formatting in the resultant table.

### Example Data
This list contains tuples for example data. That's it. Each defined column will
require an entry in a row's tuple. Note that the data for a row doesn't have to
be a `tuple`. Lists are also valid. If very close attention is paid to the
middle row of data, then it can be seen that it is defined as a `list` literal,
not a `tuple` literal, like the rows to either side of it. A real program
probably wouldn't mix row sequence types like this. This was an explicit
demonstration to show that either `list` or `tuple` can be used for row data.

```python
example_data = [
    ("Owen Klan", "oklan@example.com", 1),
    ["Barry Badlow", "bbadlow@example.com", 13],
    ("Genevive Goodhigh Really-Long-Named", "ggoodhigh@example.com", 2),
]
```

### Command-line Options
All of the decorators that are applied to the `main` function are part of how
Click handles arguments and options to commands. A tutorial on Click is outside
the scope of this document. Just understand that all those decorators give us
our nice command-line options handling.

### Finally, creating and using a table
The `main()` function in our example simply creates a new `BasicTable` class,
one for each type of border style that's available. For each table, data is
added using the `add_row(<sequence>)`.

Once all the data rows have been added, the `render()` method can be called.
Note that `render()` returns a _list_ of lines.

### ... and the output?
Do note that the below output, despite being "pre-formatted", might have gaps
between the line-drawing elements for each row. This depends on the default
line-spacing used by your particular Markdown viewer, whether that is on Github
or a dedicated application.

Of course, colour and blinking output that is defined in the last column, will
also not be visible in this README.
```text
owen@pfhor:~/git/texttab$ examples/testprog
Simple test program, designed to demonstrate alignment of columns as well as border styles.

Border styles are available from 'const.AVAILABLE_BORDERS' list.

Table style: single
┌─────────────────────────┬────────────────────────────────┬──────────────────┐
│ Name                    │             Email              │ Years-of-Service │
├─────────────────────────┼────────────────────────────────┼──────────────────┤
│Owen Klan                │       oklan@example.com        │                 1│
│Barry Badlow             │      bbadlow@example.com       │                13│
│Genevive Goodhigh Re...  │     ggoodhigh@example.com      │                 2│
└─────────────────────────┴────────────────────────────────┴──────────────────┘

Table style: single-thick
┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Name                    ┃             Email              ┃ Years-of-Service ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━┫
┃Owen Klan                ┃       oklan@example.com        ┃                 1┃
┃Barry Badlow             ┃      bbadlow@example.com       ┃                13┃
┃Genevive Goodhigh Re...  ┃     ggoodhigh@example.com      ┃                 2┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━┛

Table style: single-rounded
╭─────────────────────────┬────────────────────────────────┬──────────────────╮
│ Name                    │             Email              │ Years-of-Service │
├─────────────────────────┼────────────────────────────────┼──────────────────┤
│Owen Klan                │       oklan@example.com        │                 1│
│Barry Badlow             │      bbadlow@example.com       │                13│
│Genevive Goodhigh Re...  │     ggoodhigh@example.com      │                 2│
╰─────────────────────────┴────────────────────────────────┴──────────────────╯

Table style: double
╔═════════════════════════╦════════════════════════════════╦══════════════════╗
║ Name                    ║             Email              ║ Years-of-Service ║
╠═════════════════════════╬════════════════════════════════╬══════════════════╣
║Owen Klan                ║       oklan@example.com        ║                 1║
║Barry Badlow             ║      bbadlow@example.com       ║                13║
║Genevive Goodhigh Re...  ║     ggoodhigh@example.com      ║                 2║
╚═════════════════════════╩════════════════════════════════╩══════════════════╝

Table style: pipe-joints
┏─────────────────────────┳────────────────────────────────┳──────────────────┓
│ Name                    │             Email              │ Years-of-Service │
┣─────────────────────────╋────────────────────────────────╋──────────────────┫
│Owen Klan                │       oklan@example.com        │                 1│
│Barry Badlow             │      bbadlow@example.com       │                13│
│Genevive Goodhigh Re...  │     ggoodhigh@example.com      │                 2│
┗─────────────────────────┻────────────────────────────────┻──────────────────┛
```