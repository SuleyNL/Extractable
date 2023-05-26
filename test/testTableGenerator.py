import TableGenerator

#startProcess('tables/')

from TableGenerator import *
options = Options().__default__

TableGenerator.GenerateOneTable('tables/default.pdf', options)

'''
options = Options()
options_example = options.__default__
options_example[OptionsENUM.VERTICAL_HEADERS.value] = True
options_example[OptionsENUM.LINE_TYPE.value] = "BLACK"
options_example[OptionsENUM.TEXT_ALIGNMENT.value] = "C"
options_example[OptionsENUM.COLORED_UNEVEN_ROWS.value] = True
options_example[OptionsENUM.DECORATED_HEADER.value] = True
options_example[OptionsENUM.CENSOR_BARS.value] = 0.2
options_example[OptionsENUM.TEXT_UNDERSCORE.value] = True
options_example[OptionsENUM.ROW_AMOUNT.value] = 10
options_example[OptionsENUM.LINES_WIDTH.value] = 1
GenerateOneTable('tables/default.pdf', options_example)
'''





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
options_example = options
#GeneratePDFTable(table_data, 'tables/debug.pdf', options_example)



options_example[OptionsENUM.DECORATED_HEADER.value] = True
options_example[OptionsENUM.VERTICAL_HEADERS.value] = True
#options_example[OptionsENUM.FONT_SIZE.value] = 20

options_example = options
options_example[OptionsENUM.LINE_TYPE.value] = "NONE"
options_example[OptionsENUM.TEXT_ALIGNMENT.value] = "C"
options_example[OptionsENUM.COLORED_UNEVEN_ROWS.value] = True
options_example[OptionsENUM.DECORATED_HEADER.value] = True
options_example[OptionsENUM.CENSOR_BARS.value] = 0.001
options_example[OptionsENUM.TEXT_UNDERSCORE.value] = True
options_example[OptionsENUM.ROW_AMOUNT.value] = 4
options_example[OptionsENUM.LINES_WIDTH.value] = 3
#GenerateOneTable('tables/testingnewfunctions', options_example)

