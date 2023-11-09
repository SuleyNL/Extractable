import os
import tempfile
import time

import PIL.Image as Image
import pytest
from unittest.mock import patch
import xml.etree.ElementTree as ET
import json

import src.extractable.Datatypes.Table as Table
import src.extractable as extractable
from src.extractable import Extractor
from src.extractable.Filetype import Filetype
from src.extractable.ModeManager import Mode
from src.extractable.Dataobj import DataObj
from tests.variables import empty_folder, table_pdf_file, table_png_file_standard, test_images_dir, \
    test_xmls_structures_dir, test_table_structures_dir
from tests.setup_testenv import before_and_after, setup_test_environment


def test_StructureRecognitionTATR_dataobjVariablesShouldBePersistent(setup_test_environment, before_and_after):
    # Arrange
    mock_tempobj = tempfile.TemporaryDirectory()
    mock_tempdir = mock_tempobj.name

    mock_tempobj2 = tempfile.TemporaryDirectory()
    mock_output_dir = mock_tempobj2.name

    data = {
        'pdf_images': [os.path.join(test_images_dir, f) for f in os.listdir(test_images_dir) if f.endswith(".jpg")],
        'table_locations': [
            {'x': 28, 'y': 12, 'page': 0},
            {'x': 172, 'y': 367, 'page': 2},
            {'x': 171, 'y': 291, 'page': 3},
            {'x': 176, 'y': 1609, 'page': 3},
            {'x': 172, 'y': 530, 'page': 4}],
        'table_corrections': None,
        'table_images': None,
        'table_structures': None,
        'final_tables': None
    }

    input_dataobj = DataObj(input_file=table_pdf_file,
                            output_dir=mock_output_dir,
                            output_filetype=Filetype.XML,
                            temp_dir=mock_tempdir,
                            data=data)
    # Act
    output_dataobj = extractable.StructureRecognitionTATR.process(input_dataobj)

    # Assert
    assert output_dataobj.input_file == input_dataobj.input_file
    assert output_dataobj.output_filetype == input_dataobj.output_filetype
    assert output_dataobj.output_dir == input_dataobj.output_dir
    assert output_dataobj.mode == input_dataobj.mode
    assert output_dataobj.data['table_locations'] == data['table_locations']


def test_StructureRecognitionTATR_shouldCreateOutputTableXMLsToOutputfile(before_and_after):
    # Arrange
    mock_tempobj = tempfile.TemporaryDirectory()
    mock_tempdir = mock_tempobj.name

    mock_tempobj2 = tempfile.TemporaryDirectory()
    mock_output_dir = mock_tempobj2.name

    data = {
        'pdf_images': [os.path.join(test_images_dir, f) for f in os.listdir(test_images_dir) if f.endswith(".jpg")],
        'table_locations': [
            {'x': 28, 'y': 12, 'page': 0},
            {'x': 172, 'y': 367, 'page': 2},
            {'x': 171, 'y': 291, 'page': 3},
            {'x': 176, 'y': 1609, 'page': 3},
            {'x': 172, 'y': 530, 'page': 4}],
        'table_corrections': None,
        'table_images': None,
        'table_structures': None,
        'final_tables': None
    }

    input_dataobj = DataObj(input_file=table_pdf_file,
                            output_dir=mock_output_dir,
                            output_filetype=Filetype.XML,
                            temp_dir=mock_tempdir,
                            data=data)
    expected_output_xmls = [os.path.join(test_xmls_structures_dir, f) for f in os.listdir(test_xmls_structures_dir) if
                            f.endswith(".xml")]

    expected_table_corrections = [
        [11.579399108886719, 45.11351013183594],
        [123.72590637207031, 121.84202575683594],
        [108.12356567382812, 116.26031494140625],
        [110.49417114257812, 111.89913940429688],
        [120.85197448730469, 109.80392456054688]]

    ''''
    #TODO: check if table structures expected and actual are equal
    
    expected_table_structures = [Table.Table.from_json((open(os.path.join(test_table_structures_dir, t_json))).read())
                                 for t_json in os.listdir(test_table_structures_dir)
                                 if t_json.endswith(".json")]
    '''

    # Act
    output_dataobj = extractable.StructureRecognitionTATR.process(input_dataobj)

    # Assert
    assert expected_table_corrections == output_dataobj.data['table_corrections']
    #assert expected_table_structures == output_dataobj.data['table_structures']
    true_output_xmls = [os.path.join(mock_output_dir, f) for f in os.listdir(mock_output_dir) if
                        f.endswith(".xml")]
    for expected_output_xml, true_output_xml in zip(expected_output_xmls, true_output_xmls):
        expected_output_xml_content = ET.tostring(ET.parse(expected_output_xml).getroot())
        true_output_xml_content = ET.tostring(ET.parse(true_output_xml).getroot())

        return expected_output_xml_content == true_output_xml_content
