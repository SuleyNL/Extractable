import numpy
from fpdf import FPDF


def GeneratePDFTable(table_data: numpy.array, output_file: str, **options:dict):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font(family='FreeSans', style="", fname='fonts/FreeSans.ttf')
    pdf.add_font(family='FreeSans', style="B", fname='fonts/FreeSansBold.ttf')
    pdf.set_font('FreeSans', size=options['font_size'])

    '''
    #Iterating through each cell allows for more freedom
        with pdf.table() as table:
            for data_row in table_data:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
    '''


    with pdf.table(table_data) as table:
        pass

    # Add the table parameters to the PDF
    pdf.set_font("FreeSans", size=8)
    pdf.cell(0, 5, "With Lines: " + str(options['with_lines']))
    pdf.ln()
    pdf.cell(0, 5, "Lines Width: " + str(options['lines_width']))
    pdf.ln()
    pdf.cell(0, 5, "Double Lines: " + str(options['double_lines']))
    pdf.ln()
    pdf.cell(0, 5, "Font Size: " + str(options['font_size']))
    pdf.ln()
    pdf.cell(0, 5, "Rows of Text in Cells: " + str(options['rows_in_cell']))
    pdf.ln()
    pdf.cell(0, 5, "Empty Values: " + str(options['empty_values']))
    pdf.ln()
    pdf.cell(0, 5, "Censor Bars: " + str(options['censor_bars']))
    pdf.ln()
    pdf.cell(0, 5, "Vertical Headers: " + str(options['vertical_headers']))
    pdf.ln()
    pdf.cell(0, 5, "Text Alignment: " + options['text_alignment'])
    pdf.ln()
    pdf.cell(0, 5, "Text Underscore: " + str(options['text_underscore']))
    pdf.ln()
    pdf.cell(0, 5, "Colored Uneven Rows: " + str(options['colored_uneven_rows']))
    pdf.ln()
    pdf.cell(0, 5, "Colored Header: " + str(options['colored_header']))
    pdf.ln()
    pdf.cell(0, 5, "Column Amount: " + str(options['column_amount']))
    pdf.ln()
    pdf.cell(0, 5, "Row Amount: " + str(options['row_amount']))

    pdf.output(output_file)

