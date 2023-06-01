import ntpath
import os
from pathlib import Path

from transformers import DetrFeatureExtractor

from Extractable import Extractor
from Extractable.Datatypes.Cell import Cell
from Extractable.Datatypes.Row import Row
from Extractable.Datatypes.Table import Table
from Extractable.library import *
import abc
from typing import Type

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import xml.etree.ElementTree as ET


class StructureRecognitionWithTATR(Pipe):
    @staticmethod
    def process(dataobj):
        logger = Extractor.Logger()
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

        table_structures = []
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

            results = feature_extractor.post_process_object_detection(outputs, threshold=0.1, target_sizes=target_sizes)[0]

            filtered_results = {
                'boxes': [],
                'scores': [],
                'labels': []
            }

            for label, score, box in zip(results['labels'].tolist(), results['scores'].tolist(), results['boxes'].tolist()):
                # parameter tuning, TATR is overly sensitive to certain labels
                # filter out results of table column (1) where confidence is lower than 89%
                # filter out results of table row (2) where confidence is lower than 74% @lager dan 74 @niet hoger dan 64
                # filter out results of table spanning cell (5) where confidence is lower than 88%
                if not (label == 1 and score <= .88) and \
                        not (label == 2 and score <= .64) and \
                        not ((label == 3 or label == 4 or label == 5) and score <= .88):
                    # Add new elements to the respective tensors in the results dictionary
                    filtered_results['boxes'].append(box)
                    filtered_results['scores'].append(score)
                    filtered_results['labels'].append(label)

            results['boxes'] = torch.Tensor(filtered_results['boxes'])
            results['scores'] = torch.Tensor(filtered_results['scores'])
            results['labels'] = torch.Tensor(filtered_results['labels'])

            rows = []

            # make an XML Cell() for every recognized cell and add to a Row() and Table()
            # for every row
            for score, label, (xmin1, ymin1, xmax1, ymax1) in zip(results['scores'].tolist(), results['labels'].tolist(), results['boxes'].tolist()):
                if model.config.id2label[label] == 'table row': #TODO this can be done more efficiently than looping twice

                    bbox_row = Bbox(x1=xmin1, y1=ymin1, x2=xmax1, y2=ymax1)
                    row = Row(len(rows), xy1=(bbox_row.x1, bbox_row.y1), xy2=(bbox_row.x2, bbox_row.y2))

                    #for every column
                    for score, label, (xmin2, ymin2, xmax2, ymax2) in zip(results['scores'].tolist(), results['labels'].tolist(), results['boxes'].tolist()):
                        if model.config.id2label[label] == 'table column':

                            # add every intersection with a column as seperate cell
                            bbox_column = Bbox(x1=xmin2, y1=ymin2, x2=xmax2, y2=ymax2)
                            if intersects((bbox_column.x2, bbox_column.y2), (bbox_row.x2, bbox_row.y2),
                                       box1_width=bbox_column.width, box1_height=bbox_column.height,
                                       box2_width=bbox_row.width, box2_height=bbox_row.height):
                                cell_bbox = row.intersection_with_column_bbox(bbox_column)
                                row.add_one_cell(Cell('', len(row.cells), cell_bbox.xy1, cell_bbox.xy2))
                    rows.append(row)

            table = Table(i, rows=rows)
            table_structures.append(table)

            # Convert detected table structure to XML Object
            table_xml = ET.fromstring(table.toXML())

            # Create an ElementTree object
            tree = ET.ElementTree(table_xml)

            # Write the XML object to the file
            file_prefix = os.path.splitext(dataobj.output_file)[0]

            if ntpath.isdir(file_prefix):
                output_file = file_prefix + '/' + 'table_' + str(i+1) + '.xml'
            else:
                output_file = file_prefix + '_table_' + str(i+1) + '.xml'

            if not Path(output_file).parent.exists():
                os.makedirs(Path(output_file).parent)

            tree.write(output_file, encoding="utf-8")

            logger.info('Detected structure saved to: %s', output_file, extra={'className': __class__.__name__})

            if dataobj.mode == Mode.PRESENTATION:
                plot_results(image, model, results['scores'], results['labels'], results['boxes'], 'Recognized structure | table number ' + str(i+1) + ' out of ' + str(len(images)))
        dataobj.data['table_structures'] = table_structures

        dataobj.data[__class__.__name__] = {"objects detected: " + str([f"{model.config.id2label[value]}: {np.count_nonzero(results['labels'] == value)}" for value in np.unique(results['labels'])])}
        return dataobj