import os
import sys

import pytest
from unittest.mock import patch, Mock

# Ensure the logger is not configured when tests start
from Extractable import setup_logger, CustomFormatter, Logger, extract, Filetype, Mode, Extractor, ConvertUsingPDF2image

import logging

# Ensure the logger is not configured when tests start
logging.getLogger('Extractor').handlers = []

# Configure directories
table_pdf_file = 'test_files/files/tables/WNT1.pdf'
table_png_file_standard = 'test_files/files/tables/WNT-verantwoording2.png'
table_png_file_complex = 'test_files/files/tables/WNT-Verantwoording_2kolommen_in1.png'
empty_folder = 'test_files/files/empty_folder'
temp_dir = 'test_files/files/fake_temp_dir'


class TestTheTests:

    def test_1(self, before_and_after):
        print('cwd: ' + os.getcwd())
        assert os.path.isfile(table_pdf_file) is True


@pytest.fixture(scope='function')
def before_and_after():
    # Check if the empty folder is empty and if it stays empty
    # BEFORE EACH
    exists = os.path.exists(empty_folder) and os.path.isdir(empty_folder)
    is_empty = not os.listdir(empty_folder)

    assert exists is True
    assert is_empty is True
    # ------
    yield None  # This is the wrapped function itself
    # ------
    exists = os.path.exists(empty_folder) and os.path.isdir(empty_folder)
    is_empty = not os.listdir(empty_folder)

    assert exists is True
    assert is_empty is True

    # AFTER EACH
    # Iterate through all files in folder and delete each file
    # file_list = os.listdir(empty_folder)
    # for file_name in file_list:
    #    file_path = os.path.join(empty_folder, file_name)
    #    if os.path.isfile(file_path):
    #        os.remove(file_path)


# Mock logger for testing
@pytest.fixture
def mock_logger():
    logger = setup_logger()
    return logger





# Define your test
# Test ConvertUsingPDF2image class
class Test_ConvertUsingPDF2images:
    def test_process(self): ...

    def test_save_img_to_temp(self):
        # TODO
        # Arrange
        with \
                patch('Extractable.Extractor.compose_left') as mock_compose_left, \
                patch('Extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch('Extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('Extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('Extractable.DataObj.output') as mock_data_obj_output, \
                patch('Extractable.Extractor.DataObj') as mock_dataobj:
            mock_dataobj.input_file = Mock()
            mock_dataobj.input_file.return_value = table_png_file_standard
            mock_dataobj.temp_dir = Mock()
            mock_dataobj.temp_dir.return_value = temp_dir

            # Act
            # TODO:
            # ConvertUsingPDF2image.save_img_to_temp(mock_dataobj, mock_logger, image, 1, path_to_images)

        # Assert

    def test_install_popler(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function aswell as the functions within the pipeline so that none will be executed, only called
        with \
                patch('Extractable.Extractor.compose_left') as mock_compose_left, \
                patch('Extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch('Extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('Extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('Extractable.DataObj.output') as mock_data_obj_output, \
                patch('Extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('Extractable.Extractor.DataObj') as mock_dataobj:
            pipeline = mock_compose_left(
                mock_table_detector,
                mock_structure_detector,
                mock_text_extractor,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            Extractor.extract_using_TATR(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(mock_convert_to_image, pipeline)
        mock_dataobj.assert_called_once_with({}, input_file=table_pdf_file, output_dir=empty_folder,
                                             output_filetype=Filetype.XML, mode=Mode.PERFORMANCE)
        pipeline.assert_called_once_with(mock_dataobj())
