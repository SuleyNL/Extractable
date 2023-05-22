from TableGenerator import *
import numpy as np

from fpdf.table import Table

'''
options = Options()

print(options.font_size)

print(options.__dict__)

# Example usage
for option in options:
    print(option)

'''

#startProcess('tables/')
options = Options()


# Define the text values
table_data = np.array([
    ["OOOOO3LINE OOOOO3LINE OOOOO3LINE OOOOO3LINE OOOOO3LINE OOOOO3LINE OOOOO3LINE", "i", "How", "Are", "Youuuuuu"],
    ["OOOOO1LINE", "i", "How", "Are", "Youuuuu"],
    ["OOOOO2LINE OOOOO2LINE", "i", "How", "Are", "Youuuuuu"],
    ["I", "i", "Doing", "Great", "Todayyyy"],
    ["Python", "i", "a", "Powerful", "Languagee"],
    ["NumPy", "i", "Efficient", "Array", "Operationss"],
    ["Let's", "i", "the", "Array", "Worldcc"]
])
options_example = options.__default__

#fpdf = FPDF()
#table = Table(fpdf=fpdf, rows=table_data)
#table.render()

options_example[OptionsENUM.DECORATED_HEADER.value] = True
options_example[OptionsENUM.VERTICAL_HEADERS.value] = True
#options_example[OptionsENUM.FONT_SIZE.value] = 20

#GenerateOneTable('tables/default.pdf', options_example)
GeneratePDFTable(table_data, 'tables/debug.pdf', options_example)

options_example = options.__default__
options_example[OptionsENUM.LINE_TYPE.value] = "NONE"
options_example[OptionsENUM.TEXT_ALIGNMENT.value] = "C"
options_example[OptionsENUM.COLORED_UNEVEN_ROWS.value] = True
options_example[OptionsENUM.DECORATED_HEADER.value] = True
options_example[OptionsENUM.CENSOR_BARS.value] = 0.001
options_example[OptionsENUM.TEXT_UNDERSCORE.value] = True
options_example[OptionsENUM.ROW_AMOUNT.value] = 4
options_example[OptionsENUM.LINES_WIDTH.value] = 3


#GenerateOneTable('tables/testingnewfunctions', options_example)

