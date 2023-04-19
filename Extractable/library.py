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


class DataObj:
    def __init__(self, data: dict, input_file: str, output_file: str):
        self.data = data
        self.input_file = input_file
        self.output_file = output_file

    def output(self):
        return self.data


class Pipe(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process(dataobj: DataObj):
        pass


def plot_results(pil_img, model, scores, ids, boxes):
    plt.figure(figsize=(16, 10))
    plt.imshow(pil_img)
    ax = plt.gca()
    COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
              [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
    colors = COLORS * 100
    for score, id, (xmin, ymin, xmax, ymax), c in zip(scores.tolist(), ids.tolist(), boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        text = f'{model.config.id2label[id]}: {score:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('on')
    plt.show()

# Define the input and output files
data_object = DataObj({}, input_file='input.txt', output_file='output.txt')

#pipes: list[Type[Pipe]] = [PDFToImageConverter, ImagePreprocessor, TableDetector, TextExtractor, XMLConverter]


def Pipeline(dataobj: DataObj, pipes: list[Type[Pipe]]):
    # Initialize dataobj
    processed_dataobj = dataobj

    # Apply pipelines in sequence
    for pipe in pipes:
        processed_dataobj = pipe.process(processed_dataobj)

    # Return final processed data object
    return processed_dataobj.output()

'''
# Build pipeline of desired functions and order
pipeline = compose_left(
    PDFToImageConverter.process,
    ImagePreprocessor.process,
    TableDetector.process,
    TextExtractor.process,
    XMLConverter.process,
    DataObj.output
)
'''

# Start pipeline with desired DataObj
# print(Pipeline(data_object, pipes))
# print(pipeline(data_object))
