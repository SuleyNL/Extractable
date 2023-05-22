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
    def process(dataobj: DataObj):
        # Convert the PDF to an image using pdf2image library (dependency on poppler)
        # Return the image as an object that can be passed to the next step in the pipeline

        images = pdf2image.convert_from_path(dataobj.input_file)

        for i, image in enumerate(images):
            image_path = f"{dataobj.input_file.rstrip('.pdf')}_page_{i + 1}.jpg"
            image.save(image_path, "JPEG")
            dataobj.input_file = image_path #temporary solution! doesnt scale!

        # Display the first image
        plt.imshow(images[0])
        plt.title('pdf is transformed to this image')
        plt.axis('on')  # Optional: Turn off axis labels
        plt.show()

        dataobj.data[__class__.__name__] = {}
        return dataobj


class ConvertUsingPDF2JPG(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Convert the PDF to an image using pdf2jpg library dependent (uses cmd commands under the hood)
        # Return the image as an object that can be passed to the next step in the pipeline

        output_dir = 'tables/'

        result = pdf2jpg.convert_pdf2jpg(dataobj.input_file, output_dir, pages="ALL")

        dataobj.data[__class__.__name__] = {}
        return dataobj
