"""
Unit tests for texttab basic functionality
"""
import pytest

from texttab.const import ANSI_SEQ_RESET, FG_COLOURS, BG_COLOURS
from texttab.table import BasicTable


# test_header_minimum_width
@pytest.mark.parametrize(
    "test_columns, expected_width",
    [
        ##################
        ([
            {"label": "Column 1", },
            {"label": "Value", },
        ], 20),
        ##################
        ([
            {
                "label": "Column 2",
                "width": 14,
            },
            {
                "label": "Value",
            }
        ], 24),
        ##################
        ([
            {
                "label": "Column 3",
                "width": 14,
            },
            {
                "label": "Value",
                "width": 10,
            }
        ], 27),
    ])
def test_header_minimum_width(test_columns, expected_width):
    """
    Minimum width (ie: no second field given in tuple) will be:
      Tw + 2N + (N-1) + 2
      Tw = Text width
      2N = Number of columns * 2 (for text spacing)
      +2 = constant for left and right edges
    """
    bt = BasicTable(columns=test_columns)
    assert bt.width == expected_width


@pytest.mark.parametrize(
    "test_columns, expected", [
        (
            [  # Testing centre alignment
                {
                    "label": "Column 3",
                    "width": 14,
                    "align": "center",
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "center"
                }
            ],
            u"\u2502   Column 3   \u2502  Value   \u2502"
        ),
        ##################
        (
            [  # Testing centre alignment, mixed spellings, both valid
                {
                    "label": "Column 3",
                    "width": 14,
                    "align": "centre",
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "center"
                }
            ],
            u"\u2502   Column 3   \u2502  Value   \u2502"
        ),
        ##################
        (
            [  # Testing right alignment
                {
                    "label": "Column 3",
                    "width": 14,
                    "align": "right",
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "right"
                }
            ],
            u"\u2502     Column 3 \u2502    Value \u2502"
        ),
        ##################
        (
            [  # Testing right alignment, mixed case for alignment values
                {
                    "label": "Column 3",
                    "width": 14,
                    "align": "RIGHT",
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "rIGHt"
                }
            ],
            u"\u2502     Column 3 \u2502    Value \u2502"
        )])
def test_header_label_alignments(test_columns, expected):
    bt = BasicTable(columns=test_columns)
    assert bt.generate_header_line() == expected


def test_minimum_width_autocorrects():
    """
    Making sure that if a width is specified that less than the text length
    of the label given, that the minimum width is calculated appropriately
    """
    test_columns = [
        {
            "label": "Column 3",
            "width": 4,
        },
        {
            "label": "Value",
            "width": 4,
        }
    ]
    bt = BasicTable(columns=test_columns)

    assert bt.width == 20


def test_data_row_min_fields_required():
    test_columns = [
        {"label": "Col 1"},
        {"label": "Column 2"},
        {"label": "Value"},
    ]

    test_data = ("foo", "bar",)
    bt = BasicTable(columns=test_columns)

    with pytest.raises(ValueError):
        bt.add_row(test_data)


def test_data_row_suitable_type_given():
    test_columns = [
        {"label": "Col 1"},
        {"label": "Column 2"},
        {"label": "Value"},
    ]

    test_data = "I am a string, I should be a list or tuple"
    bt = BasicTable(columns=test_columns)

    with pytest.raises(TypeError):
        bt.add_row(test_data)


@pytest.mark.parametrize(
    "test_columns, expected", [
        (
            [  # Testing fg colour adds FG colour and reset sequence on column label
                {
                    "label": "Col 3",
                    "width": 10,
                    "align": "center",
                    "fg": "blue"
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "center"
                }
            ],
            u"\u2502" + FG_COLOURS["blue"] + "  Col 3   " + ANSI_SEQ_RESET + "\u2502  Value   \u2502"
        ),
        ##################
        (
            [  # Test FG & BG adds both sequences, FG colour first, and adds reset to end of label text
                {
                    "label": "Column 3",
                    "width": 14,
                    "align": "centre",
                    "fg": "yellow",
                    "bg": "blue"
                },
                {
                    "label": "Value",
                    "width": 10,
                    "align": "center"
                }
            ],
            u"\u2502" + FG_COLOURS["yellow"] + BG_COLOURS["blue"] + "   Column 3   " + ANSI_SEQ_RESET + "\u2502  Value   \u2502"
        )
    ])
def test_header_label_colour_and_reset_sequences(test_columns, expected):
    """
    Ensure that the ANSI reset sequence is added to header label text,
    but only if a colour attribute was used, FG or BG. We also need to
    test the colour sequences appear, of course. The FG sequence will
    appear before the BG.

    Also add to our test parameters two consecutive columns of the
    same colour, to ensure the reset chars are still present.

    Minimum width (ie: no second field given in tuple) will be:
      Tw + 2N + (N-1) + 2
      Tw = Text width
      2N = Number of columns * 2 (for text spacing)
      +2 = constant for left and right edges
    """
    bt = BasicTable(columns=test_columns)
    assert bt.generate_header_line() == expected

