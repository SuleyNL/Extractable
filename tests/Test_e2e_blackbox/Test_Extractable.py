import time
from src.Extractable import *
from src.Extractable import Extractor
from tests.setup_testenv import *


# Define the test case
def test_Extractable_happyflow(setup_test_environment):
    try:
        # Act
        start_time = time.time()
        Extractor.extract_using_TATR(table_pdf_file, empty_folder, mode=Mode.PERFORMANCE)
        end_time = time.time()

        # Assert
        execution_time = end_time - start_time
        assert execution_time < 30  # Ensure execution time is within an acceptable range
        assert os.listdir(empty_folder)  # Check that the output folder is now filled

    except TestSetupError as e:
        pytest.fail(str(e))

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
