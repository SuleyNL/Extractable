import os
import tempfile
import PIL.Image as Image
import pytest
from unittest.mock import patch

import src.extractable as extractable
from src.extractable import Extractor
from src.extractable.Filetype import Filetype
from src.extractable.ModeManager import Mode
from src.extractable.Dataobj import DataObj
from tests.variables import empty_folder, table_pdf_file, table_png_file_standard, tables_dir, test_images_dir
from tests.setup_testenv import before_and_after


def test_ConvertUsingPDF2image_dataobjVariablesShouldBePersistent(before_and_after):
    # Arrange
    mock_tempobj = tempfile.TemporaryDirectory()
    mock_tempdir = mock_tempobj.name
    input_dataobj = DataObj(input_file=table_pdf_file,
                            output_dir=empty_folder,
                            output_filetype=Filetype.XML,
                            temp_dir=mock_tempdir)

    # Act
    output_dataobj = extractable.ConvertUsingPDF2image.process(input_dataobj)

    # Assert
    assert output_dataobj.input_file == input_dataobj.input_file
    assert output_dataobj.output_filetype == input_dataobj.output_filetype
    assert output_dataobj.output_dir == input_dataobj.output_dir
    assert output_dataobj.mode == input_dataobj.mode


def test_ConvertUsingPDF2image_shouldCreateOutputImagesToTemp(before_and_after):
    # Arrange
    mock_tempobj = tempfile.TemporaryDirectory()
    mock_tempdir = mock_tempobj.name
    input_dataobj = DataObj(input_file=table_pdf_file,
                            output_dir=empty_folder,
                            output_filetype=Filetype.XML,
                            temp_dir=mock_tempdir)
    # Act
    extractable.ConvertUsingPDF2image.process(input_dataobj)

    # Assert
    if os.path.exists(mock_tempdir):
        output_images = [f for f in os.listdir(mock_tempdir) if f.endswith(".jpg")]
        assert len(output_images) > 0
        for output_image_path in output_images:
            output_image_dir = os.path.join(mock_tempdir, output_image_path)
            output_image = Image.open(output_image_dir)
            reference_image = Image.open(os.path.join(test_images_dir, output_image_path))
            assert output_image == reference_image
    else:
        raise AssertionError(f"The directory '{mock_tempdir}' does not exist.")

