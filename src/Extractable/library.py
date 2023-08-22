import abc
import os
import tempfile
from enum import Enum

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection
import matplotlib.pyplot as plt
import numpy as np


class Filetype(Enum):
    EXCEL = 'xlsx'
    LATEX = 'tex'
    PARQUET = 'parquet'
    PDF = 'pdf'
    IMG = 'img'
    XML = 'xml'
    JSON = 'json'
    CSV = 'csv'
    HTML = 'html'
    YAML = 'yaml'


class Mode(Enum):
    PERFORMANCE = 'performance'                 # maximize performance for big data ETL
    PRESENTATION = 'presentation'               # show every visual step in process
    PRESENTATION_PLUS = 'presentation plus'     # show every visual step in process, including irrelevant steps such as transforming images
    DEBUG = 'debug'                             # don't show every visual step, but do log all debugging-relevant information


class DataObj:
    def __init__(self, data: dict,
                 input_file: str,
                 output_file: str,
                 output_filetype: Filetype = Filetype.XML,
                 mode: Mode = Mode.PERFORMANCE):

        data['pdf_images'] = None if input_file.endswith('.pdf') else [input_file]       # image of each page in pdf
        data['table_locations'] = None                                                   # a list of dicts, each sublist containing the leftupper x,y value of the table-cropped image, aswell as the page it belongs to and table_id
        data['table_corrections'] = None                                                 # for each table, the difference between detected table (topleft xy tuple) by TableDetector vs by StructureDetector, so this can be used to find true location of words on page
        data['table_images'] = None                                                      # image of each table
        data['table_structures'] = None                                                  # a Table() containing bboxes, for each table
        data['final_tables'] = None                                                      # a Table() containing bboxes and text, for each table

        self.data = data
        self.input_file = input_file    # input pdf or img
        self.output_file = output_file  # output dir for example 'tables/' produces tables/_table_1.xml
                                        # if not a dir, like 'tables/hello', it will be treated as prefix
                                        # so it will produce tables/hello_table_1.xml
        self.output_filetype = output_filetype
        self.mode = mode
        self.temp = tempfile.TemporaryDirectory()
        self.temp_dir = self.temp.name

    def output(self) -> dict:
        return self.data


class Pipe(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process(input_obj: DataObj):
        return input_obj


class Bbox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    @property
    def xy1(self):
        return self.x1, self.y1

    @property
    def xy2(self):
        return self.x2, self.y2

    @property
    def box(self):
        return [self.x1, self.y1, self.x2, self.y2]

    @property
    def width(self):
        return abs(self.x1 - self.x2)

    @property
    def height(self):
        return abs(self.y1 - self.y2)

    @property
    def area(self):
        """
        Calculates the surface area. useful for IOU!
        """
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)

    def intersection_area(self, bbox):
        x1 = max(self.x1, bbox.x1)
        y1 = max(self.y1, bbox.y1)
        x2 = min(self.x2, bbox.x2)
        y2 = min(self.y2, bbox.y2)
        intersection = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)
        return intersection

    def iou(self, bbox):
        intersection = self.intersection_area(bbox)

        iou = intersection / float(self.area + bbox.area - intersection)
        # return the intersection over union value
        return iou


def intersects(box1: tuple, box2: tuple,
               box1_width: int = 100, box1_height: int = 15,
               box2_width: int = 100, box2_height: int = 15):

    # accepts two tuples within which:
    # tuple[0] = x
    # tuple[1] = y

    x1, y1 = box1
    box1_top_left = (x1,            y1)
    box1_top_right = (x1 + box1_width,    y1)
    box1_bottom_left = (x1,            y1 + box1_height)
    box1_bottom_right = (x1 + box1_width,    y1 + box1_height)

    x2, y2 = box2
    box2_top_left = (x2,            y2)
    box2_top_right = (x2 + box2_width,    y2)
    box2_bottom_left = (x2,            y2 + box2_height)
    box2_bottom_right = (x2 + box2_width,    y2 + box2_height)

    return not (box1_top_right[0] < box2_bottom_left[0] or box1_bottom_left[0] > box2_top_right[0] or box1_top_right[1] > box2_bottom_left[1] or box1_bottom_left[1] < box2_top_right[1])


def plot_results(pil_img, model, scores, labels, boxes, title: str):
    plt.figure(figsize=(8, 5))
    plt.imshow(pil_img)
    ax = plt.gca()
    COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
              [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
    colors = COLORS * 100
    drawn_boxes = []
    for score, label, (xmin, ymin, xmax, ymax), color in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
        alpha = 0.15
        linewidth = 1
        if model.config.id2label[label] == 'table row':
            text_x = 0-(pil_img.height*0.18)
            text_y = ((ymin+ymax)/2)
            color = [0.850, 0.325, 0.098]

        elif model.config.id2label[label] == 'table column':
            text_x = ((xmin+xmax)/2)-80
            text_y = ymin-15
            color = [0.350, 0.925, 0.098]

        elif model.config.id2label[label] == 'table':
            text_x = xmin+30
            text_y = ymin-50
            color = [0.000, 0.447, 0.741]

        else:
            text_x = ((xmin+xmax)/2)-100
            text_y = ((ymin+ymax)/2)+3
            color = [0.033, 0.045, 0.033]
            alpha = 0.05
            linewidth = 0
            ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, facecolor=color, alpha=0.3, linewidth=0))

        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=color, linewidth=linewidth))

        '''
        # Below code not that necessary yet, maybe in future with different type of pdf-tables. 
        # But for now adds unnecessary complexity
        
        # check if textbox overlaps with another textbox
        for drawn_box in drawn_boxes:
            while intersects(drawn_box, (xmin, ymin)):
                #if model.config.id2label[label] == 'table':
                xmin = max(xmin-10, 0)
                if xmin == 0:
                    ymin = max(ymin-10, 0)

                if xmin == 0 and ymin == 0:
                    break
        '''

        text = f'{model.config.id2label[label]}: {score:0.2f}'
        ax.text(text_x, text_y, text, fontsize=6,
                bbox=dict( facecolor=color, alpha=alpha))
        drawn_boxes.append([xmin, ymin])

    plt.axis('on')
    plt.title(title)
    plt.show()
