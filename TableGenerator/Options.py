from enum import Enum


class Options:
    with_lines = [True, False]
    lines_width = [1, 3, 5]
    double_lines = [True, False]
    font_size = [5, 8, 16]
    rows_in_cell = [1, 2, 3]
    empty_values = [0, 0.2, 0.4, 0.6, 0.8, 1]
    censor_bars = [0, 0.2, 0.4, 0.6, 0.8, 1]
    vertical_headers = [True, False]
    text_alignment = ["L", "C", "R", "X"]
    text_underscore = [True, False]
    colored_uneven_rows = [True, False]
    colored_header = [True, False]
    row_amount = [2, 4, 6, 8, 10]
    column_amount = [2, 4, 6, 8, 10]

    def __iter__(self):
        for attr in dir(self):
            if not attr.startswith("__"):
                yield getattr(self, attr)

    @property
    def __default__(self):
        return {
            "with_lines": True,
            "lines_width": 1,
            "double_lines": False,
            "font_size": 8,
            "rows_in_cell": 1,
            "empty_values": 0,
            "censor_bars": 0,
            "vertical_headers": False,
            "text_alignment": "L",
            "text_underscore": False,
            "colored_uneven_rows": False,
            "colored_header": False,
            "column_amount": 4,
            "row_amount": 5,
        }


class OptionsENUM(Enum):
    WITH_LINES = 'with_lines'                         # Show separation lines in the table
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
    COLORED_HEADER = 'colored_header'                 # Whether to color the table header
    ROW_AMOUNT = 'row_amount'                         # Number of rows in the table
    COLUMN_AMOUNT = 'column_amount'                   # Number of columns in the table
