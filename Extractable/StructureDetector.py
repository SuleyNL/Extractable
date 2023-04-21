from transformers import DetrFeatureExtractor

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


class StructureRecognitionWithTATR(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Detect table structure in a table
        # Return the table locations as an object that can be passed to the next step in the pipeline
        file_path = dataobj.input_file
        image = Image.open(file_path).convert("RGB")
        width, height = image.size
        image.resize((int(width * 0.5), int(height * 0.5)))

        feature_extractor = DetrFeatureExtractor()
        encoding = feature_extractor(image, return_tensors="pt")
        encoding.keys()

        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")

        with torch.no_grad():
            outputs = model(**encoding)
        target_sizes = [image.size[::-1]]

        results = feature_extractor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
        plot_results(image, model, results['scores'], results['labels'], results['boxes'])

        dataobj.data[__class__.__name__] = {"objects detected: " + str([f"{model.config.id2label[value]}: {np.count_nonzero(results['labels'] == value)}" for value in np.unique(results['labels'])])}
        return dataobj