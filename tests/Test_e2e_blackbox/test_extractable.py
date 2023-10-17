import os
import time
import warnings
import platform

import pytest

from src.extractable.ModeManager import Mode
from src.extractable import Extractor
from tests.setup_testenv import setup_test_environment as setup_test_environment

# Define the test case
import tests.variables as variables


def test_Extractable_happyflow(setup_test_environment):
    try:
        # Act
        start_time = time.time()
        Extractor.extract_using_TATR(variables.table_pdf_file, variables.empty_folder, mode=Mode.PERFORMANCE)
        end_time = time.time()

        # Assert
        execution_time = end_time - start_time

        assert os.listdir(variables.empty_folder)  # Check that the output folder is now filled

        # Warn if execution time is greater than 10 seconds
        if execution_time > 20:
            warning_message = f"Performance warning: Execution time exceeded 20 seconds: ({execution_time:.2f} seconds)"
            warnings.warn(warning_message, UserWarning)
        # Fail the test if execution time is greater than 20 seconds
        if execution_time > 35 and platform.system() != "Darwin":
            pytest.fail(f"Test failed: Execution time exceeded 35 seconds ({execution_time:.2f} seconds)")
        elif platform.system() == "Darwin":
            warning_message = f"Performance warning: Execution time is not being limited for MacOS due to " \
                              f"unreliable services of the github runner. Time: ({execution_time:.2f} seconds)"
            warnings.warn(warning_message, UserWarning)

    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {str(e)}")

'''
with pytest.raises(ExpectedException):
    # Code that should raise the expected exception
    Extractor.extract_using_TATR(invalid_table_pdf_file, empty_folder, mode=Mode.PERFORMANCE)
'''

# AFTER EACH
# Iterate through all files in folder and delete each file
# file_list = os.listdir(empty_folder)
# for file_name in file_list:
#    file_path = os.path.join(empty_folder, file_name)
#    if os.path.isfile(file_path):
#        os.remove(file_path)


# TEST NOT YET WORKING PDFS
# Prob wrong PPI
# Extractor.extract('src/test/files/error_pdfs/no_rows/1.pdf', 'src/test/files/error_pdfs/no_rows/1.pdf', mode=Mode.PRESENTATION)
# Low accuracy cols & rows
# Extractor.extract('src/test/files/error_pdfs/no_text/1.pdf', 'src/test/files/error_pdfs/no_text/1.pdf', mode=Mode.PRESENTATION)
# Detects rotated tables but cant parse them into columns and rows
# Extractor.extract('src/test/files/error_pdfs/no_text/2.pdf', 'src/test/files/error_pdfs/no_text/2.pdf', mode=Mode.PRESENTATION)
# Multiple overlapping tables, and horizontal pages
# Extractor.extract('src/test/files/error_pdfs/some_error/Data Fact Sheet - 2022 Microsoft Sustainability Report.pdf', 'src/test/files/error_pdfs/some_error/Data Fact Sheet - 2022 Microsoft Sustainability Report.pdf', mode=Mode.PRESENTATION)
