import abc
from typing import Type

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
import numpy as np


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
    def process(input_obj: DataObj):
        pass


class PDFToImageConverter(Pipe):
    @staticmethod
    def process(dataobj):
        # Convert the PDF to an image
        # Return the image as an object that can be passed to the next step in the pipeline
        dataobj.data[__class__.__name__] = {}

        return dataobj


def plot_results(pil_img, model, scores, labels, boxes):
    plt.figure(figsize=(16, 10))
    plt.imshow(pil_img)
    ax = plt.gca()
    COLORS = [[0.000, 0.447, 0.741], [0.850, 0.325, 0.098], [0.929, 0.694, 0.125],
              [0.494, 0.184, 0.556], [0.466, 0.674, 0.188], [0.301, 0.745, 0.933]]
    colors = COLORS * 100
    for score, label, (xmin, ymin, xmax, ymax), c in zip(scores.tolist(), labels.tolist(), boxes.tolist(), colors):
        ax.add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin,
                                   fill=False, color=c, linewidth=3))
        text = f'{model.config.id2label[label]}: {score:0.2f}'
        ax.text(xmin, ymin, text, fontsize=15,
                bbox=dict(facecolor='yellow', alpha=0.5))
    plt.axis('off')
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
