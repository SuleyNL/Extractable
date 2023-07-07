import ntpath
import platform
from pathlib import Path

from Extractable import Extractor
from Extractable.library import *
import pdf2image
from pdf2jpg import pdf2jpg

import abc
from typing import Type

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
import numpy as np
from enum import Enum


class ConvertUsingPDF2image(Pipe):

    @staticmethod
    def process(dataobj):
        # Convert the PDF to an image using pdf2image library (has dependency on poppler)
        # Return the image as an object that can be passed to the next step in the pipeline
        logger = Extractor.Logger()

        poppler_path = None

        if platform.system() == "Windows":
            poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-0.68.0(win)', 'bin')

        elif platform.system() == "Linux":
            poppler_path = os.path.join(os.path.dirname(__file__), 'poppler-23.06.0(linux)')
            pass

        pdf2images = pdf2image.convert_from_path(dataobj.input_file, poppler_path=poppler_path)
        path_to_images = []

        for i, image in enumerate(pdf2images):

            image_name = Path(ntpath.basename(dataobj.input_file)).stem
            image_path_string = f"{image_name}_page_{i + 1}.jpg"
            image_path = dataobj.temp_dir + '\\' + os.path.normpath(image_path_string)
            logger.info('Saved image to: ' + image_path, extra={'className': __class__.__name__})

            image.save(image_path, "JPEG")
            path_to_images.append(image_path)

            if dataobj.mode == Mode.PRESENTATION_PLUS:
                # Display the image
                image_file = Image.open(image_path).convert("RGB")
                plt.imshow(image_file)
                plt.title('pdf is transformed to image(s) | number: ' + str(i+1) + '/' + str(len(pdf2images)))
                plt.axis('on')  # Optional: Turn off axis labels
                plt.show()

        dataobj.data['pdf_images'] = path_to_images
        dataobj.data[__class__.__name__] = {}
        return dataobj


# space for other conversion methods. this one is not in use
class dont_use_ConvertUsingPDF2JPG(Pipe):
    @staticmethod
    def process(dataobj):
        # This one doesnt work (yet) !
        # Convert the PDF to an image using pdf2jpg library dependent (uses cmd commands under the hood)
        # Return the image as an object that can be passed to the next step in the pipeline

        output_dir = 'tables/'

        result = pdf2jpg.convert_pdf2jpg(dataobj.input_file, output_dir, pages="ALL")

        dataobj.data[__class__.__name__] = {}
        return dataobj
