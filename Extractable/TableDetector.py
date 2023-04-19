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
        print('r')
        plot_results(image, model, results['scores'], results['labels'], results['boxes'])
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


