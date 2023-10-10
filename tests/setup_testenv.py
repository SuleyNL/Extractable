
# Define a pytest fixture to check and set up the test environment
import os
import pytest


# Define a custom exception for test setup errors
from tests.variables import empty_folder, table_pdf_file


@pytest.fixture(scope="function")
def setup_test_environment():
    try:
        os.mkdir(empty_folder)
    except OSError:
        pass

    # Check that folder exists and that it is a folder
    if not os.path.exists(empty_folder) or not os.path.isdir(empty_folder):
        pytest.fail(f"The folder '{empty_folder}' does not exist or is not a directory.")

    # Check that input file exists
    if not os.path.exists(table_pdf_file):
        pytest.fail(f"The input file '{table_pdf_file}' does not exist.")

    # Ensure that the output folder starts empty
    for file_name in os.listdir(empty_folder):
        file_path = os.path.join(empty_folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

    yield  # This allows the test to run

    # Cleanup
    for file_name in os.listdir(empty_folder):
        file_path = os.path.join(empty_folder, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
