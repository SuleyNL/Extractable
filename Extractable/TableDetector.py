from Extractable.library import *

import abc
from typing import Type

import torch
from PIL import Image
from toolz import compose_left
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrFeatureExtractor, \
    DetrForObjectDetection
import matplotlib.pyplot as plt
from transformers import TableTransformerForObjectDetection
import numpy as np
from enum import Enum
import scipy


class TableDetectorTATR(Pipe):
    @staticmethod
    def process(dataobj: DataObj):
        # Detect tables in the image
        # Return the table locations as an object that can be passed to the next step in the pipeline

        inner_data = {}

        file_path = dataobj.input_file
        image = Image.open(file_path).convert("RGB")

        image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            inner_data['detection'] = f"Detected {model.config.id2label[label.item()]} with confidence " +f"{round(score.item(), 3)} at location {box}"
            print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
            )
        plot_results(image, model, results['scores'], results['labels'], results['boxes'], title='Tables detected: ' + str(len(results["scores"])))

        max_width, max_height = target_sizes[0]

        if len(results["scores"]) > 0:
            for i, bbox in enumerate(results["boxes"]):
                # Extract the bounding box values as a list
                bbox = bbox.int().tolist()

                # Increase the bounding box size by 5 pixels on all sides so that
                bbox_enlarged = [
                    max(bbox[0] - 20, 0),  # expanded_x_min
                    max(bbox[1] - 20, 0),  # expanded_y_min
                    min(bbox[2] + 20, max_width),  # expanded_x_max
                    min(bbox[3] + 20, max_height)  # expanded_y_max
                ]

                table_image = image.crop(bbox_enlarged)
                plt.imshow(table_image)
                plt.axis('on')
                plt.title(
                    'cropped image of only table, number ' + str(i + 1) + ' out of ' + str(len(results["scores"])))
                plt.show()
            dataobj.data['table_image'] = table_image

        dataobj.data[__class__.__name__] = inner_data
        return dataobj


class TableDetectorDETR(Pipe):
    def process(dataobj: DataObj):
        file_path = dataobj.input_file
        image = Image.open(file_path).convert("RGB")

        feature_extractor = DetrFeatureExtractor.from_pretrained('facebook/detr-resnet-101-dc5')
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
        plot_results(image, model, scores, ids, bboxes)
        return dataobj


