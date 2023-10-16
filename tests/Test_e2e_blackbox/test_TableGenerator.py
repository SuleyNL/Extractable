import os
import time
import warnings

import pytest

from src import TableGenerator as TableGenerator
from src.TableGenerator import Options, OptionsENUM
from tests.variables import default_pdf_file, default_pdf_dir
#  startProcess('files/tables/')

options = Options().__default__


# Define the test case
def test_TableGenerator_happyflow():
    start_time = time.time()
    try:
        # Act
        TableGenerator.GenerateOneTable(default_pdf_file, options)
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {str(e)}")
    finally:
        end_time = time.time()
        execution_time = end_time - start_time
        # Warn if execution time is greater than 10 seconds
        if execution_time > 10:
            warning_message = f"Performance warning: Execution time exceeded 10 seconds: ({execution_time:.2f} seconds)"
            warnings.warn(warning_message, UserWarning)
        # Fail the test if execution time is greater than 20 seconds
        if execution_time > 20:
            pytest.fail(f"Test failed: Execution time exceeded 20 seconds ({execution_time:.2f} seconds)")
    # Assert
    assert os.listdir(default_pdf_dir)  # Check that the output folder is now filled




# TableGenerator.startProcess('test/generated_tables')

#options[OptionsENUM.LINES_WIDTH.value] = 5
#options[OptionsENUM.VERTICAL_HEADERS.value] = True
#options[OptionsENUM.DECORATED_HEADER.value] = True
#options[OptionsENUM.VERTICAL_HEADERS.value] = True
#options[OptionsENUM.FONT_SIZE.value] = 20
#options[OptionsENUM.LINE_TYPE.value] = "NONE"
#options[OptionsENUM.TEXT_ALIGNMENT.value] = "C"
#options[OptionsENUM.COLORED_UNEVEN_ROWS.value] = True
#options[OptionsENUM.DECORATED_HEADER.value] = True
#options[OptionsENUM.CENSOR_BARS.value] = 0.001
#options[OptionsENUM.TEXT_UNDERSCORE.value] = True
#options[OptionsENUM.ROW_AMOUNT.value] = 4
#options[OptionsENUM.LINES_WIDTH.value] = 3
















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
# GeneratePDFTable(table_data, 'tables/debug.pdf', options_example)



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
#  GenerateOneTable('tables/testingnewfunctions', options_example)
'''

