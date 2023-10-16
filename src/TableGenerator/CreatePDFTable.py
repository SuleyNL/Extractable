import os

from src.TableGenerator.Options import OptionsENUM

import random
import math
from src.fpdf.fonts import FontFace

import numpy
from src.fpdf import FPDF
from src import fpdf


def GeneratePDFTable(table_data: numpy.array, output_file: str, options: dict):
    pdf = FPDF(unit="pt")
    pdf.add_page()

    fonts_path = os.path.join(os.path.dirname(__file__), "fonts")
    font1 = os.path.join(fonts_path, "FreeSans.ttf")
    font2 = os.path.join(fonts_path, "FreeSansBold.ttf")

    pdf.add_font(family='FreeSans', style="", fname=font1)
    pdf.add_font(family='FreeSans', style="B", fname=font2)
    pdf.set_font('FreeSans', size=options['font_size'])

    # TABLE COLOR
    table_color_option = (255, 255, 255)
    #table_color_option = (random.randint(80, 250), random.randint(80, 250), random.randint(80, 250))

    # TABLE WIDTH
    table_width_option = 538.5870866141731
    table_width_option = None

    #table_width_option = (random.randint(150, 538))

    # TEXT_UNDERLINE
    text_style = FontFace()
    if options[OptionsENUM.TEXT_UNDERSCORE.value]:
        text_style = FontFace(emphasis=fpdf.enums.TextEmphasis.U.value)

    # BORDERS
    borders_layout_option = None
    borders_color = (0, 0, 0)

    if options[OptionsENUM.LINE_TYPE.value] == "NONE":
        borders_layout_option = fpdf.enums.TableBordersLayout.NONE
        borders_color = (0, 0, 0)
    elif options[OptionsENUM.LINE_TYPE.value] == "BLACK":
        borders_color = (0, 0, 0)
        borders_layout_option = fpdf.enums.TableBordersLayout.ALL
    elif options[OptionsENUM.LINE_TYPE.value] == "WHITE":
        borders_color = (255, 255, 255)
        borders_layout_option = fpdf.enums.TableBordersLayout.ALL

    # COLORED_UNEVEN_ROWS
    cell_fill_mode_option = None
    if options[OptionsENUM.COLORED_UNEVEN_ROWS.value]:
        cell_fill_mode_option = fpdf.enums.TableCellFillMode.ROWS
    else:
        cell_fill_mode_option = fpdf.enums.TableCellFillMode.NONE

    # TEXT_ALIGNMENT
    text_align_option = None
    if options[OptionsENUM.TEXT_ALIGNMENT.value] == "L":
        text_align_option = fpdf.enums.Align.L
    elif options[OptionsENUM.TEXT_ALIGNMENT.value] == "C":
        text_align_option = fpdf.enums.Align.C
    elif options[OptionsENUM.TEXT_ALIGNMENT.value] == "R":
        text_align_option = fpdf.enums.Align.R
    elif options[OptionsENUM.TEXT_ALIGNMENT.value] == "X":
        # TODO: random text alignment per cell
        pass

    # DECORATED_HEADERS
    first_row_as_headings_option = options[OptionsENUM.DECORATED_HEADER.value]
    if options[OptionsENUM.DECORATED_HEADER.value] or options[OptionsENUM.COLORED_UNEVEN_ROWS.value]:
        cell_fill_color_option = (random.randint(80, 250), random.randint(80, 250), random.randint(80, 250))
    else:
        cell_fill_color_option = table_color_option

    # VERTICAL_HEADERS
    vertical_headers_option = options[OptionsENUM.VERTICAL_HEADERS.value]

    num_cells = sum(len(row) for row in table_data)

    # EMPTY_CELLS
    num_empty_cells = math.ceil(num_cells * options[OptionsENUM.EMPTY_VALUES.value])
    # Create a list of cell indices to empty
    empty_indices = random.sample(range(num_cells), num_empty_cells)

    # CENSOR_BARS
    num_censor_cells = math.ceil(num_cells * options[
        OptionsENUM.CENSOR_BARS.value])  # used math.ceil to make sure at least one cell is merged if value > 0
    # Create a list of cell indices to censor
    censor_indices = random.sample(range(num_cells), num_censor_cells)

    '''
    # MERGED_CELLS - # unused but works
    #num_merge_cells = math.ceil(num_cells * options[OptionsENUM.MERGED_CELLS.value])
    num_merge_cells = math.ceil(num_cells * 0.1)
    # Create a list of cell indices to merge
    merge_indices = random.sample(range(num_cells), num_merge_cells)
    '''
    with pdf.table(
            width=table_width_option,
            borders_layout=borders_layout_option,
            first_row_as_headings=first_row_as_headings_option,
            text_align=text_align_option,
            output_file=output_file,
            vertical_headers=vertical_headers_option
    ) as table:

        cell_id = 0
        row_id = 0
        pdf.set_line_width(options[OptionsENUM.LINES_WIDTH.value])
        pdf.set_draw_color(borders_color)
        # while i < len(table_data):
        for data_row in table_data:
            # data_row = table_data[i]
            row = table.row()
            column_id = 0
            # while j < len(data_row):
            colspan = 1
            for datum in data_row:
                '''
                #part of merge_cells functionality unused but works

                #skip the loop if the previous cell has been merged
                if colspan >= 2:
                    colspan = colspan-1
                    continue
                if cell_id in merge_indices:
                    colspan = 2
                '''

                '''
                #color each uneven column - #unused but works
                if column_id%2 == 1:
                    pdf.set_fill_color(220,200,180)
                '''

                # color each uneven row
                if row_id % 2 == 1:
                    text_style = FontFace(emphasis=text_style.emphasis, fill_color=cell_fill_color_option)
                else:
                    text_style = FontFace(emphasis=text_style.emphasis, fill_color=(table_color_option))

                if cell_id in censor_indices:
                    text_style = FontFace(emphasis=text_style.emphasis, fill_color=(10, 10, 10))
                    datum = ""

                if cell_id in empty_indices:
                    datum = ""

                with pdf.rotation(angle=100):
                    row.cell(datum, colspan=colspan, style=text_style)
                    cell_id += 1
                    column_id += colspan

            row_id += 1

    # add all options as text in pdf
    pdf.set_font("FreeSans", size=8)
    pdf.ln(h=28)

    for key, value in options.items():
        pdf.cell(0, 14, f"{key.title().replace('_', ' ')}: {str(value)}")
        pdf.ln(h=28)

    '''
    # useful for debugging purposes
    pdf.cell(0, 14, f"{'x'}: {str(pdf.get_x())}")
    pdf.ln()
    pdf.cell(0, 14, f"{'y'}: {str(pdf.get_y())}")
    '''

    pdf.output(output_file)
