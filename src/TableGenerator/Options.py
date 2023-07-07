from enum import Enum


class Options:
    line_type = ["BLACK", "WHITE", "NONE"]  # Show separation lines in the table
    lines_width = [0.05, 0.3, 0.5, 1, 2.75]  # How many pixels should the separation-lines be?
    double_lines = [True, False]  # Should the separation-lines exist of two lines?
    font_size = [5, 8, 16]  # Font size of the text in the table
    rows_in_cell = [1, 2, 3]  # In a cell there can be multiple rows of text
    empty_values = [0, 0.001, 0.2, 0.3, 0.4, 0.5]  # How much % of the total cells in the table should be empty
    censor_bars = [0, 0.001, 0.2, 0.4, 0.6, 0.8]  # How much % of the total cells in the table should be censor bars
    vertical_headers = [True, False]  # Whether to make headers in the table vertical (else its horizontal)
    text_alignment = ["L", "C", "R", "X"]  # Text alignment within cells (L for left, C for Center, R for Right, X for random)
    text_underscore = [True, False]  # Whether to underscore the text in the table
    colored_uneven_rows = [True, False]  # Whether to color uneven rows in the table
    decorated_header = [True, False]  # Whether to color the table header
    row_amount = [2, 5, 10, 20]  # Number of rows in the table
    column_amount = [2, 5, 8, 10]  # Number of columns in the table

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                yield getattr(self, attr)

    def __to_dict__(self):
        options_dict = {}
        for attr_name in dir(self):
            if not attr_name.startswith("__") and not callable(getattr(self, attr_name)):
                options_dict[attr_name] = getattr(self, attr_name)
        return options_dict

    @property
    def __default__(self):
        return {
            OptionsENUM.LINE_TYPE.value: "BLACK",
            OptionsENUM.LINES_WIDTH.value: 0.1,
            OptionsENUM.DOUBLE_LINES.value: False,
            OptionsENUM.FONT_SIZE.value: 8,
            OptionsENUM.ROWS_IN_CELL.value: 1,
            OptionsENUM.EMPTY_VALUES.value: 0,
            OptionsENUM.CENSOR_BARS.value: 0,
            OptionsENUM.VERTICAL_HEADERS.value: False,
            OptionsENUM.TEXT_ALIGNMENT.value: 'L',
            OptionsENUM.TEXT_UNDERSCORE.value: False,
            OptionsENUM.COLORED_UNEVEN_ROWS.value: False,
            OptionsENUM.DECORATED_HEADER.value: False,
            OptionsENUM.ROW_AMOUNT.value: 5,
            OptionsENUM.COLUMN_AMOUNT.value: 4,
        }


class OptionsENUM(Enum):
    LINE_TYPE = 'line_type'                           # Should seperation lines be black, white, or none?
    LINES_WIDTH = 'lines_width'                       # How many pixels should the separation-lines be?
    DOUBLE_LINES = 'double_lines'                     # Should the separation-lines exist of two lines?
    FONT_SIZE = 'font_size'                           # Font size of the text in the table
    ROWS_IN_CELL = 'rows_in_cell'                     # In a cell there can be multiple rows of text
    EMPTY_VALUES = 'empty_values'                     # How much % of the total cells in the table should be empty
    CENSOR_BARS = 'censor_bars'                       # How much % of the total cells in the table should be censor bars
    VERTICAL_HEADERS = 'vertical_headers'             # Whether to make headers in the table vertical (else its horizontal)
    TEXT_ALIGNMENT = 'text_alignment'                 # Text alignment within cells (L for left, C for Center, R for Right, X for random)
    TEXT_UNDERSCORE = 'text_underscore'               # Whether to underscore the text in the table
    COLORED_UNEVEN_ROWS = 'colored_uneven_rows'       # Whether to color uneven rows in the table
    DECORATED_HEADER = 'decorated_header'             # Whether to decorate the table header, make it bold, show on pagebreak
    ROW_AMOUNT = 'row_amount'                         # Number of rows in the table
    COLUMN_AMOUNT = 'column_amount'                   # Number of columns in the table

