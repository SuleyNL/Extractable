from Extractable.library import *

import abc
from typing import Type, List

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrForObjectDetection, DetrImageProcessor
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
import scipy
from Extractable import Extractor
import tempfile
import os
import ntpath
from pathlib import Path


class TableDetectorTATR(Pipe):
    @staticmethod
    def process(dataobj):
        logger = Extractor.Logger()

        table_locations:  List[dict] = []

        # Detect tables in the image
        # Return the table locations as an object that can be passed to the next step in the pipeline
        if dataobj.data['table_images'] is not None and len(dataobj.data['table_images']) > 0:
            images = dataobj.data['table_images']
        elif dataobj.data['pdf_images'] is not None and len(dataobj.data['pdf_images']) > 0:
            images = dataobj.data['pdf_images']
        else:
            images = None
            #TODO: raise error no image found
            pass

        inner_data = {}
        inner_data['detection'] = []
        table_images = []                   #cropped images of only the table
        for i, image_path in enumerate(images):
            image = Image.open(image_path).convert("RGB")

            image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
            model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

            inputs = image_processor(images=image, return_tensors="pt")
            outputs = model(**inputs)

            # convert outputs (bounding boxes and class logits) to COCO API
            target_sizes = torch.tensor([image.size[::-1]])
            results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

            for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
                box = [round(i, 2) for i in box.tolist()]
                inner_data['detection'].append(f"Detected {model.config.id2label[label.item()]} with confidence: " +f"{round(score.item(), 3)} at location: {box}")
                logger.info(
                    f"Detected {model.config.id2label[label.item()]} with confidence " f"{round(score.item(), 3)} at location {box}",
                    extra={'className': __class__.__name__})

            if dataobj.mode == Mode.PRESENTATION:
                plot_results(image, model, results['scores'], results['labels'], results['boxes'], title='Page number: ' + str(i + 1) + '/' + str(len(images)) +' | Tables detected: ' + str(len(results["scores"])))

            max_height, max_width = target_sizes[0]

            if len(results["scores"]) > 0:
                for j, bbox in enumerate(results["boxes"]):
                    # Extract the bounding box values as a list
                    bbox = bbox.int().tolist()

                    # Increase the bounding boxes by 40 pixels to zoom out a bit to give the table a loose fit
                    bbox_enlarged = [
                        max(bbox[0] - 40, 0),  # expanded_x_min
                        max(bbox[1] - 40, 0),  # expanded_y_min
                        min(bbox[2] + 40, max_width.item()),  # expanded_x_max
                        min(bbox[3] + 40, max_height.item())  # expanded_y_max
                    ]
                    table_locations.append({'x': bbox_enlarged[0], 'y': bbox_enlarged[1], 'page': i})
                    table_image = image.crop(bbox_enlarged)

                    if dataobj.mode == Mode.PRESENTATION:
                        plt.imshow(table_image)
                        plt.axis('on')
                        plt.title('cropped image of only table | number ' + str(j + 1) + ' out of ' + str(len(results["scores"])))
                        plt.show()

                    image_name = Path(ntpath.basename(dataobj.input_file)).stem
                    image_path_string = f"{image_name}_table_{i + 1}{('.' + str(j + 1))if i>0 else ''}.jpg"
                    image_path = dataobj.temp_dir + '\\' + os.path.normpath(image_path_string)

                    logger.info('Saved image to: ' + image_path, extra={'className': __class__.__name__})

                    table_image.save(image_path, "JPEG")
                    table_images.append(image_path)

        dataobj.data['table_locations'] = table_locations
        dataobj.data['table_images'] = table_images
        dataobj.data[__class__.__name__] = inner_data
        return dataobj


class TableDetectorDETR(Pipe):
    #unused
    @staticmethod
    def process(dataobj):
        file_path = dataobj.input_file
        image = Image.open(file_path).convert("RGB")

        feature_extractor = DetrImageProcessor.from_pretrained('facebook/detr-resnet-101-dc5')
        model = DetrForObjectDetection.from_pretrained('facebook/detr-resnet-101-dc5')

        inputs = feature_extractor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # model predicts bounding boxes and corresponding COCO classes
        logits = outputs.logits
        bboxes = outputs.pred_boxes

        # convert outputs (bounding boxes and class logits)
        image_width, image_height = image.size[::-1]

        # Only keep the bounding boxes, not the tensor
        bboxes.squeeze_(0)

        # Convert the bounding box coordinates from [0,1] normalized values to real pixel values
        bboxes[:, 0] *= image_width  # xmin
        bboxes[:, 1] *= image_height  # ymin
        bboxes[:, 2] *= image_width  # xmax
        bboxes[:, 3] *= image_height  # ymax

        scores = np.ones((bboxes.shape[0]))
        ids = np.zeros((bboxes.shape[0]))
        plot_results(image, model, scores, ids, bboxes, title='detected tables using DETR')
        return dataobj


