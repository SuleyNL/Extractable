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
        # Detect structure in a table_image
        # Return the table locations as an object that can be passed to the next step in the pipeline
        if dataobj.data['table_images'] is not None and len(dataobj.data['table_images']) > 0:
            images = dataobj.data['table_images']
        elif dataobj.data['pdf_images'] is not None and len(dataobj.data['pdf_images']) > 0:
            images = dataobj.data['pdf_images']
        else:
            images = None
            #TODO: raise error no image found
            pass

        for i, image in enumerate(images):
            image = Image.open(image).convert("RGB")
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
            '''
            
            TODO make a XML Cell(), Row() and Table() for every recognized cell
            for score, label, (xmin1, ymin1, xmax1, ymax1), color in zip(results['scores'].tolist(), results['labels'].tolist(), results['boxes'].tolist()):
                print()
                if model.config.id2label[label] == 'table row': #TODO this can be done more efficiently than looping twice
                    for score, label, (xmin2, ymin2, xmax2, ymax2), color in zip(results['scores'].tolist(),
                                                                             results['labels'].tolist(),
                                                                             results['boxes'].tolist()):
                        if model.config.id2label[label] == 'table column':
            '''

            plot_results(image, model, results['scores'], results['labels'], results['boxes'], 'Recognized structure | table number ' + str(i+1) + ' out of ' + str(len(images)))



        dataobj.data[__class__.__name__] = {"objects detected: " + str([f"{model.config.id2label[value]}: {np.count_nonzero(results['labels'] == value)}" for value in np.unique(results['labels'])])}
        return dataobj