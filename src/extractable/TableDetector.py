from typing import List

import torch
from PIL import Image
from transformers import AutoImageProcessor, TableTransformerForObjectDetection, DetrForObjectDetection, DetrImageProcessor
import numpy as np

from src.extractable import Logger, ModeManager
from src.extractable.Dataobj import DataObj
from src.extractable.Pipe import Pipe

import os
import ntpath
from pathlib import Path


class TableDetectorTATR(Pipe):
    @staticmethod
    def process(dataobj: DataObj) -> DataObj:

        images = TableDetectorTATR.load_images(dataobj)

        logger = Logger.Logger()

        table_locations:  List[dict] = []

        inner_data = {'detection': []}
        table_images = []                   # cropped images of only the table

        image_processor = AutoImageProcessor.from_pretrained("microsoft/table-transformer-detection")
        model = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")

        # loop past each image (every image is one page of the pdf)
        for i, image_path in enumerate(images):
            image = Image.open(image_path).convert("RGB")

            # run TATR on the image
            results, model, target_sizes = TableDetectorTATR.runTATR(image, image_processor, model)

            # log all results
            TableDetectorTATR.logResults(results, model, logger, inner_data)

            # present results if in a mode containing presentation
            ModeManager.TableDetector_display_image(dataobj.mode, image, model, results, i, len(images))

            max_height, max_width = target_sizes[0]

            # if there are results, loop past each bounding box
            if len(results["scores"]) > 0:
                for j, bbox in enumerate(results["boxes"]):

                    # crop the full image to only image of table
                    table_image = TableDetectorTATR.crop_image(i, image, bbox, max_height, max_width, table_locations)

                    # show image containing the table if in presentation mode
                    ModeManager.TableDetector_display_table(dataobj.mode, table_image, results, j)

                    # save the image to temporary directory
                    TableDetectorTATR.save_img_to_temp(table_image, dataobj, logger, table_images, i, j)

        dataobj.data['table_locations'] = table_locations
        dataobj.data['table_images'] = table_images
        dataobj.data[__class__.__name__] = inner_data
        return dataobj

    @staticmethod
    def load_images(dataobj: DataObj) -> DataObj:
        # Detect tables in the image
        # Return the table locations as an object that can be passed to the next step in the pipeline
        # load_images

        if dataobj.data['table_images'] is not None and len(dataobj.data['table_images']) > 0:
            return dataobj.data['table_images']
        elif dataobj.data['pdf_images'] is not None and len(dataobj.data['pdf_images']) > 0:
            return dataobj.data['pdf_images']
        else:
            raise Exception("No images found, is your input a valid PDF or PNG? Is Poppler installed and in PATH?")

    @staticmethod
    def runTATR(image, image_processor, model):

        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # convert outputs (bounding boxes and class logits) to COCO API
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]

        return results, model, target_sizes

    @staticmethod
    def logResults(results, model, logger, inner_data):
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            box = [round(i, 2) for i in box.tolist()]
            inner_data['detection'].append(
                f"Detected {model.config.id2label[label.item()]} with confidence: " + f"{round(score.item(), 3)} at location: {box}")
            logger.info(
                f"Detected {model.config.id2label[label.item()]} with confidence " f"{round(score.item(), 3)} at location {box}",
                extra={'className': __class__.__name__})

    @staticmethod
    def crop_image(i, image, bbox, max_height, max_width, table_locations):
        # cropImage
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

        return image.crop(bbox_enlarged)

    @staticmethod
    def save_img_to_temp(table_image, dataobj, logger, table_images, i, j):
        image_name = Path(ntpath.basename(dataobj.input_file)).stem
        image_path_string = f"{image_name}_table_{i + 1}{('.' + str(j + 1)) if i > 0 else ''}.jpg"
        image_path = dataobj.temp_dir + '\\' + os.path.normpath(image_path_string)

        logger.info('Saved image to: ' + image_path, extra={'className': __class__.__name__})

        table_image.save(image_path, "JPEG")
        table_images.append(image_path)


class TableDetectorDETR(Pipe):
    #unused
    @staticmethod
    def process(dataobj: DataObj) -> DataObj:
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
        ModeManager.plot_results(image, model, scores, ids, bboxes, title='detected tables using DETR')
        return dataobj


