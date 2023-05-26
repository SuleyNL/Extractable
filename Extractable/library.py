import abc
from enum import Enum
from typing import Type

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
import numpy as np


class Filetype(Enum):
    PDF = 'pdf'
    IMG = 'img'


class Mode(Enum):
    PERFORMANCE = 'performance'
    PRESENTATION = 'presentation'


class DataObj:
    def __init__(self, data: dict, input_file: str, output_file: str, input_filetype: Filetype = Filetype.PDF, mode: Mode = Mode.PERFORMANCE):

        data['pdf_images'] = [input_file] if input_filetype is not None else None        # image of each page in pdf
        data['table_images'] = None                                                      # image of each table in pdf
        data['table_structures'] = None                                                  # a Table() containing bboxes, for each table in pdf
        data['tables'] = None                                                            # a Table() containing bboxes and text, for each table in pdf

        self.data = data
        self.input_file = input_file    # input pdf or img
        self.output_file = output_file  # output xml (or other type, yet to be produced)
        self.mode = mode                # performance or presentation, if presentation: show every visual step in process

    def output(self):
        return self.data


class Pipe(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def process(input_obj: DataObj):
        return data_object


class PDFToImageConverter(Pipe):
    @staticmethod
    def process(dataobj):
        # Convert the PDF to an image
        # Return the image as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}

        return dataobj


class Bbox:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

        self.xy1 = (self.x1, self.y1)
        self.xy2 = (self.x2, self.y2)

        self.box = [self.x1, self.y1, self.x2, self.y2]
        self.width = abs(self.x1 - self.x2)
        self.height = abs(self.y1 - self.y2)

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

    # accepts two tuples
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
        # not that necessary yet, maybe in future with different type of pdf-tables. But for now adds unnecessary complexity
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


class ImagePreprocessor(Pipe):
    @staticmethod
    def process(dataobj):
        # Preprocess the image
        # Return the preprocessed image as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class TableDetector(Pipe):
    @staticmethod
    def process(dataobj):
        # Detect tables in the image
        # Return the table locations as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class TableStructureDetectorTATR(Pipe):
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


class TableDetectorTATR(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Detect tables in the image
        # Return the table locations as an object that can be passed to the next step in the pipeline

        # file_path = hf_hub_download(repo_id="nielsr/example-pdf", repo_type="dataset", filename="example_pdf.png")
        file_path = dataobj.input_file
        image = Image.open(file_path).convert("RGB")

        image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[
            0
        ]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            dataobj.data[__class__.__name__] = {f"Detected {model.config.id2label[label.item()]} with confidence " +
                                                f"{round(score.item(), 3)} at location {box}"}
            print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
            )

        plot_results(image, model, results['scores'], results['labels'], results['boxes'])
        return dataobj


class TextExtractor(Pipe):
    @staticmethod
    def process(dataobj):
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class TextExtractorTesseractOCR(Pipe):
    @staticmethod
    def process(dataobj):
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class TextExtractorPDF(Pipe):
    '''
    We process the PDF document into a sequence of
    characters each with their associated bounding box and use
    the Needleman-Wunsch algorithm [9] to align this with the
    character sequence for the text extracted from each table
    XML
    '''

    @staticmethod
    def process(dataobj):
        # Extract text from the cells
        # Return the text as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}
        return dataobj


class XMLConverter(Pipe):
    @staticmethod
    def process(dataobj):
        # Convert the extracted text to XML
        # Return the XML as a string
        dataobj.data[__class__.__name__] = {}
        return dataobj


# Define the input and output files
data_object = DataObj({}, input_file='input.txt', output_file='output.txt')

pipes: list[Type[Pipe]] = [PDFToImageConverter, ImagePreprocessor, TableDetector, TextExtractor, XMLConverter]


def Pipeline(dataobj: DataObj, pipes: list[Type[Pipe]]):
    # Initialize dataobj
    processed_dataobj = dataobj

    # Apply pipelines in sequence
    for pipe in pipes:
        processed_dataobj = pipe.process(processed_dataobj)

    # Return final processed data object
    return processed_dataobj.output()


# Build pipeline of desired functions and order
pipeline = compose_left(
    PDFToImageConverter.process,
    ImagePreprocessor.process,
    TableDetector.process,
    TextExtractor.process,
    XMLConverter.process,
    DataObj.output
)

# Start pipeline with desired DataObj
# print(Pipeline(data_object, pipes))
# print(pipeline(data_object))
