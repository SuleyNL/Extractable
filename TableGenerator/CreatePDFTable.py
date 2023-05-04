import numpy
from fpdf import FPDF
import fpdf

from TableGenerator import *
from TableGenerator.Options import OptionsENUM

import random
import math


def GeneratePDFTable(table_data: numpy.array, output_file: str, options: dict):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font(family='FreeSans', style="", fname='fonts/FreeSans.ttf')
    pdf.add_font(family='FreeSans', style="B", fname='fonts/FreeSansBold.ttf')
    pdf.set_font('FreeSans', size=options['font_size'])

    borders_layout_option = None
    if options[OptionsENUM.WITH_LINES.value]:
        borders_layout_option = fpdf.enums.TableBordersLayout.ALL
    else:
        borders_layout_option = fpdf.enums.TableBordersLayout.NONE

    cell_fill_mode_option = None
    if options[OptionsENUM.COLORED_UNEVEN_ROWS.value]:
        cell_fill_mode_option = fpdf.enums.TableCellFillMode.ROWS
    else:
        cell_fill_mode_option = fpdf.enums.TableCellFillMode.NONE

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

    cell_fill_color_option = None
    if options[OptionsENUM.CENSOR_BARS.value]:
        # TODO: cell_fill_color_option = 1
        pass

    if options[OptionsENUM.COLORED_HEADER.value] or options[OptionsENUM.COLORED_UNEVEN_ROWS.value]:
        cell_fill_color_option = 200

    first_row_as_headings_option = options[OptionsENUM.COLORED_HEADER.value]

    num_cells = sum(len(row) for row in table_data)

    # CENSOR_BARS
    #num_censor_cells = max(round(num_cells * options[OptionsENUM.CENSOR_BARS.value]), 1) # Make sure at least one cell is merged
    num_censor_cells = max(round(num_cells * 0.2), 1) # Make sure at least one cell is merged

    # Create a list of cell indices to censor
    censor_indices = random.sample(range(num_cells), num_censor_cells)

    #MERGE CELLS
    #num_merge_cells = round(num_cells * options[OptionsENUM.EMPTY_VALUES.value])
    num_merge_cells = math.ceil(num_cells * 0.0)


    # Create a list of cell indices to merge
    merge_indices = random.sample(range(num_cells), num_merge_cells)

    with pdf.table(
                   borders_layout=borders_layout_option,
                   cell_fill_mode=cell_fill_mode_option,
                   first_row_as_headings=first_row_as_headings_option,
                   text_align=text_align_option,
                   cell_fill_color=100
                   ) as table:

        censor_index_set = set(censor_indices)
        merge_index_set = set(merge_indices)
        cell_id = 0
        i = 0
        
        #while i < len(table_data):
        for data_row in table_data:
            #data_row = table_data[i]
            row = table.row()
            j = 0
            #while j < len(data_row):
            for datum in data_row:
                colspan = 1
                pdf.set_fill_color(255,255,255)

                if cell_id in censor_index_set:
                    pdf.set_fill_color(10, 10, 20)
                    pass

                if cell_id in merge_index_set:
                    colspan = 2
                    pass

                datum = data_row[j]
                row.cell(datum, colspan=colspan)

                cell_id += 1
                j += colspan
            i+=1


        pass
    pdf.ln(h=10)


    # add all options as text in pdf
    pdf.set_font("FreeSans", size=8)
    pdf.ln(h=10)

    for key, value in options.items():
        pdf.cell(0, 5, f"{key.title().replace('_', ' ')}: {str(value)}")
        pdf.ln()

    pdf.output(output_file)
