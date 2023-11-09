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
    test_xmls_structures_dir, test_table_structures_dir, test_table_images_dir
from tests.setup_testenv import before_and_after, setup_test_environment


def test_DataObjWithEmptyData_shouldbeJSONconvertible():
    # Arrange
    data = {'pdf_images': None, 'table_locations': None,
            'table_corrections': None, 'table_images': [0, 334, 245363, 24234], 'table_structures': None,
            'final_tables': None}

    dataObj = DataObj(input_file=table_pdf_file, output_dir=table_pdf_file, output_filetype=extractable.Filetype.XML, data=data)

    # Act
    dataObj_json = dataObj.toJSON()  # dataObj.toJSON()
    dataObj_fromJSON = DataObj.fromJSON(dataObj_json)

    # Assert
    assert dataObj.output_filetype == dataObj_fromJSON.output_filetype
    assert dataObj.output_dir      == dataObj_fromJSON.output_dir
    assert dataObj.mode            == dataObj_fromJSON.mode
    assert dataObj.input_file      == dataObj_fromJSON.input_file
    assert dataObj.data            == dataObj_fromJSON.data
    assert dataObj.temp_dir        == dataObj_fromJSON.temp_dir


def test_DataObjWithComplexData_shouldbeJSONconvertible():
    # Arrange
    data = {
        'pdf_images': [os.path.join(test_images_dir, f) for f in os.listdir(test_images_dir) if f.endswith(".jpg")],
        'table_locations': [
            {'x': 28, 'y': 12, 'page': 0},
            {'x': 172, 'y': 367, 'page': 2},
            {'x': 171, 'y': 291, 'page': 3},
            {'x': 176, 'y': 1609, 'page': 3},
            {'x': 172, 'y': 530, 'page': 4}],
        'table_corrections': [
        [11.579399108886719, 45.11351013183594],
        [123.72590637207031, 121.84202575683594],
        [108.12356567382812, 116.26031494140625],
        [110.49417114257812, 111.89913940429688],
        [120.85197448730469, 109.80392456054688]],
        'table_images': [os.path.join(test_table_images_dir, f) for f in os.listdir(test_table_images_dir) if f.endswith(".jpg")],
        'table_structures': None,
        'final_tables': None
    }

    dataObj = DataObj(input_file=table_pdf_file, output_dir=table_pdf_file, output_filetype=extractable.Filetype.XML,
                      data=data)

    # Act
    dataObj_json = dataObj.toJSON()  # dataObj.toJSON()
    dataObj_fromJSON = DataObj.fromJSON(dataObj_json)

    # Assert
    assert dataObj.output_filetype == dataObj_fromJSON.output_filetype
    assert dataObj.output_dir == dataObj_fromJSON.output_dir
    assert dataObj.mode == dataObj_fromJSON.mode
    assert dataObj.input_file == dataObj_fromJSON.input_file
    assert dataObj.data == dataObj_fromJSON.data
    assert dataObj.temp_dir == dataObj_fromJSON.temp_dir

# TODO: add tables to the data[structures] to see if tables are also convertible
