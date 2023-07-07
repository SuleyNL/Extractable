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
        # Detect structure in a table_image
        # Return the table locations as an object that can be passed to the next step in the pipeline
        logger = Extractor.Logger()

        if dataobj.data['table_images'] is not None and len(dataobj.data['table_images']) > 0:
            images = dataobj.data['table_images']
        elif dataobj.data['pdf_images'] is not None and len(dataobj.data['pdf_images']) > 0:
            images = dataobj.data['pdf_images']
        else:
            images = None
            # TODO: raise error no image found
            pass
        table_corrections = []
        table_structures = []
        table_locations = dataobj.data['table_locations']

        if len(table_locations) == 0:
            # no tables detected to run structure detector on
            # can be expanded by having structuredetector still look for tables itself regardless
            return dataobj

        for i, image in enumerate(images):
            image = Image.open(image).convert("RGB")
            width, height = image.size
            image.resize((int(width * 0.5), int(height * 0.5)))

            feature_extractor = DetrFeatureExtractor()
            encoding = feature_extractor(image, return_tensors="pt")
            encoding.keys()

            model = TableTransformerForObjectDetection.from_pretrained(
                "microsoft/table-transformer-structure-recognition")

            with torch.no_grad():
                outputs = model(**encoding)
            target_sizes = [image.size[::-1]]

            results = \
            feature_extractor.post_process_object_detection(outputs, threshold=0.1, target_sizes=target_sizes)[0]

            presentation_results = {
                'boxes': [],
                'scores': [],
                'labels': []
            }

            filtered_results = {
                'boxes': [],
                'scores': [],
                'labels': []
            }

            # Save the difference between detected table by StructureDetector compared to TableDetector
            table_index = torch.where(results['labels'] == 0)[0].item()
            box = results['boxes'][table_index]
            x1, y1 = box[:2]
            diff_x = x1 - 40  # 40 because TableDetector zoomed out by 40px
            diff_y = y1 - 40  # 40 because TableDetector zoomed out by 40px
            table_corrections.append((diff_x, diff_y))
            logger.info('Table correction: ' + str((diff_x, diff_y)), extra={'className': __class__.__name__})

            for label, score, box in zip(results['labels'].tolist(), results['scores'].tolist(),
                                         results['boxes'].tolist()):
                # parameter tuning, TATR is overly sensitive to certain labels
                # 0: 'table',
                # 1: 'table column',
                # 2: 'table row',
                # 3: 'table column header',
                # 4: 'table projected row header',
                # 5: 'table spanning cell'
                # filter out results of table column (1) where confidence is lower than 89%
                # filter out results of table row (2) where confidence is lower than 74% @lager dan 74 @niet hoger dan 64
                # filter out results of table spanning cell (5) where confidence is lower than 88%
                if not (label == 1 and score <= .88) and \
                        not (label == 2 and score <= .64) and \
                        not ((label == 3 or label == 4 or label == 5) and score <= .88):
                    # Add new elements to the respective tensors in the results dictionary
                    presentation_results['scores'].append(score)
                    presentation_results['labels'].append(label)
                    presentation_results['boxes'].append(box)

                    # Perform table coordinate corrections on each unit
                    table_x = table_locations[i]['x']
                    table_y = table_locations[i]['y']

                    unit_bbox = Bbox(*box)

                    unit_bbox.x1 += table_corrections[-1][0] + table_x
                    unit_bbox.x2 += table_corrections[-1][0] + table_x
                    unit_bbox.y1 += table_corrections[-1][1] + table_y
                    unit_bbox.y2 += table_corrections[-1][1] + table_y

                    # Add new elements to the respective tensors in the results dictionary
                    filtered_results['scores'].append(score)
                    filtered_results['labels'].append(label)
                    filtered_results['boxes'].append(unit_bbox.box)

            # TODO: this can be done more efficiently than creating a tensor after it was a list
            presentation_results['boxes'] = torch.Tensor(presentation_results['boxes'])
            presentation_results['scores'] = torch.Tensor(presentation_results['scores'])
            presentation_results['labels'] = torch.Tensor(presentation_results['labels'])

            filtered_results['boxes'] = torch.Tensor(filtered_results['boxes'])
            filtered_results['scores'] = torch.Tensor(filtered_results['scores'])
            filtered_results['labels'] = torch.Tensor(filtered_results['labels'])

            # SORT BOXES BY HORIZONTAL POSITION LEFT TO RIGHT
            # Get the X-min values from the 'boxes' tensor
            xmins = filtered_results['boxes'][:, 0]
            # Use torch.argsort() to get the indices that would sort the 'xmins' tensor
            sorted_indices = torch.argsort(xmins)
            # Sort
            filtered_results['boxes'] = filtered_results['boxes'][sorted_indices]
            filtered_results['scores'] = filtered_results['scores'][sorted_indices]
            filtered_results['labels'] = filtered_results['labels'][sorted_indices]

            # SORT BOXES BY VERTICAL POSITION TOP TO BOTTOM
            # Get the Y-min values from the 'boxes' tensor
            ymins = filtered_results['boxes'][:, 1]
            # Use torch.argsort() to get the indices that would sort the 'ymins' tensor
            sorted_indices = torch.argsort(ymins)
            # Sort the 'boxes', 'scores', and 'labels' tensors based on the sorted indices
            filtered_results['boxes'] = filtered_results['boxes'][sorted_indices]
            filtered_results['scores'] = filtered_results['scores'][sorted_indices]
            filtered_results['labels'] = filtered_results['labels'][sorted_indices]

            # SPLIT INTO COLUMNS AND ROWS
            labels_rows = filtered_results['labels']
            indices_row = (labels_rows == 2).nonzero().squeeze()
            indices_column = (labels_rows == 1).nonzero().squeeze()
            # Split the 'boxes', 'scores', and 'labels' tensors based on the indices
            results_rows = {'boxes': filtered_results['boxes'][indices_row],
                            'scores': filtered_results['scores'][indices_row],
                            'labels': filtered_results['labels'][indices_row]}

            results_columns = {'boxes': filtered_results['boxes'][indices_column],
                               'scores': filtered_results['scores'][indices_column],
                               'labels': filtered_results['labels'][indices_column]}

            # SORT COLUMN BOXES BY HORIZONTAL POSITION LEFT TO RIGHT
            # Get the X-min values from the 'boxes' tensor
            shape = results_columns['boxes'].shape
            if len(shape) == 1 and shape[0] == 4:
                results_columns['boxes'] = torch.tensor([results_columns['boxes'].tolist()])

            xmins = results_columns['boxes'][:, 0]

            # Use torch.argsort() to get the indices that would sort the 'xmins' tensor
            sorted_indices = torch.argsort(xmins)

            # Sort
            results_columns['boxes'] = torch.tensor(results_columns['boxes'][sorted_indices])
            results_columns['scores'] = torch.tensor(results_columns['scores'][sorted_indices]) if len(
                results_columns['scores'].shape) != 0 else torch.tensor(results_columns['scores'].item())
            results_columns['labels'] = torch.tensor(results_columns['labels'][sorted_indices]) if len(
                results_columns['labels'].shape) != 0 else torch.tensor(results_columns['labels'].item())

            # define scores, labels and boxes for rows
            scores_rows = results_rows['scores'].tolist()
            scores_rows = scores_rows if type(scores_rows) != float else [scores_rows]

            labels_rows = results_rows['labels'].tolist()
            labels_rows = labels_rows if type(labels_rows) != float else [labels_rows]

            boxes_rows = results_rows['boxes'].tolist()
            boxes_rows = boxes_rows if type(boxes_rows[0]) != float else [boxes_rows]

            # define scores, labels and boxes for columns
            scores_columns = results_columns['scores'].tolist()
            scores_columns = scores_columns if type(scores_columns) != float else [scores_columns]

            labels_columns = results_columns['labels'].tolist()
            labels_columns = labels_columns if type(labels_columns) != float else [labels_columns]

            boxes_columns = results_columns['boxes'].tolist()
            boxes_columns = boxes_columns if type(boxes_columns[0]) != float else [boxes_columns]

            rows = []

            # make an XML Cell() for every recognized cell and add to a Row() and Table()

            # for every row
            for score, label, (xmin1, ymin1, xmax1, ymax1) in zip(scores_rows, labels_rows, boxes_rows):
                bbox_row = Bbox(x1=xmin1, y1=ymin1, x2=xmax1, y2=ymax1)
                row = Row(len(rows), xy1=(bbox_row.x1, bbox_row.y1), xy2=(bbox_row.x2, bbox_row.y2))

                # for every column
                for score, label, (xmin2, ymin2, xmax2, ymax2) in zip(scores_columns, labels_columns, boxes_columns):

                    # add every intersection with a column as seperate cell
                    bbox_column = Bbox(x1=xmin2, y1=ymin2, x2=xmax2, y2=ymax2)
                    if intersects((bbox_column.x2, bbox_column.y2), (bbox_row.x2, bbox_row.y2),
                                  box1_width=bbox_column.width, box1_height=bbox_column.height,
                                  box2_width=bbox_row.width, box2_height=bbox_row.height):
                        pass
                        # TODO: only add cell if it intersects
                    else:
                        pass
                        # TODO: Error log or Warning log
                        #  that is weird? every column should intersect with a row

                    cell_bbox = row.intersection_with_column_bbox(bbox_column)

                    '''
                    table_x = table_locations[i]['x']
                    table_y = table_locations[i]['y']

                    cell_bbox.x1 += table_corrections[-1][0] + table_x
                    cell_bbox.x2 += table_corrections[-1][0] + table_x
                    cell_bbox.y1 += table_corrections[-1][1] + table_y
                    cell_bbox.y2 += table_corrections[-1][1] + table_y
                    '''

                    row.add_one_cell(Cell('', len(row.cells), cell_bbox.xy1, cell_bbox.xy2))

                rows.append(row)

            table = Table(i, rows=rows)
            table_structures.append(table)

            # Convert detected table structure to XML Object
            table_xml = ET.fromstring(table.to_xml_with_coords())

            # Create an ElementTree object
            tree = ET.ElementTree(table_xml)

            # Prettify XML output
            ET.indent(tree, space="\t", level=0)

            # Write the XML object to the file
            file_prefix = os.path.splitext(dataobj.output_file)[0]

            if ntpath.isdir(file_prefix):
                output_file = file_prefix + '/' + 'table_' + str(i + 1) + '.xml'
            else:
                output_file = file_prefix + '_table_' + str(i + 1) + '.xml'

            if not Path(output_file).parent.exists():
                os.makedirs(Path(output_file).parent)

            tree.write(output_file, encoding="utf-8")

            logger.info('Detected structure saved to: %s', output_file, extra={'className': __class__.__name__})

            if dataobj.mode == Mode.PRESENTATION:
                plot_results(image, model, presentation_results['scores'], presentation_results['labels'],
                             presentation_results['boxes'],
                             'Recognized structure | table number ' + str(i + 1) + ' out of ' + str(len(images)))

        dataobj.data['table_structures'] = table_structures
        dataobj.data['table_corrections'] = table_corrections

        dataobj.data[__class__.__name__] = {"objects detected: " + str(
            [f"{model.config.id2label[value]}: {np.count_nonzero(filtered_results['labels'] == value)}" for value in
             np.unique(filtered_results['labels'])])}
        return dataobj