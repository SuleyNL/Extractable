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


class StandardPreprocessor(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Preprocess the image
        # Return the preprocessed image as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj