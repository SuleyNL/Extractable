import os

import pytest
from unittest.mock import patch

from src.extractable import Extractor
from src.extractable.Filetype import Filetype
from src.extractable.ModeManager import Mode
from src.extractable.Logger import setup_logger, CustomFormatter

# Ensure the logger is not configured when tests start
import logging

from tests.variables import empty_folder, table_pdf_file, table_png_file_standard

logging.getLogger('Extractor').handlers = []


@pytest.fixture(scope='function')
def before_and_after():
    try:
        os.mkdir(empty_folder)
    except OSError:
        pass

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


class TestTheTests:

    def test_1(self, before_and_after):
        print('cwd: ' + os.getcwd())
        assert os.path.isfile(table_pdf_file) is True


# Test setup_logger method
def test_setup_logger(before_and_after):
    # Create a logger with a custom formatter and check its configuration
    # Arrange

    logger = setup_logger()
    assert isinstance(logger, logging.Logger)
    assert len(logger.handlers) == 1
    assert isinstance(logger.handlers[0], logging.StreamHandler)
    assert isinstance(logger.handlers[0].formatter, CustomFormatter)
    assert logger.level == logging.DEBUG


# Test the main extract method
def test_extract(before_and_after):
    # Mock extract_using_TATR()
    # Arrange

    with patch('src.extractable.Extractor.extract_using_TATR') as mock_extract_using_TATR:
        mock_extract_using_TATR.return_value = None
        # Act
        Extractor.extract(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)

    # Assert
    # check if extract() correctly calls extract_using_TATR()
    mock_extract_using_TATR.assert_called_once_with(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)


# Define your test
# Test extract_using_TATR method
class Test_extract_using_TATR_methods:
    def test_extract_using_TATR_shouldCompilePipelineWhenInputPDF(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function aswell as the functions within the pipeline so that none will be executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj_class:  # Mock the DataObj class

            #mock_dataobj = mock_dataobj_class()
            pipeline = mock_compose_left(
                mock_table_detector,
                mock_structure_detector,
                mock_text_extractor,
                mock_dataobj_class.output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(mock_convert_to_image, pipeline)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_pdf_file

    def test_extract_using_TATR_shouldCompilePipelineWhenInputPNG(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function as well as the functions within the pipeline, so it's not executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.Dataobj.DataObj.output') as mock_data_obj_output, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj:  # Mock the DataObj class
            pipeline = mock_compose_left(
                mock_table_detector,
                mock_structure_detector,
                mock_text_extractor,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR(table_png_file_standard, empty_folder, Filetype.XML, Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(
            mock_table_detector,
            mock_structure_detector,
            mock_text_extractor,
            mock_data_obj_output)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_png_file_standard

        mock_convert_to_image.assert_not_called()

    def test_extract_using_TATR_table_only_shouldCompilePipelineWhenInputPDF(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function aswell as the functions within the pipeline so that none will be executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.Dataobj.DataObj.output') as mock_data_obj_output, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj:
            pipeline = mock_compose_left(
                mock_table_detector,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR_table_only(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(mock_convert_to_image, pipeline)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_pdf_file

        mock_structure_detector.assert_not_called()
        mock_text_extractor.assert_not_called()

    def test_extract_using_TATR_table_only_shouldCompilePipelineWhenInputPNG(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function as well as the functions within the pipeline, so it's not executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.Dataobj.DataObj.output') as mock_data_obj_output, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj:
            pipeline = mock_compose_left(
                mock_table_detector,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR_table_only(table_png_file_standard, empty_folder, Filetype.XML,
                                                    Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(
            mock_table_detector,
            mock_data_obj_output)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_png_file_standard

        mock_convert_to_image.assert_not_called()
        mock_structure_detector.assert_not_called()
        mock_text_extractor.assert_not_called()

    def test_extract_using_TATR_structure_only_shouldCompilePipelineWhenInputPDF(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function aswell as the functions within the pipeline so that none will be executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.Dataobj.DataObj.output') as mock_data_obj_output, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj:
            pipeline = mock_compose_left(
                mock_structure_detector,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR_structure_only(table_pdf_file, empty_folder, Filetype.XML, Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(mock_convert_to_image, pipeline)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_pdf_file

        mock_table_detector.assert_not_called()
        mock_text_extractor.assert_not_called()

    def test_extract_using_TATR_structure_only_shouldCompilePipelineWhenInputPNG(self, before_and_after):
        # Arrange
        # Mock the 'compose_left' function as well as the functions within the pipeline, so it's not executed, only called
        with \
                patch('src.extractable.Extractor.compose_left') as mock_compose_left, \
                patch('src.extractable.TableDetector.TableDetectorTATR.process') as mock_table_detector, \
                patch(
                    'src.extractable.StructureDetector.StructureRecognitionWithTATR.process') as mock_structure_detector, \
                patch('src.extractable.TextExtractor.PyPDF2Textport.process') as mock_text_extractor, \
                patch('src.extractable.Dataobj.DataObj.output') as mock_data_obj_output, \
                patch('src.extractable.PDFtoImageConvertor.ConvertUsingPDF2image.process') as mock_convert_to_image, \
                patch('src.extractable.Dataobj.DataObj') as mock_dataobj:
            pipeline = mock_compose_left(
                mock_structure_detector,
                mock_data_obj_output)

            # Act
            # Call the 'extract_using_TATR' function with some test parameters.
            # This will trigger the execution of the pipeline of functions.
            return_dataobj = Extractor.extract_using_TATR_structure_only(table_png_file_standard, empty_folder, Filetype.XML,
                                                        Mode.PERFORMANCE)

        # Assert
        # Check whether compose left has been called properly
        mock_compose_left.assert_called_with(
            mock_structure_detector,
            mock_data_obj_output)

        assert return_dataobj.output_filetype == Filetype.XML
        assert return_dataobj.output_file == empty_folder
        assert return_dataobj.mode == Mode.PERFORMANCE
        assert return_dataobj.input_file == table_png_file_standard

        mock_convert_to_image.assert_not_called()
        mock_table_detector.assert_not_called()
        mock_text_extractor.assert_not_called()
