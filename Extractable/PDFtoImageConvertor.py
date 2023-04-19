from Extractable.library import *

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


class StandardConversion(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Convert the PDF to an image
        # Return the image as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}

        return dataobj