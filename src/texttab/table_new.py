"""
Basic text-based table classes
"""
import const
from const import FG_COLOURS, BG_COLOURS
from fields import Field


class BasicTable(object):
    def __init__(self, columns=None, border="single"):
        self.__col_width_calculated = False

        self.columns = columns
        self.num_columns = len(self.columns)
        self.width = self.calculate_table_width()
        self.generate_column_labels()
        self.rows = []

        if border not in const.AVAILABLE_BORDERS:
            exception_string = "Unknown border style: '" + border + "'"
            raise ValueError(exception_string)
        self.border_style = border
        self.border_symbols = const.border_symbols[self.border_style]

    def render(self):
        table_lines = []
        table_lines.append(self._gen_header_top())
        table_lines.append(self.generate_header_line())
        table_lines.append(self._gen_header_bottom())

        for row in self.rows:
            table_lines.append(self._gen_table_row(row))

        table_lines.append(self._gen_table_bottom())

        return table_lines

    def add_row(self, rowdata):
        """
        Provide data to fill in the columns.
        rowdata must be a list or a tuple so that ordering is guaranteed.
        """
        if not isinstance(rowdata, (type(tuple([])), type([]))):
            raise TypeError(
                "Row data can only be expressed as a tuple or list")

        if len(rowdata) < self.num_columns:
            raise ValueError(
                "Insufficient number of data items. "
                "Received {}, expected {}".format(
                    len(rowdata), self.num_columns))
        elif len(rowdata) > self.num_columns:
            raise ValueError(
                "Too many data items. "
                "Received {}, expected {}".format(
                    len(rowdata), self.num_columns))
        self.rows.append(rowdata)

    def calculate_column_widths(self):
        for col in self.columns:
            minimum_width = len(col['label'].strip()) + 2
            if "width" not in col.keys():  # Auto calculate min width
                width = minimum_width
                col['width'] = width
            else:
                if col['width'] < minimum_width:
                    col['width'] = minimum_width

        self.__col_width_calculated = True

    def generate_column_labels(self):
        for col in self.columns:
            generated_label = ""
            if "align" in col.keys():
                if col['align'].lower() in ("center", "centre"):
                    fmt_str = " {:^" + str(col['width'] - 2) + "s} "
                elif col['align'].lower() == "left":
                    fmt_str = " {:" + str(col['width'] - 2) + "s} "
                elif col['align'].lower() == "right":
                    fmt_str = " {:>" + str(col['width'] - 2) + "s} "
            else:
                fmt_str = " {:" + str(col['width'] - 2) + "s} "

            if "fg" in col.keys():
                generated_label = const.FG_COLOURS[col["fg"]]
            if "bg" in col.keys():
                generated_label = const.BG_COLOURS[col["bg"]]

            generated_label += fmt_str.format(col['label'])
            generated_label += "\033[0m"
            col['gen_label'] = generated_label

    def calculate_table_width(self):
        if not self.__col_width_calculated:
            self.calculate_column_widths()

        table_width = 0
        for col in self.columns:
            table_width += col['width']

        table_width += 2 + (self.num_columns - 1)
        return table_width

    def generate_header_line(self):
        line = self.border_symbols['VBAR']
        column_labels = [col['gen_label'] for col in self.columns]
        line += self.border_symbols["VBAR"].join(column_labels)
        line += self.border_symbols["VBAR"]
        return line

    def _gen_header_top(self):
        line = self.border_symbols["TOP_LEFT"]
        col_bars = [
            col['width'] * self.border_symbols["HBAR"] for col in self.columns
        ]
        line += self.border_symbols["TOP_TEE"].join(col_bars)
        line += self.border_symbols["TOP_RIGHT"]
        return line

    def _gen_header_bottom(self):
        line = self.border_symbols["LEFT_TEE"]
        col_bars = [
            col['width'] * self.border_symbols["HBAR"] for col in self.columns
        ]
        line += self.border_symbols["INTERSECT"].join(col_bars)
        line += self.border_symbols["RIGHT_TEE"]
        return line

    def _gen_table_bottom(self):
        line = self.border_symbols["BOTTOM_LEFT"]
        col_bars = [
            col['width'] * self.border_symbols["HBAR"] for col in self.columns
        ]
        line += self.border_symbols["BOTTOM_TEE"].join(col_bars)
        line += self.border_symbols["BOTTOM_RIGHT"]
        return line

    def _gen_table_row(self, rowdata):
        line = self.border_symbols["VBAR"]
        col_strings = []

        for col_index, col in enumerate(self.columns):
            fmt_str = self._get_column_format_string(col)
            col_string = self.format_column_value(
                col, rowdata[col_index], fmt_str)
            col_strings.append(col_string)
        line += self.border_symbols["VBAR"].join(col_strings)
        line += self.border_symbols["VBAR"]
        return line

    def format_column_value(self, col, rowdata, fmtstr):
        cell_field = Field.from_column(col, rowdata)
        ret_str = ""

        if "fg" in col.keys():
            ret_str += FG_COLOURS[col["fg"]]
        if "bg" in col.keys():
            ret_str += BG_COLOURS[col["bg"]]

        if 'formatter' in col.keys():
            value_str = col['formatter'].format(rowdata)
        else:
            value_str = str(rowdata)
            # value_str = str(cell_field)
            if len(value_str) > col['width'] - 2:
                value_str = value_str[:col['width'] - 5] + "..."
        ret_str += fmtstr.format(value_str)

        if "fg" in col.keys() or "bg" in col.keys():
            ret_str += "\033[0m"

        return ret_str

    def _get_column_format_string(self, col):
        if "align" not in col.keys() or col["align"] == "left":
            fmt_str = "{:" + str(col['width']) + "}"
        elif col["align"] == "right":
            fmt_str = "{:>" + str(col['width']) + "}"
        elif col["align"] in ("center", "centre"):
            fmt_str = "{:^" + str(col['width']) + "}"
        return fmt_str
